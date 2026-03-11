from typing import List, Optional
from fastmcp import FastMCP, tool, InputParams
from pydantic import BaseModel
import httpx

# ---- Models ----

class Category(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class Tag(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class Pet(BaseModel):
    id: Optional[int] = None
    name: str
    category: Optional[Category] = None
    photoUrls: List[str]
    tags: Optional[List[Tag]] = None
    status: Optional[str] = None

# ---- Input and Output Schemas ----

class FindByStatusInput(BaseModel):
    status: str  # Comma-separated string: "available", "pending", "sold"

class FindByStatusOutput(BaseModel):
    pets: List[Pet]

# ---- The Tool Implementation ----

@tool(
    name="pet/findByStatus",
    description="Finds pets by status (available, pending, sold). Returns a list of pets.", 
    input=FindByStatusInput,
    output=FindByStatusOutput
)
async def find_pets_by_status(params: InputParams):
    inp: FindByStatusInput = params.input
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://petstore3.swagger.io/api/v3/pet/findByStatus",
            params={"status": inp.status}
        )
        response.raise_for_status()
        results = response.json()
    pets = [Pet(**data) for data in results]
    return FindByStatusOutput(pets=pets)

# ---- Server ----

server = FastMCP()        # instantiate the server
server.include_tools([find_pets_by_status])   # register the tool

if __name__ == "__main__":
    server.serve()          # runs the FastMCP server with all tools