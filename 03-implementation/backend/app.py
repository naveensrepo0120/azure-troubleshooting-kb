from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient
import os
import uuid
from typing import List, Optional
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

app = FastAPI()

# Environment configuration
COSMOS_ENDPOINT = os.environ.get("COSMOS_ENDPOINT")
DATABASE_NAME = "troubleshootingdb"
CONTAINER_NAME = "troubleshooting"
SEARCH_ENDPOINT = os.environ.get("SEARCH_ENDPOINT")
SEARCH_INDEX_NAME = "troubleshooting-index"


# -----------------------------
# Cosmos container factory
# -----------------------------
def get_container():
    if not COSMOS_ENDPOINT:
        raise Exception("COSMOS_ENDPOINT environment variable not set")

    credential = DefaultAzureCredential()
    client = CosmosClient(COSMOS_ENDPOINT, credential=credential)
    database = client.get_database_client(DATABASE_NAME)
    return database.get_container_client(CONTAINER_NAME)

def get_search_client():
    if not SEARCH_ENDPOINT:
        raise Exception("SEARCH_ENDPOINT not configured")

    key = os.environ.get("SEARCH_API_KEY")
    if not key:
        raise Exception("SEARCH_API_KEY not configured")

    return SearchClient(
        endpoint=SEARCH_ENDPOINT,
        index_name=SEARCH_INDEX_NAME,
        credential=AzureKeyCredential(key)
    )
# -----------------------------
# Request model
# -----------------------------
class TroubleshootingEntry(BaseModel):
    title: str
    issueDescription: str
    stepsTaken: List[str]
    resolution: str
    status: str
    tags: List[str]


# -----------------------------
# Health endpoint
# -----------------------------
@app.get("/")
def health():
    return {"status": "API is running"}


# -----------------------------
# Create troubleshooting entry
# -----------------------------
@app.post("/api/troubleshooting", status_code=201)
def create_entry(entry: TroubleshootingEntry):
    try:
        # 🔎 Temporary Debug
        print("SEARCH_ENDPOINT:", SEARCH_ENDPOINT)
        print("SEARCH_API_KEY exists:", bool(os.environ.get("SEARCH_API_KEY")))

        container = get_container()
        item = entry.model_dump()
        item["id"] = str(uuid.uuid4())

        container.create_item(body=item)

        search_client = get_search_client()
        search_client.upload_documents(documents=[item])

        return item

    except Exception as e:
        import traceback
        print("ERROR:", str(e))
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Get troubleshooting entry
# -----------------------------
@app.get("/api/troubleshooting/{item_id}")
def get_entry(item_id: str):
    try:
        container = get_container()
        item = container.read_item(item=item_id, partition_key=item_id)
        return item

    except Exception:
        raise HTTPException(status_code=404, detail="Item not found")


# -----------------------------
# Basic search (Cosmos query)
# -----------------------------
@app.get("/api/troubleshooting/search")
def search_entries(q: Optional[str] = None):
    if not q:
        raise HTTPException(status_code=400, detail="Search query required")

    try:
        container = get_container()
        query = (
            "SELECT * FROM c "
            "WHERE CONTAINS(c.title, @query) "
            "OR CONTAINS(c.issueDescription, @query)"
        )

        items = list(
            container.query_items(
                query=query,
                parameters=[{"name": "@query", "value": q}],
                enable_cross_partition_query=True,
            )
        )

        return items

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
