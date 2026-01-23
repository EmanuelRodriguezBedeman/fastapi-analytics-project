"""
Order model
"""

# from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
# from sqlalchemy.sql import func
# from sqlalchemy.orm import relationship
# import enum
# from app.database import Base


# class OrderStatus(str, enum.Enum):
#     """Order status enumeration"""
#     PENDING = "pending"
#     PROCESSING = "processing"
#     SHIPPED = "shipped"
#     DELIVERED = "delivered"
#     CANCELLED = "cancelled"


# class Order(Base):
#     """Order database model"""
#     
#     __tablename__ = "orders"
#     
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     total_amount = Column(Float, nullable=False)
#     status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
#     shipping_address = Column(String, nullable=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())
#     
#     # Relationships
#     user = relationship("User", backref="orders")
