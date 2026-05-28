from sqlalchemy import Column, String, Integer, Text, DateTime
from database import Base
from datetime import datetime
import uuid


class ChatMessage(Base):

    __tablename__ = "chat_messages"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    session_id = Column(String)

    role = Column(String)

    content = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class InferenceLog(Base):

    __tablename__ = "inference_logs"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    session_id = Column(String)

    model = Column(String)

    provider = Column(String)

    latency = Column(Integer)

    input_tokens = Column(Integer)

    output_tokens = Column(Integer)

    status = Column(String)

    input_preview = Column(Text)

    output_preview = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )