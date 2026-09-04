# CMPE 272 HW2: GitHub Issues REST API & Webhook Service

Author: Oleg Mrynskyi (CMPE 272 - Enterprise Software Platforms)

FastAPI service that wraps the GitHub REST API for Issues on a single repo. Has an OpenAPI 3.1 contract, HMAC-verified webhooks with SQLite dedupe, a pytest suite (>80% coverage), and a Dockerfile.

## Routes

Base URL: `http://localhost:${PORT}` (default `http://localhost:8000`)

1. `POST /issues` - create issue, returns `201` + `Location: /issues/{number}`
2. `GET /issues` - list issues (`state`, `labels`, `page`, `per_page` <= 100), forwards `Link` header, supports conditional GET via `ETag`/`If-None-Match`
3. `GET /issues/{number}` - get a single issue (`200` / `404`)
4. `PATCH /issues/{number}` - update title/body/state
5. `POST /issues/{number}/comments` - add a comment (`201`)
6. `POST /webhook` - GitHub webhook receiver, HMAC SHA-256 verified, dedupes by delivery id, `204` ACK
7. `GET /events` - recent processed webhook deliveries
8. `GET /healthz` - health check

## Setup

Copy `.env.example` to `.env` and fill in:

```bash
GITHUB_TOKEN=github_pat_xxxx      # fine-grained PAT with "Issues: Read and Write"
GITHUB_OWNER=your-github-username
GITHUB_REPO=cmpe272-issues-test   # a repo you control, dedicated for testing
WEBHOOK_SECRET=your_shared_secret # used for the webhook HMAC
PORT=8000
```

## Running it

Non-Docker:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Swagger docs at `http://localhost:8000/docs`.

Docker:
```bash
docker build -t hw2-issues-service .
docker run --env-file .env -p 8000:8000 hw2-issues-service
```

Docker Compose:
```bash
docker-compose up --build
```

## API examples

Create issue:
```bash
curl -i -X POST http://localhost:8000/issues \
  -H "Content-Type: application/json" \
  -d '{"title": "Bug in login flow", "body": "OAuth callback times out", "labels": ["bug", "auth"]}'
```

List issues:
```bash
curl -i "http://localhost:8000/issues?state=open&page=1&per_page=10"
```

Get one issue:
```bash
curl -i http://localhost:8000/issues/1
```

Update / close an issue:
```bash
curl -i -X PATCH http://localhost:8000/issues/1 \
  -H "Content-Type: application/json" \
  -d '{"state": "closed"}'
```

Add a comment:
```bash
curl -i -X POST http://localhost:8000/issues/1/comments \
  -H "Content-Type: application/json" \
  -d '{"body": "Issue resolved in v1.0.1"}'
```

Trigger a webhook manually (signature has to match `WEBHOOK_SECRET`):
```bash
# echo -n '{"action":"opened"}' | openssl dgst -sha256 -hmac "$WEBHOOK_SECRET"
curl -i -X POST http://localhost:8000/webhook \
  -H "X-GitHub-Event: issues" \
  -H "X-GitHub-Delivery: delivery-guid-100" \
  -H "X-Hub-Signature-256: sha256=COMPUTED_HEX" \
  -d '{"action":"opened","issue":{"number":1}}'
```

List recent events:
```bash
curl -i http://localhost:8000/events
```

## Webhook setup + redelivery

1. Tunnel your local port with ngrok (or smee): `ngrok http 8000`
2. In the GitHub repo, go to Settings -> Webhooks -> Add webhook
   - Payload URL: `https://<your-ngrok-subdomain>.ngrok-free.app/webhook`
   - Content type: `application/json`
   - Secret: same value as `WEBHOOK_SECRET`
   - Events: Issues, Issue comments
3. To redeliver: Settings -> Webhooks -> [webhook] -> Recent Deliveries -> Redeliver. Should come back `204`, and a repeat delivery with the same id gets deduped instead of double-processed.

## Tests

```bash
pytest --cov=app --cov-report=term-missing tests/
```
17 tests, ~80% line coverage.

## Other files

- `openapi.yaml` - OpenAPI 3.1 contract, generated from the FastAPI app via `scripts/export_openapi.py`
- `HW2_Submission.docx` - write-up with screenshots
- `postman_collection.json` - Postman collection for the routes above
