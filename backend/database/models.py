from database.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Boolean, String, Integer
import uuid

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # id = Column(String, unique=False, nullable=True)
    title = Column(String, unique=False, nullable=False)
    description = Column(String, unique=False, nullable=True)
    completed = Column(Boolean, default=False, unique=False)
    priority = Column(String, default="nonpriority", unique=False)

