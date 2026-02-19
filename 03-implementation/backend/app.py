from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os
import uuid
from typing import List, Optional

app = FastAPI()

# -----------------------------
# Environment Configuration
# -----------------------------
COSMOS_ENDPOINT = os.environ.get("COSMOS_ENDPOINT")
DATABASE_NAME = "troubleshootingdb"
CONTAINER_NAME = "troubleshooting"

SEARCH_ENDPOINT = os.environ.get("SEARCH_ENDPOINT")
SEARCH_INDEX_NAME = "troubleshooting-index"
SEARCH_API_KEY = os.environ.get("SEARCH_API_KEY")


# -----------------------------
# Cosmos Client Factory
# -----------------------------
def get_container():
    if not COSMOS_ENDPOINT:
        raise Exception("COSMOS_ENDPOINT environment variable not set")

    credential = DefaultAzureCredential()
    client = CosmosClient(COSMOS_ENDPOINT, credential=credential)
    database = client.get_database_client(DATABASE_NAME)
    return database.get_container_client(CONTAINER_NAME)


# -----------------------------
# Search Client Factory
# -----------------------------
def get_search_client():
    if not SEARCH_ENDPOINT:
        raise Exception("SEARCH_ENDPOINT not configured")

    if not SEARCH_API_KEY:
        raise Exception("SEARCH_API_KEY not configured")

    return SearchClient(
        endpoint=SEARCH_ENDPOINT,
        index_name=SEARCH_INDEX_NAME,
        credential=AzureKeyCredential(SEARCH_API_KEY),
    )


# -----------------------------
# Request Model
# -----------------------------
class TroubleshootingEntry(BaseModel):
    title: str
    issueDescription: str
    stepsTaken: List[str]
    resolution: str
    status: str
    tags: List[str]


# -----------------------------
# Health Endpoint
# -----------------------------
@app.get("/")
def health():
    return {"status": "API is running"}


# -----------------------------
# Create Entry (Cosmos + Search)
# -----------------------------
@app.post("/api/troubleshooting", status_code=201)
def create_entry(entry: TroubleshootingEntry):
    try:
        container = get_container()
        item = entry.model_dump()
        item["id"] = str(uuid.uuid4())

        # Write to Cosmos (system of record)
        container.create_item(body=item)

        # Index in Search (retrieval layer)
        search_client = get_search_client()
        search_client.upload_documents(documents=[item])

        return item

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Search Entries (Cognitive Search)
# -----------------------------
@app.get("/api/troubleshooting/search")
def search_entries(
    q: Optional[str] = None,
    status: Optional[str] = None,
    tag: Optional[str] = None
):
    try:
        search_client = get_search_client()

        filters = []

        if status:
            filters.append(f"status eq '{status}'")

        if tag:
            filters.append(f"tags/any(t: t eq '{tag}')")

        filter_query = " and ".join(filters) if filters else None

        results = search_client.search(
            search_text=q or "*",
            filter=filter_query,
            facets=["status", "tags"],
            top=10,
            scoring_profile="kb-ranking-profile",
            search_mode="all"
        )

        response = {
            "results": [doc for doc in results],
            "facets": results.get_facets()
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# Get Entry by ID (Cosmos)
# -----------------------------
@app.get("/api/troubleshooting/{item_id}")
def get_entry(item_id: str):
    try:
        container = get_container()
        item = container.read_item(item=item_id, partition_key=item_id)
        return item

    except Exception:
        raise HTTPException(status_code=404, detail="Item not found")
