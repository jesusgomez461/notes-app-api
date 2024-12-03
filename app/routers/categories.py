from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.services.categories import (
    get_categories,
    get_category_by_id,
    create_category,
    update_category,
    delete_category,
)
from app.schemes.categories import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
)
from app.models import User
from app.core.security import get_current_user

router = APIRouter()


@router.get(
    "/",
    response_model=List[CategoryResponse],
    summary="Read Categories",
    description="Read all categories from authenticate user"
)
async def read_categories(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Read all categories from authenticate user
    """
    categories = await get_categories(db, user_id=user.id)
    return categories


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Read Category",
    description="Read a specific category from authenticate user"
)
async def read_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Read a specific category from authenticate user
    - **category_id**: ID of the category
    """
    category = await get_category_by_id(
        db, category_id=category_id, user_id=user.id
    )
    if not category:
        raise HTTPException(status_code=404, detail="categoryNotFound")
    return category


@router.post(
    "/",
    response_model=CategoryResponse,
    summary="Create Category",
    description="Create a new category from authenticate user"
)
async def create_new_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Create a new category from authenticate user
    - **name**: Name of the category
    - **color**: Color of the category
    """
    return await create_category(db, category, user_id=user.id)


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Update Category",
    description="Update a specific category from authenticate user"
)
async def update_existing_note(
    category_id: int,
    category_update: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Update a specific note from authenticate user
    - **category_id**: ID of the note
    """
    category = await update_category(
        db,
        category_id=category_id,
        category_update=category_update,
        user_id=user.id
    )
    if not category:
        raise HTTPException(
            status_code=404,
            detail="categoryNotFoundOrNotAuthorized"
        )
    return category


@router.delete(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Delete Category",
    description="Delete a specific category from authenticate user"
)
async def delete_existing_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Delete a specific category from authenticate user
    - **category_id**: ID of the category
    """
    category = await delete_category(
        db, category_id=category_id, user_id=user.id
    )
    if not category:
        raise HTTPException(
            status_code=404,
            detail="categoryNotFoundOrNotAuthorized"
        )
    return category
