from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

    users = relationship("User", back_populates="category")

    def __str__(self):
        return f"Category(id={self.id}, name={self.name}, description={self.description})"
