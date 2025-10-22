import io
from fastapi import FastAPI, UploadFile, HTTPException
from app.recog import extract_embeddings, find_match
from app.store import insert_face, load_all
from app.liveness import basic_antispoof
from app.schemas import EnrollResp, IdentifyResp
from app import add_cors

app = FastAPI(title="Face Attendance API", version="1.0.0")
add_cors(app)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/enroll", response_model=EnrollResp)
async def enroll(label: str, file: UploadFile):
    img = await file.read()
    if not basic_antispoof(img):
        raise HTTPException(400, "failed liveness checks")
    embs = extract_embeddings(img)
    if not embs:
        raise HTTPException(400, "no face detected")
    for e in embs:
        insert_face(label, e, {"filename": file.filename})
    return {"enrolled": len(embs)}

@app.post("/identify", response_model=IdentifyResp)
async def identify(file: UploadFile, tau: float = 0.6):
    img = await file.read()
    if not basic_antispoof(img):
        raise HTTPException(400, "failed liveness checks")
    embs = extract_embeddings(img)
    if not embs:
        raise HTTPException(400, "no face detected")
    db_embs, labels = load_all()
    label, dist = find_match(embs[0], db_embs, labels, tau=tau)
    return {"label": label, "distance": dist}
