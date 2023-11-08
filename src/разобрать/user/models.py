# from datetime import datetime
# from sqlalchemy import create_engine, Column, func, DateTime, Integer, BIGINT, TIMESTAMP, String, Boolean, Float, ForeignKey, UniqueConstraint
# from sqlalchemy.orm import relationship

# from src.database import Base


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     is_active: bool = Column(Boolean, default=True, nullable=False)
#     created_at = Column(DateTime, default=func.now(), nullable=True)
#     updated_at = Column(DateTime, default=func.now(),
#                         onupdate=func.now(), nullable=True)
#     deleted_flag = Column(Boolean, default=False)
#     deleted_at = Column(DateTime, nullable=True)


# class UserData(Base):
#     __tablename__ = "user_datas"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     username = Column(String, nullable=False, unique=True)
#     hashed_password = Column(String(length=1024), nullable=False)
#     name = Column(String, nullable=True)
#     number_phone = Column(BIGINT, unique=True, nullable=True)
#     employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
#     role_id = Column(Integer, ForeignKey("roles.id"), default=1)

#     employees = relationship('Employee', foreign_keys=[employee_id])
#     users = relationship('User', foreign_keys=[user_id])
#     roles = relationship('Role', foreign_keys=[role_id])
#     # tokens = relationship('Token', back_populates='user')


# class Shop(Base):
#     __tablename__ = "shops"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id"))


# class TokenBotTelegram(Base):
#     __tablename__ = "tokens_bot_telegram"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     token_bot = Column(BIGINT, nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id"))


# class GroupTelegram(Base):
#     __tablename__ = "groups_telegram"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     token_group_id = Column(BIGINT, nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id"))


# # class Role(Base):
# #     __tablename__ = "roles"

# #     id = Column(Integer, primary_key=True, index=True)
# #     name = Column(String, nullable=False)
# #     created_at = Column(DateTime, default=func.now(), nullable=True)
# #     updated_at = Column(DateTime, default=func.now(),
# #                         onupdate=func.now(), nullable=True)
# #     deleted_flag = Column(Boolean, default=False)
# #     deleted_at = Column(DateTime, nullable=True)
