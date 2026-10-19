# Provable.ai

A red-teaming and guardrail platform for LLM applications: attack your model with adversarial prompts, filter live traffic, and keep an auditable record of what failed.

## Status

Early development. The repository currently contains the product requirements and an empty FastAPI project skeleton. No endpoints, models, or attack logic are implemented yet, and there is no frontend code. Everything under [Planned modules](#planned-modules) is a specification, not working software.

## Planned modules

From the [PRD](./documentations/PRD.md) (v1.0, draft, frontend-first with a dense dark "HUD" design language):

| Module | Purpose |
| --- | --- |
| Mission Control | Dashboard with an overall trust score, a live log of audited prompts, a 24-hour hallucination heatmap, and a threat radar (PII leaks, toxicity, competitor mentions, hallucinations). |
| Attack Studio | Configure and run adversarial agents (for example jailbreak, SQL injection, PII extraction personas) with adjustable intensity and mutation count; side-by-side prompt diffs and tagging of responses as safe, leak, or hallucination. |
| Live Interceptor | Node-based editor for guardrail rules between user and LLM (PII scrubber, topic blocker, tone check, competitor filter), with a dry-run mode and an active-block mode. |
| Forensics | Per-interaction trace view: latency breakdown, retrieved context, and highlighting of response text that the context does not support. |
| Compliance Vault | Reports and policies for compliance reviewers, such as PDF reports and safety scores. |
| Settings | API keys and webhooks. |

The PRD recommends Next.js or SvelteKit, Tailwind CSS, shadcn/ui, and Recharts or VisX for the frontend.

## What exists today

- `pyproject.toml` with the backend dependency set (FastAPI, OpenAI SDK, Pydantic, pydantic-settings, python-dotenv, Uvicorn) and Python 3.12.
- Package skeleton under `app/` (`api/v1`, `core`, `models`, `schema`). All files there are empty. `app/api/v1/` has placeholder `agent.py` and `users.py`.
- `main.py` is a stub that prints a greeting. It does not create a FastAPI application.
- `documentations/PRD.md` and the lock file `uv.lock`.

Note: `documentations/PROJECT_STRUCTURE.md` and the files in `documentations/docs/` describe a different project (NeuraList) and are not specifications for Provable.ai.

## Tech stack

Backend: Python 3.12, FastAPI, Uvicorn, OpenAI Python SDK, Pydantic and pydantic-settings. Package management with [uv](https://docs.astral.sh/uv/).

## Quickstart

```bash
git clone https://github.com/yuvraaj2002/Provable.ai.git
cd Provable.ai
uv sync
uv run python main.py        # prints a greeting; the API app does not exist yet
```

Once an ASGI app is added (for example `app = FastAPI()` in `main.py`), run it with:

```bash
uv run uvicorn main:app --reload
```

### Environment variables

The current code does not read any environment variables. `python-dotenv` and `pydantic-settings` are installed for upcoming configuration. The OpenAI SDK reads `OPENAI_API_KEY` by default, so expect to set it in a local `.env` (not committed) once LLM calls are added.

## Project structure

```
.
├── app/
│   ├── api/v1/          # route modules (placeholders: agent.py, users.py)
│   ├── core/            # config and shared logic (empty)
│   ├── models/          # data models (empty)
│   └── schema/          # request/response schemas (empty)
├── documentations/
│   ├── PRD.md           # product requirements
│   ├── PROJECT_STRUCTURE.md  # from another project (NeuraList)
│   └── docs/            # notes from another project (NeuraList)
├── main.py
├── pyproject.toml
└── uv.lock
```

## Documentation

- [Product Requirements Document](./documentations/PRD.md)
