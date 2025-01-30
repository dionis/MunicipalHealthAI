from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
import asyncio
from neo4j import GraphDatabase
import subprocess
import json

# FastAPI app initialization
app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Cambia esto al dominio de tu frontend si es necesario
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],
)

# Neo4j driver configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Models
class QueryModel(BaseModel):
    query: str

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "API funcionando correctamente"}

# Function to process text using local phi 3.5 LLM
def process_with_phi3_5(text: str) -> dict:
    try:
        # Call the local LLM model (phi 3.5) using subprocess
        result = subprocess.run(
            ["ollama", "generate", "--model", "phi-3.5"],
            input=text,
            text=True,
            capture_output=True
        )
        if result.returncode != 0:
            raise Exception(result.stderr)
        return json.loads(result.stdout)
    except Exception as e:
        raise RuntimeError(f"Error processing text with phi 3.5: {str(e)}")

# Upload and process document
@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    try:
        # Read file content
        content = await file.read()

        # Process document with phi 3.5 LLM
        structured_data = process_with_phi3_5(content.decode("utf-8"))

        # Store structured data in Neo4j
        with driver.session() as session:
            for node in structured_data.get("nodes", []):
                session.run("CREATE (:Node {id: $id, content: $content})", 
                            id=node["id"], content=node["content"])

            for relation in structured_data.get("relations", []):
                session.run(
                    "MATCH (a:Node {id: $from_id}), (b:Node {id: $to_id}) "
                    "CREATE (a)-[:RELATED_TO]->(b)",
                    from_id=relation["from"], to_id=relation["to"]
                )

        return {"message": "Document processed and stored successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

# Query the knowledge graph
@app.post("/query/")
async def query_graph(query: QueryModel):
    try:
        with driver.session() as session:
            result = session.run(query.query)
            data = [record.data() for record in result]

        return {"result": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing query: {str(e)}")

# Shutdown event to close Neo4j connection
@app.on_event("shutdown")
async def shutdown_event():
    driver.close()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
