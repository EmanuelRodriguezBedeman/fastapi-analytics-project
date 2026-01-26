"""
Product model
"""

# from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime
# from sqlalchemy.sql import func
# from app.database import Base


# class Product(Base):
#     """Product database model"""
#
#     __tablename__ = "products"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True, nullable=False)
#     description = Column(Text, nullable=True)
#     price = Column(Float, nullable=False)
#     stock = Column(Integer, default=0)
#     category = Column(String, index=True, nullable=True)
#     image_url = Column(String, nullable=True)
#     is_active = Column(Boolean, default=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())
