# Quite Scale AI — Multilingual RAG Receptionist Demo

> **Production-grade AI infrastructure for high-revenue service businesses.**  
> Built by [Shaheer Rizwan](www.linkedin.com/in/muhammad-shaheer-rizwan-) — Applied AI Engineer | FastAPI · LangChain · RAG Pipelines

---

## What This Is

A fully functional **Retrieval-Augmented Generation (RAG) API** that powers a 24/7 multilingual AI receptionist for medical tourism clinics and luxury boutique hotels.

Drop in your business's FAQ, SOPs, or pricing PDFs — the system instantly answers client questions in **English, Turkish, Arabic, German, or Russian** with source citations, zero hallucination risk, and sub-second latency.

---

## Architecture

```
Client (WhatsApp / Telegram / Web Widget)
        │
        ▼
  FastAPI Backend  ←──────────────────────────────┐
        │                                          │
        ▼                                          │
  RAG Pipeline (LangChain)               Chroma Vector Store
        │                                  (local / hosted)
        ▼                                          │
  OpenAI GPT-4o-mini  ──── Embeddings ────────────┘
        │
        ▼
  Structured JSON Response → Client
```

**Stack:**
- **Backend:** Python 3.11, FastAPI, Pydantic v2
- **AI / RAG:** LangChain, OpenAI GPT-4o-mini, ChromaDB
- **Deployment:** Docker, Render / DigitalOcean

---

## Features

- ✅ **RAG Pipeline** — answers only from your documents, no hallucinations
- ✅ **Multilingual** — EN / TR / AR / DE / RU out of the box
- ✅ **Source Citations** — every answer includes document references
- ✅ **Plug-and-play** — drop `.txt` or `.pdf` files into `/docs`, restart, done
- ✅ **Production-ready** — health check endpoint, Docker, CORS config, env management
- ✅ **Modular** — clean separation of routers / services / models

---

## Quickstart

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/quite-scale-rag-demo
cd quite-scale-rag-demo

# 2. Set up environment
cp .env.example .env
# Add your OPENAI_API_KEY to .env

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your business documents
# Drop .txt files into the /docs directory
# A sample FAQ is included for demo purposes

# 5. Run
uvicorn app.main:app --reload
```

API will be live at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

---

## API Usage

### POST `/chat/`

```json
{
  "question": "Do you offer packages for international patients?",
  "language": "en",
  "session_id": "user_123"
}
```

**Response:**
```json
{
  "answer": "Yes, we offer all-inclusive packages covering the procedure, accommodation, and airport transfers. Prices start from €1,500.",
  "sources": [
    {
      "content": "We offer all-inclusive packages...",
      "source": "docs/sample_faq.txt"
    }
  ],
  "language": "en",
  "session_id": "user_123"
}
```

### GET `/health`
```json
{ "status": "ok", "service": "quite-scale-rag-demo" }
```

---

## Docker Deployment

```bash
docker build -t quite-scale-rag .
docker run -p 8000:8000 --env-file .env quite-scale-rag
```

---

## Customization

| What to change | Where |
|---|---|
| Your business documents | Drop `.txt` files into `/docs/` |
| Supported languages | `app/models/chat.py` → `language` field pattern |
| LLM model / temperature | `app/services/rag_service.py` → `ChatOpenAI(...)` |
| CORS origins | `.env` → `CORS_ORIGINS` |

---

## Real-World Applications

This system is the backend engine for:

1. **WhatsApp AI Receptionist** — integrated via Twilio API, handles inquiry triage, pricing questions, and appointment qualification 24/7
2. **Website Chat Widget** — embedded on clinic/hotel websites, answers visitor questions instantly
3. **Telegram Bot** — for MENA markets where Telegram is the primary B2B channel

---

## About

**Quite Scale AI** builds custom AI infrastructure and premium web systems for high-revenue service businesses in Istanbul and the MENA region.

- 🌐 [quite-scale.ai](https://quite-scale.ai) *(coming soon)*
- 💼 [LinkedIn](https://www.linkedin.com/in/muhammad-shaheer-rizwan-/)
- 🐦 [X / Twitter](https://x.com/quietscaleai)

> *"You are losing wealthy international clients at 3 AM — not because your service is inferior, but because no one answered."*

---

## License

MIT — fork it, learn from it, build on it.
