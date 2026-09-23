from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.orm import declarative_base

# 1. Engine Setup (echo=True helps inspect generated CREATE TABLE SQL)
engine = create_engine("sqlite:///orm_database.db", echo=True)

# 2. Declarative Base Registry
Base = declarative_base()

# 3. Model Definitions with Types and Constraints
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, in_stock={self.in_stock})>"


if __name__ == "__main__":
    # 4. Generate Tables in the SQLite Database
    Base.metadata.create_all(engine)
    print("\nDatabase and tables created successfully!")