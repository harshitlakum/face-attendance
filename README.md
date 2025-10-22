# Face Attendance API (FastAPI + `face_recognition`) — with Basic Anti-Spoofing

[![CI](https://github.com/harshitlakum/face-attendance/actions/workflows/ci.yml/badge.svg)](https://github.com/harshitlakum/face-attendance/actions/workflows/ci.yml)

> Minimal, production-shaped microservice that **enrolls** faces and **identifies** people from images using 128-D embeddings. Open-set verification via distance threshold **τ** (returns `unknown` when > τ) plus **basic anti-spoofing** to reject obvious screen/print attacks. Demo-ready, Dockerized, and tested.  
> **Disclaimer:** Not for security-critical use.

**Demo video (90s):** _add Loom link here_

---

## Features
- **Endpoints:** `/enroll` (store embeddings per label), `/identify` (label or `unknown` with distance), `/health`
- **Anti-spoofing:** glare + low-texture heuristics (Laplacian variance & saturation)
- **Storage:** SQLite embeddings (no raw images) — easy deletion per user
- **Ops:** pytest health test, Dockerfile, GitHub Actions CI

---

## Quickstart

### Local
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH="$(pwd)"   # macOS/tests convenience
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
````

### Docker

```bash
docker build -t face-attendance .
docker run -p 8000:8000 -v "$(pwd)"/data:/app/data face-attendance
```

### Health

```bash
curl -s http://localhost:8000/health
# {"status":"ok"}
```

---

## API

### `POST /enroll?label=<name>`

* **Body:** multipart `file=@image.jpg|png`
* **Response:** `{ "enrolled": N }`
* **Errors:** `400 "failed liveness checks"` · `400 "no face detected"`

### `POST /identify?tau=0.6`

* **Body:** multipart `file=@image.jpg|png`
* **Response:** `{ "label": "<name|unknown>", "distance": <float> }`
* **Note:** tune **τ** for your gallery (typical 0.50–0.65)

**Examples**

```bash
curl -F "file=@Harsh.JPG"  "http://localhost:8000/enroll?label=Harsh"
curl -F "file=@Harsh3.JPG" "http://localhost:8000/identify?tau=0.6"
```

---

## Demo (screens)

<p align="center">
  <img src="docs/ss-01-health.png" width="520" alt="Health OK">
</p>

**Enroll & Identify**

<p align="center">
  <img src="docs/ss-02-enroll.png" width="520" alt="Enroll">
  <br/>
  <img src="docs/ss-03-identify-harsh.png" width="520" alt="Identify Harsh">
  <br/>
  <img src="docs/ss-04-identify-pra.png" width="520" alt="Identify Pra">
</p>

**Anti-spoof (basic liveness)**

<p align="center">
  <img src="docs/ss-05-liveness-400.png" width="680" alt="Rejected spoof (HTTP 400)">
</p>

**State & Ops**

<p align="center">
  <img src="docs/ss-06-db.png" width="520" alt="SQLite rows & labels">
  <br/>
  <img src="docs/ss-07-openapi.png" width="680" alt="OpenAPI schema (excerpt)">
  <br/>
  <img src="docs/ss-08-docker.png" width="680" alt="Docker container running">
</p>

---

## Architecture (at a glance)

```
[Client] --multipart--> [FastAPI]
   └─ basic_antispoof()  → reject obvious spoofs
      face_recognition   → 128D embedding
      SQLite store       → embeddings only (no images)
      open-set match τ   → return label or 'unknown'
```

---

## Evaluation (minimal)

1. Small gallery (2–5 people, 2–3 images/person).
2. Sweep τ to balance TPR/FAR; report **TPR@FAR≈0.1%**.
3. Note p95 latency & liveness rejection rate on screen/print images.

---

## Privacy & Limits

* Stores **embeddings only**; delete per label to remove a user.
* Heuristic liveness (not production-grade).
* HOG detector weaker in low light/pose; use `"cnn"` if CUDA dlib available.

---

## Troubleshooting

* **`failed liveness checks`** → avoid screen photos; use real camera images, normal lighting.
* **`no face detected`** → face too small/profile/occluded; try a clearer frontal image.
* macOS HEIC → convert: `sips -s format jpeg input.HEIC --out fixed.jpg`
* Tests: `export PYTHONPATH="$(pwd)"; pytest -q`

---

## Roadmap

* `/list` & `/delete?label=` endpoints
* `/metrics` (uptime, counts, latency)
* Minimal HTML upload page under `/`
* Swap SQLite → **FAISS** for >10k embeddings

---

## What I built (Harshit Lakum)

* Designed **open-set** API (`/enroll`, `/identify`) with clean error handling
* Implemented **basic anti-spoofing** heuristics
* Built **SQLite** embedding store, **pytest** test, **Docker** packaging, **CI**
* Documented privacy, limits, and threshold tuning


