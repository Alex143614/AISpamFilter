from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime

from sqlalchemy.orm import declarative_base

engine = create_engine("sqlite:///./spam_filter.db", echo=True)
Base = declarative_base()


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True)
    sender = Column(String(50), nullable=False)
    text = Column(String(300), nullable=False)
    time = Column(DateTime, default=datetime.now, nullable=False)
    classification = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    reasons = Column(String(300), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=True)
class Statistic(Base):
    __tablename__ = "statistics"
    id = Column(Integer, primary_key=True)
    sender = Column(String(50), nullable=False)
    text = Column(String(300), nullable=False)
    scores = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=True)
Base.metadata.create_all(bind=engine)