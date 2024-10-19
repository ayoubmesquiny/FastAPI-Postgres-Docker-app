from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import SessionLocal
from app.schemas.item import ItemCreate, ItemResponse
from app.services.item import create_item, get_item, get_items, update_item, delete_item

# Create an API router specifically for item-related routes
router = APIRouter()

# Dependency to get a database session
async def get_db() -> AsyncSession:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()  # Close the session asynchronously

# 1. Create a new item
@router.post("/items/", response_model=ItemResponse)
async def create_new_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    return await create_item(db, item)  # Await the service call

# 2. Get a single item by ID
@router.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    db_item = await get_item(db, item_id)  # Await the service call
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# 3. Get all items with pagination
@router.get("/items/", response_model=list[ItemResponse])
async def read_items(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await get_items(db, skip=skip, limit=limit)  # Await the service call

# 4. Update an item by ID
@router.put("/items/{item_id}", response_model=ItemResponse)
async def update_existing_item(item_id: int, item: ItemCreate, db: AsyncSession = Depends(get_db)):
    db_item = await update_item(db, item_id, item)  # Await the service call
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# 5. Delete an item by ID
@router.delete("/items/{item_id}")
async def delete_existing_item(item_id: int, db: AsyncSession = Depends(get_db)):
    db_item = await get_item(db, item_id)  # Await the service call
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await delete_item(db, item_id)  # Await the service call
    return {"message": "Item deleted"}
