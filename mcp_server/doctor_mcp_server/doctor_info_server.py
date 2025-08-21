import os
import json # Added json import
from fastmcp import FastMCP # Import FastMCP
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

# Define the path to the local JSON file
DOCTORS_JSON_FILE = "..\\mcp_server\\doctor_mcp_server\\doctor_list_sg.json"
#DOCTORS_JSON_FILE = "doctor_list_sg.json"

# Global variable to store doctor data
DOCTORS_DATA = []

def _load_doctors_from_json():
    """
    Loads doctor information from a local JSON file.
    """
    print(f"Loading doctor information from {DOCTORS_JSON_FILE}...")
    try:
        with open(DOCTORS_JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # The JSON is a dictionary with DOCSG001, DOCSG002 keys.
            # We need to convert it to a list of doctor dictionaries.
            doctors = [doc_data for doc_id, doc_data in data.items()]
            print(f"Loaded {len(doctors)} doctors from {DOCTORS_JSON_FILE}.\n")
            return doctors
    except FileNotFoundError:
        print(f"Error: {DOCTORS_JSON_FILE} not found. Please ensure the file exists in the same directory as the script.\n")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {DOCTORS_JSON_FILE}: {e}\n")
        return []

# Load doctor data when the script starts
DOCTORS_DATA = _load_doctors_from_json()

# Initialize FastMCP server (for tool definition, not for running the server directly)
mcp = FastMCP(name="DoctorInfoServer")

def _get_doctors_by_location_impl(location: str) -> str:
    """
    Returns a list of doctors based on the provided location.
    This is the actual implementation.
    """
    if not DOCTORS_DATA:
        return "No doctor data available. Please ensure 'doctor_list_sg.json' is correctly loaded.\n"

    filtered_doctors = []
    for doctor in DOCTORS_DATA:
        # Assuming 'location' field exists in each doctor's dictionary
        if location.lower() in doctor.get("location", "").lower():
            filtered_doctors.append(doctor)
    
    if not filtered_doctors:
        return f"No doctors found in {location}.\n"
    
    response_str = f"Doctors in {location}:\n"
    for doc in filtered_doctors:
        response_str += f"- {doc.get('name', 'N/A')} ({doc.get('specialty', 'N/A')}) at {doc.get('clinic', 'N/A')} ({doc.get('location', 'N/A')})\n"
    return response_str

@mcp.tool()
def get_doctors_by_location(location: str) -> str:
    """
    FastMCP tool wrapper for _get_doctors_by_location_impl.
    """
    return _get_doctors_by_location_impl(location)

# Define Pydantic model for input
class LocationInput(BaseModel):
    location: str

# Initialize FastAPI app
app = FastAPI()

# Expose the FastMCP tool via a FastAPI endpoint
@app.post("/call/doctor_info_tool")
async def call_doctor_info_tool(input: LocationInput):
    """
    Endpoint to call the doctor_info_tool.
    """
    # Call the underlying implementation directly
    return _get_doctors_by_location_impl(input.location)


if __name__ == "__main__":
    print("Starting Doctor MCP Server (via FastAPI and Uvicorn). Access the API at http://localhost:8002/docs")
    print("To use the tool, send a POST request to http://localhost:8002/call/doctor_info_tool with a JSON body like: {'location': 'Orchard'}")
    #uvicorn.run(app, host="0.0.0.0", port=8002)
    mcp.run(transport="stdio")