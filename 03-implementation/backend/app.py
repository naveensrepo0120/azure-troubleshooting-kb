from fastapi import FastAPI
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient
import os
import uuid

app = FastAPI()

COSMOS_ENDPOINT = os.environ.get("COSMOS_ENDPOINT")
DATABASE_NAME = "troubleshootingdb"
CONTAINER_NAME = "troubleshooting"

credential = DefaultAzureCredential()
client = CosmosClient(COSMOS_ENDPOINT, credential=credential)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)


@app.get("/")
def root():
    return {"status": "API is running"}


@app.post("/troubleshooting")
def create_entry():
    item = {
        "id": str(uuid.uuid4()),
        "title": "Test Issue",
        "issueDescription": "Sample issue",
        "stepsTaken": ["Step 1", "Step 2"],
        "resolution": "Test resolution",
        "status": "Resolved",
        "tags": ["test"]
    }

    container.create_item(body=item)
    return {"message": "Item created", "id": item["id"]}


@app.get("/troubleshooting/{item_id}")
def get_entry(item_id: str):
    item = container.read_item(item=item_id, partition_key=item_id)
    return item
