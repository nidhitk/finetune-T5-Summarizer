from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schema import DialogueInput
from data_processing import summarize
from settings import get_csv_env
from redis.exceptions import RedisError
from redis_client import redis_client
import hashlib
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Text Summarizer App", description="Text summarization using T5")

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_csv_env("CORS_ALLOW_ORIGINS"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)


@app.get("/")
def health_check():
    return {"status": "ok"}



@app.post("/summarize")
def post_summarize(dialogue_input: DialogueInput):
    dialogue = dialogue_input.dialogue.strip()

    if not dialogue:
        logger.info("chat empty detacted")
        raise HTTPException(
            status_code=400,
            detail="Dialogue cannot be empty"
        )

    # Create a deterministic cache key
    dialogue_hash = hashlib.sha256(
        dialogue.encode("utf-8")
    ).hexdigest()

    cache_key = f"summarize:{dialogue_hash}"

    # 1. Check Redis
    try:
        cached_summary = redis_client.get(cache_key)

        if cached_summary is not None:
            
            logger.info("cache hit")

            return {
                "summary": cached_summary,
                "cached": True
            }

    except RedisError:
        # Redis failure should not break summarization
        pass

    # 2. Generate summary
    try:
        logger.info("cache missed")
        summary = summarize(dialogue)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate summary"
        )

    # 3. Store summary in Redis
    try:
        redis_client.setex(
            cache_key,
            3600,  # 1 hour TTL
            summary
        )
        logger.info("cached")
    except RedisError:
        # Don't fail the request if Redis is unavailable
        pass
    return {
        "summary": summary,
        "cached": False
    }
