from fastapi import APIRouter, HTTPException, Depends
from app.model import Case
from app.db import cases_collection
from typing import List
from bson import ObjectId
from datetime import datetime

router = APIRouter()

# 🔹 Helper function to convert MongoDB documents to Python dict
def case_serializer(case) -> dict:
    return {
            "_id": str(case["_id"]),  # Convert ObjectId to string
            "name": case["name"],
            "description": case["description"],
            "type": case["type"],
            "subtype": case["subtype"],
            "status": case["status"],
            "archived": case["archived"],
            "involved_personnel": case["involved_personnel"],
            "created_at": case["created_at"],
            "updated_at": case["updated_at"]
        }


# 🔹 Create a Case (POST /cases/)
@router.post("/", response_model=dict)
async def create_case(case: dict):
    print("Received Data:", case)  # Debugging line
    
    # Set default dates if not provided
    if "archived" not in case:
        case["archived"] = False
    if "created_at" not in case:
        case["created_at"] = datetime.utcnow()
    if "updated_at" not in case:
        case["updated_at"] = datetime.utcnow()
    
    result = await cases_collection.insert_one(case)
    return {"id": str(result.inserted_id), "message": "Case creado exitosamente"}

# 🔹 Get All Cases (GET /cases/)
@router.get("/", response_model=List[dict])
async def get_cases():
    cases = await cases_collection.find().to_list(100)
    return [case_serializer(case) for case in cases]


# 🔹 Get a Case by ID (GET /cases/{case_id})

@router.get("/{case_id}", response_model=dict)
async def get_case(case_id: str):
    # Query MongoDB for the case by _id
    case = await cases_collection.find_one({"_id": ObjectId(case_id)})
    
    # If case is found, serialize it and return
    if case:
        # Prepare the case data
        case_data = case_serializer(case)
        # Return the serialized case data
        return case_data

    # If no case is found, raise 404 error
    raise HTTPException(status_code=404, detail="Caso no encontrado")



# 🔹 Update a Case (PUT /cases/{case_id})
@router.put("/{case_id}", response_model=dict)
async def update_case(case_id: str, case: dict):
    updated_case = await cases_collection.find_one_and_update(
        {"_id": ObjectId(case_id)},
        {"$set": case},
        return_document=True
    )
    if updated_case:
        updated_case["updated_at"] = datetime.now()
        return {"message": "¡Caso actualizado extosamente!", "case":case_serializer(updated_case)}
    raise HTTPException(status_code=404, detail="Caso no encontrado")


# 🔹 Archive or restore a Case (DELETE /cases/{case_id})
@router.delete("/{case_id}", response_model=dict)
async def archive_case(case_id: str):
    # Update the case status to "archived" by setting the archived field to True
    # If already True, set to False
    # Find the case by its ID
    case = await cases_collection.find_one({"_id": ObjectId(case_id)})

    # If case is not found, raise an error
    if not case:
        raise HTTPException(status_code=404, detail="Case no encontrado")
    
    # Toggle the archived status
    new_archived_status = not case["archived"]

    # Update the case with the new archived status
    archived_case = await cases_collection.find_one_and_update(
        {"_id": ObjectId(case_id)},
        {"$set": {"archived": new_archived_status}},
        return_document=True
    )
    
    # If the case is found and updated, return a success message
    if archived_case:
        return {"message": "¡Caso archivado extosamente!", "case": case_serializer(archived_case)}
    
    # If no case is found, raise 404 error
    raise HTTPException(status_code=404, detail="Caso no encontrado")

# 🔹 Permanently Delete a Case (DELETE /cases/permanent/{case_id})
@router.delete("/permanent/{case_id}", response_model=dict)
async def delete_case(case_id: str):
    # Find and delete the case by its ID
    delete_result = await cases_collection.delete_one({"_id": ObjectId(case_id)})

    # If the case is deleted, return a success message
    if delete_result.deleted_count == 1:
        return {"message": "¡Caso eliminado permanentemente!"}
    
    # If no case is found, raise 404 error
    raise HTTPException(status_code=404, detail="Caso no encontrado")
