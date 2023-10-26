from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.database import get_async_session
from fastapi import APIRouter, Depends, HTTPException


async def create_table_new_schema(schema_name: str, session: AsyncSession = Depends(get_async_session)):
    await session.execute(text(f"""CREATE TABLE {schema_name}.categories (
        id SERIAL PRIMARY KEY,
        name_rus VARCHAR,
        availability BOOLEAN DEFAULT true,
        created_at TIMESTAMP DEFAULT NOW(),
        created_by INTEGER,
        updated_at TIMESTAMP DEFAULT NOW(),
        updated_by INTEGER,
        deleted_flag BOOLEAN DEFAULT false,
        deleted_at TIMESTAMP,
        FOREIGN KEY (created_by) REFERENCES users(id),
        FOREIGN KEY (updated_by) REFERENCES users(id));"""))
    await session.execute(text(f"""CREATE TABLE {schema_name}.subcategories (
        id SERIAL PRIMARY KEY,
        name VARCHAR,
        parent_category_id INTEGER REFERENCES {schema_name}.categories(id),
        FOREIGN KEY (parent_category_id) REFERENCES {schema_name}.categories(id));"""))
    await session.execute(text(f"""CREATE TABLE {schema_name}.products (
        id SERIAL PRIMARY KEY,
        category_id INTEGER REFERENCES {schema_name}.categories(id),
        subcategory_id INTEGER REFERENCES {schema_name}.subcategories(id),
        name_rus VARCHAR,
        description_rus VARCHAR,
        price FLOAT,
        wt INTEGER,
        unit_id INTEGER REFERENCES units(id),
        kilocalories INTEGER,
        proteins INTEGER,
        fats INTEGER,
        carbohydrates INTEGER,
        availability BOOLEAN,
        popular BOOLEAN,
        delivery BOOLEAN,
        takeaway BOOLEAN,
        dinein BOOLEAN,
        created_at TIMESTAMP DEFAULT NOW(),
        created_by INTEGER,
        updated_at TIMESTAMP DEFAULT NOW(),
        updated_by INTEGER,
        deleted_flag BOOLEAN DEFAULT false,
        deleted_at TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES {schema_name}.categories(id),
        FOREIGN KEY (subcategory_id) REFERENCES {schema_name}.subcategories(id),
        FOREIGN KEY (unit_id) REFERENCES units(id),
        FOREIGN KEY (created_by) REFERENCES users(id),
        FOREIGN KEY (updated_by) REFERENCES users(id));"""))
    await session.commit()
