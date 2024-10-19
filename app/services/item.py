from sqlalchemy.ext.asyncio import AsyncSession
from app.models.item import Item
from sqlalchemy.future import select
from app.schemas.item import ItemCreate, ItemResponse

# Service to create a new item
async def create_item(db: AsyncSession, item_create: ItemCreate) -> ItemResponse:
    new_item = Item(name=item_create.name, description=item_create.description)
    db.add(new_item)  # Add the new item to the session
    await db.commit()  # Commit the transaction to save the item in the database
    await db.refresh(new_item)  # Refresh the item to get its ID from the database
    
    # Return the newly created item as an ItemResponse
    return ItemResponse(id=new_item.id, name=new_item.name, description=new_item.description)

# Service to retrieve an item by ID
async def get_item(db: AsyncSession, item_id: int) -> Item:
    result = await db.execute(select(Item).filter(Item.id == item_id))
    return result.scalar_one_or_none()

# Service to retrieve all items
async def get_items(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Item).offset(skip).limit(limit))
    return result.scalars().all()

# Service to update an item
async def update_item(db: AsyncSession, item_id: int, item_update: ItemCreate) -> Item:
    item = await get_item(db, item_id)
    if item:
        item.name = item_update.name
        item.description = item_update.description
        await db.commit()
        await db.refresh(item)
    return item

# Service to delete an item
async def delete_item(db: AsyncSession, item_id: int) -> None:
    item = await get_item(db, item_id)
    if item:
        await db.delete(item)
        await db.commit()