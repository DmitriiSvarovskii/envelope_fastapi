# from sqlalchemy.orm import Session
# from .schemas import CategoryBase
# from .models import Category
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import insert, select, delete, update
# from sqlalchemy.engine import Result
# from json import dumps
# from dataclasses import asdict


# def category_to_dict(category):
#     return {
#         "id": category.id,
#         "name_rus": category.name_rus,
#         "availability": category.availability,
#         "position": category.position,

#     }


# async def get_all_categories(session: AsyncSession) -> list[CategoryBase]:
#     query = select(Category).where(
#         Category.deleted_flag != True).order_by(Category.id)
#     result: Result = await session.execute(query)
#     categories = result.scalars().all()
#     category_dicts = [
#         {
#             "id": category.id,
#             "name_rus": category.name_rus,
#             "availability": category.availability,
#             # "position": category.position,
#         }

#         for category in categories
#     ]
#     return category_dicts
#     # name_rus: str
#     # # availability: bool}
