# finetune-T5-Summarizer

A dialogue/text summarization app powered by a **fine-tuned T5 model**, served through a **FastAPI** backend with **Redis** caching, and a **React (Vite)** frontend. The whole stack is containerized with Docker Compose.



---

## ✨ Features

- 🔤 **Text summarization** using a T5 model fine-tuned for dialogue/text summarization, hosted on Hugging Face (`nidhitk/T5-summarizer`)
- ⚡ **FastAPI** backend exposing a simple `/summarize` REST endpoint
- 🧠 **Redis caching** — summaries are cached by a SHA-256 hash of the input dialogue (1 hour TTL) to avoid recomputing summaries for repeated input; the API still works even if Redis is unavailable
- 💻 **React + Vite frontend** for interacting with the summarizer in the browser
- 🐳 **Dockerized** — backend, Redis, and frontend are all defined in `docker-compose.yml` for one-command startup
- 🧪 **Training pipeline** (`t5_model_training/`) used to fine-tune the T5 model

---

## 🏗️ Project Structure

```
finetune-T5-Summarizer/
├── main.py                  # FastAPI app & /summarize endpoint
├── config.py                 # Loads the T5 model/tokenizer, sets device (CUDA/MPS/CPU)
├── data_processing.py        # Text cleaning + summarization logic
├── schema.py                  # Pydantic request schema (DialogueInput)
├── settings.py                 # .env loading & environment variable helpers
├── redis_client.py              # Redis client setup
├── requirements.txt              # Python dependencies (local/dev)
├── requirements.docker.txt        # Python dependencies (Docker image)
├── Dockerfile                      # Backend Docker image
├── docker-compose.yml               # Orchestrates backend + redis + frontend
├── .env.example                      # Sample environment variables
├── frontend/                          # React + Vite client app
├── t5_model_training/                  # Notebooks/scripts for fine-tuning the T5 model
└── .github/workflows/                    # CI/CD workflows
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js (for running the frontend outside Docker)
- Docker & Docker Compose (recommended — easiest way to run the full stack)
- A Redis instance (only needed if not using Docker Compose)

### Option 1: Run with Docker Compose (recommended)

This spins up the backend, Redis, and frontend together.

```bash
git clone https://github.com/nidhitk/finetune-T5-Summarizer.git
cd finetune-T5-Summarizer
cp .env.example .env   # adjust values if needed
docker compose up --build
```

- Backend API → `http://localhost:8000`
- Frontend → `http://localhost:5173`

### Option 2: Run manually (without Docker)

**1. Backend**

```bash
cd finetune-T5-Summarizer
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Make sure you have a Redis server running locally (or update `REDIS_URL` in `.env` to point to your Redis instance).

**2. Frontend**

```bash
cd frontend
npm install
npm run dev
```

By default the frontend expects the API at the URL set in `VITE_API_BASE_URL`.

---

## ⚙️ Environment Variables

Set these in a `.env` file (see `.env.example`):

| Variable | Description | Example |
|---|---|---|
| `MODEL_DIR` | Local path or Hugging Face model ID for the T5 model | `nidhitk/T5-summarizer` |
| `CORS_ALLOW_ORIGINS` | Comma-separated list of allowed origins for CORS | `http://localhost:5173,http://127.0.0.1:5173` |
| `VITE_API_BASE_URL` | Backend API base URL used by the frontend | `http://127.0.0.1:8000` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |

> By default, `config.py` loads the model directly from the Hugging Face Hub (`nidhitk/T5-summarizer`), so no local model download step is strictly required.

---

## 📡 API Usage

### Health Check

```
GET /
```

**Response:**
```json
{ "status": "ok" }
```

### Summarize Text

```
POST /summarize
Content-Type: application/json
```

**Request body:**
```json
{
  "dialogue": "Your text or dialogue to summarize goes here..."
}
```

**Response:**
```json
{
  "summary": "Generated summary text.",
  "cached": false
}
```

- `cached: true` means the summary was served from Redis instead of being regenerated.
- If `dialogue` is empty, the API returns a `400` error.
- If summarization fails internally, the API returns a `500` error.

**Example with `curl`:**

```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"dialogue": "Alice: Are we still meeting at 5? Bob: Yes, see you then."}'
```

---

## 🧠 Model

The summarization model is a **T5** model fine-tuned for summarization and published on the Hugging Face Hub as [`nidhitk/T5-summarizer`](https://huggingface.co/nidhitk/T5-summarizer). Training code/notebooks for reproducing or extending the fine-tuning process live in [`t5_model_training/`](./t5_model_training).

Inference uses beam search decoding (`num_beams=4`) with a max output length of 150 tokens, and automatically runs on CUDA or Apple MPS if available, falling back to CPU otherwise.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Model | T5 (Transformers, PyTorch) |
| Backend | FastAPI, Uvicorn |
| Caching | Redis |
| Frontend | React, Vite |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |

---
