from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Category
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.schemes.categories import CategoryCreate, CategoryUpdate
from fastapi import HTTPException


# DOC: Service to get all categories from user
async def get_categories(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Category).where(Category.user_id == user_id)
    )
    return result.scalars().all()


# DOC: Service to get category by id
async def get_category_by_id(db: AsyncSession, category_id: int, user_id: int):
    result = await db.execute(
        select(Category).where(
            Category.id == category_id,
            Category.user_id == user_id
        )
    )
    return result.scalar_one_or_none()


# DOC: Service to create category with user authenticated
async def create_category(
    db: AsyncSession, category: CategoryCreate, user_id: int
):
    try:
        db_category = Category(
            name=category.name,
            user_id=user_id,
            color=category.color,
        )
        db.add(db_category)
        await db.commit()
        await db.refresh(db_category)
        return db_category
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="categoryAlreadyExists")
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="databaseError")


# DOC: Service to update category with user authenticated
async def update_category(
        db: AsyncSession,
        category_id: int,
        category_update: CategoryUpdate,
        user_id: int):
    try:
        # Obtener la categoría correspondiente al usuario autenticado.
        result = await db.execute(
            select(Category).where(
                Category.id == category_id,
                Category.user_id == user_id
            )
        )
        db_category = result.scalar_one_or_none()

        # Verificar si la categoría existe.
        if not db_category:
            raise HTTPException(status_code=404, detail="CategoryNotFound")

        # DOC: Update category
        db_category.name = category_update.name
        db_category.color = category_update.color

        await db.commit()
        await db.refresh(db_category)
        return db_category

    except IntegrityError:
        # DOC: Database integrity error handling
        await db.rollback()
        raise HTTPException(status_code=400, detail="IntegrityError")

    except SQLAlchemyError:
        # doc: General SQLAlchemy error handling.
        await db.rollback()
        raise HTTPException(status_code=500, detail="DatabaseError")


# DOC: Service to delete category with user authenticated
async def delete_category(
        db: AsyncSession,
        category_id: int,
        user_id: int):
    try:
        # DOC: Obtain the category corresponding to the authenticated user
        result = await db.execute(
            select(Category).where(
                Category.id == category_id,
                Category.user_id == user_id
            )
        )
        db_category = result.scalar_one_or_none()

        # DOC: Verify if the category exists
        if not db_category:
            raise HTTPException(status_code=404, detail="categoryNotFound")

        # DOC: Delete category
        await db.delete(db_category)
        await db.commit()
        return db_category

    except SQLAlchemyError:
        # DOC: If a database error occurs, the transaction is rolled back
        await db.rollback()
        raise HTTPException(status_code=500, detail="databaseError")
