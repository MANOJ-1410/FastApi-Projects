from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from typing import List

from models import PropertyModel, UpdatePropertyModel
from database import property_collection, property_helper

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.post("/create_new_property", response_description="Add new property", response_model=List[PropertyModel])
async def create_property(property: PropertyModel = Body(...)):
    property = jsonable_encoder(property)
    new_property = await property_collection.insert_one(property)
    created_property = await property_collection.find_one({"_id": new_property.inserted_id})
    return [property_helper(created_property)]

@app.get("/fetch_property_details/{city}", response_description="Get properties by city", response_model=List[PropertyModel])
async def get_properties_by_city(city: str):
    properties = []
    async for property in property_collection.find({"city": city}):
        properties.append(property_helper(property))
    return properties

@app.put("/update_property_details/{property_id}", response_description="Update a property", response_model=List[PropertyModel])
async def update_property(property_id: str, req: UpdatePropertyModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    if len(req) >= 1:
        update_result = await property_collection.update_one({"_id": ObjectId(property_id)}, {"$set": req})
        if update_result.modified_count == 1:
            updated_property = await property_collection.find_one({"_id": ObjectId(property_id)})
            return [property_helper(updated_property)]
    raise HTTPException(status_code=404, detail=f"Property {property_id} not found")

@app.get("/find_cities_by_state/{state}", response_description="Get cities by state")
async def get_cities_by_state(state: str):
    cities = await property_collection.distinct("city", {"state": state})
    return cities

@app.get("/find_similar_properties/{property_id}", response_description="Get similar properties by city", response_model=List[PropertyModel])
async def get_similar_properties(property_id: str):
    property = await property_collection.find_one({"_id": ObjectId(property_id)})
    if property:
        properties = []
        async for prop in property_collection.find({"city": property["city"]}):
            properties.append(property_helper(prop))
        return properties
    raise HTTPException(status_code=404, detail=f"Property {property_id} not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
