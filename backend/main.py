from database import SessionLocal, engine
from models import Base, ChatMessage
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from llm_wrapper import generate_response
from schemas import ChatRequest

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary memory for context
conversation_memory = {}


@app.get("/")
def home():
    return {
        "message": "LLM Observability Backend Running"
    }


@app.post("/chat")
def chat(req: ChatRequest):

    try:

        session_id = req.session_id or str(uuid4())

        history = conversation_memory.get(session_id, [])

        history.append({
            "role": "user",
            "content": req.message
        })

        db = SessionLocal()

        # Save user message
        user_msg = ChatMessage(
            session_id=session_id,
            role="user",
            content=req.message
        )

        db.add(user_msg)
        db.commit()

        # Generate AI response
        response = generate_response(
            message=req.message,
            session_id=session_id,
            history=history
        )

        # Save bot response
        bot_msg = ChatMessage(
            session_id=session_id,
            role="assistant",
            content=str(response)
        )

        db.add(bot_msg)
        db.commit()

        db.close()

        history.append({
            "role": "assistant",
            "content": str(response)
        })

        # Keep last 6 messages in memory
        conversation_memory[session_id] = history[-6:]

        return {
            "session_id": session_id,
            "response": str(response)
        }

    except Exception as e:

        return {
            "error": str(e)
        }


@app.get("/conversation/{session_id}")
def get_conversation(session_id: str):

    db = SessionLocal()

    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).all()

    db.close()

    return messages

@app.get("/conversations")
def get_conversations():

    db = SessionLocal()

    sessions = db.query(
        ChatMessage.session_id
    ).distinct().all()

    result = []

    for s in sessions:

        first_msg = db.query(ChatMessage).filter(
            ChatMessage.session_id == s[0],
            ChatMessage.role == "user"
        ).first()

        result.append({
            "session_id": s[0],
            "title": first_msg.content[:30] if first_msg else "New Chat"
        })

    db.close()

    return result