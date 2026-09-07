from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schema import DialogueInput
from data_processing import summarize
from settings import get_csv_env

app = FastAPI(title="Text Summarizer App", description="Text summarization using T5")

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_csv_env("CORS_ALLOW_ORIGINS"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "ok"}



@app.post("/summarize")
def post_summarize(dialogue_input: DialogueInput):
    print("Received dialogue:")
    print(repr(dialogue_input.dialogue))
    summary = summarize(dialogue_input.dialogue)
    return {"summary": summary}
