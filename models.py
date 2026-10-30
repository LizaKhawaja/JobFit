from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Text, DateTime, JSON
from database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    resume = Column(Text, nullable=False)
    job_description = Column(Text, nullable=False)
    match_score = Column(Integer, nullable=False)
    result = Column(JSON, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )