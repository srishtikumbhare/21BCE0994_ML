from sqlalchemy import Column, Integer, String, Text
from database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(String, nullable=False)
    user = relationship("UserRequest", back_populates="documents")

class UserRequest(Base):
    __tablename__ = 'user_requests'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = Column(String(50), ForeignKey('documents.id'))
    request_count = Column(Integer)
