# Lucid

An autonomous, scheduled RAG-based pipeline that tracks the latest AI/ML research on GPU inference, LLM serving, and hardware acceleration — filters it against a personal interest profile, summarizes it for engineers (not analysts), and delivers it as a daily email digest. No manual intervention required.

Built solo, end-to-end: ingestion, LLM-based relevance filtering, summarization, vector storage, and automated delivery — running on a fully serverless, cost-minimal architecture.

<img width="1362" height="507" alt="image" src="https://github.com/user-attachments/assets/0cc7ba14-b567-40d5-ae39-bff7533ffe66" />


---

## Why this exists

Staying current with fast-moving AI/ML research (inference optimization, quantization, hardware acceleration) usually means relying on secondhand summaries from social media threads — slow, incomplete, and dependent on someone else's curation. This project automates that pipeline directly from the source: it pulls new arXiv papers daily, scores them against a defined interest profile, and only surfaces what's actually relevant — with a developer-facing explanation of *why it matters*, not just what the paper says.

---

## What it does

1. **Ingests** new papers daily from arXiv across configurable categories (`cs.LG`, `cs.CL`, `cs.AR`, `cs.DC`, etc.)
2. **Scores relevance** (0–10) against a custom interest profile using an LLM-based classifier — no keyword matching, actual semantic judgment
3. **Summarizes** papers that pass the threshold in a consistent, developer-facing format: what the paper proposes, and what it practically enables you to build or run differently
4. **Embeds and stores** each paper (via `BAAI/bge-large-en-v1.5`) in a persistent ChromaDB vector store, building a queryable research corpus over time
5. **Delivers** a formatted HTML digest email automatically — no dashboard to check, it just lands in your inbox
6. Runs **entirely on a schedule**, with zero manual triggering, via GitHub Actions

---

## Architecture

```
GitHub Actions (scheduled, daily)
        │
        ▼
Download vectorstore ← Azure Blob Storage (persistent, Cool tier)
        │
        ▼
┌─────────────────────────────────────────────┐
│  Ingestion → Relevance Gate → Summarization  │
│         → Vector Store (Chroma)              │
└─────────────────────────────────────────────┘
        │
        ├──► Upload updated vectorstore → Azure Blob Storage
        │
        └──► Email digest → recipients
```

### Design decisions worth calling out

- **Ephemeral compute, persistent storage** — GitHub Actions runners are stateless and destroyed after every run, so the vector store is synced to/from Azure Blob Storage (Cool tier) before and after each pipeline execution. This avoids paying for an always-on VM for a job that runs once a day for a few minutes — the same outcome as a persistent server, at a fraction of the cost.
- **Config → Manager → Component architecture** — every pipeline stage (ingestion, relevance scoring, summarization, storage) is driven by typed, immutable config objects (`@dataclass(frozen=True)`) built from a single `config.yaml`. No hardcoded parameters in component logic; every tunable value (thresholds, model names, chunk sizes) lives in one place.
- **Tiered retrieval design** — currently operating at "tier 1" (abstract-level embedding and summarization). The architecture is deliberately structured to extend to full-text chunk-level retrieval (tier 2) without restructuring the vector store schema, once the corpus and use case justify the added complexity.
- **Relevance gating before summarization** — every fetched paper is scored first; only papers clearing the threshold are summarized, avoiding wasted LLM calls on irrelevant content.

---

## Tech stack

| Layer | Technology |
|---|---|
| Ingestion | arXiv API |
| LLM (relevance + summarization) | Groq API (Llama 3.3 70B) |
| Embeddings | `BAAI/bge-large-en-v1.5` (local, GPU-accelerated) |
| Vector store | ChromaDB |
| Orchestration | LangChain |
| Persistent storage | Azure Blob Storage (Cool tier) |
| Scheduling / CI | GitHub Actions |
| Email delivery | Python `smtplib`, custom HTML template |
| Config management | YAML + typed dataclasses |

---

## Project structure

```
research-digest/
├── config/
│   └── config.yaml              # all tunable pipeline parameters
├── src/
│   ├── entity/                  # frozen dataclass config objects
│   ├── config/                  # ConfigurationManager
│   ├── components/              # ingestion, relevance gate, summarizer, vectorstore, email sender
│   ├── pipeline/                # orchestrates components in sequence
│   ├── utils/                   # shared helpers, Blob sync logic
│   └── api/
│       └── main.py              # entry point triggered by GitHub Actions
├── .github/workflows/
│   └── ingestion_schedule.yml   # daily cron trigger
├── email_template.html          # HTML email template
├── requirements.txt
└── setup.py
```

---

## Setup & local development

**1. Clone and install:**
```bash
git clone https://github.com/<your-username>/research-digest.git
cd research-digest
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
pip install -e .
```

**2. Environment variables** — create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key
EMAIL_PASSWORD=your_gmail_app_password
AZURE_STORAGE_CONNECTION_STRING=your_azure_blob_connection_string
```

**3. Configure** `config/config.yaml` — set your arXiv categories, interest profile, relevance threshold, and recipient email(s).

**4. Run manually:**
```bash
python src/api/main.py
```

---

## Automated deployment

The pipeline runs daily via a GitHub Actions scheduled workflow (`.github/workflows/ingestion_schedule.yml`), triggered independently of any local machine. Secrets (`GROQ_API_KEY`, `EMAIL_PASSWORD`, `AZURE_STORAGE_CONNECTION_STRING`) are stored as GitHub repository secrets, never committed to source.

To adjust the schedule, edit the `cron` expression in the workflow file (times are UTC).

---

## Known limitations & roadmap

- Currently operates at abstract-level retrieval (tier 1). Full-text chunked retrieval is architected for but not yet implemented.
- Single relevance-gate/summarization LLM call per paper; no batching yet — a planned optimization to reduce token usage on high-volume days.
- No cross-run deduplication yet — overlapping date windows across daily runs can occasionally reprocess the same paper.
- **Phase 2 (in progress):** a conversational RAG interface for querying the accumulated paper corpus directly — router-based retrieval (single-paper vs. cross-paper), session memory, and a chat UI.

---

## Author

Built by **Aryan Dhawan** — AI/ML engineer, currently a CS student at GLS University
