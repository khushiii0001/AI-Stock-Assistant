from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

from agent import ask_agent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Stock Assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str
    history: list = []


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
def home():

    return {
        "message": "Stock Assistant Running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/chat-stream")
def chat(request: ChatRequest):

    def generate():

        for token in ask_agent(
            request.question,
            request.history
        ):
            yield token

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )