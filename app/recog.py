from typing import List, Tuple
import io, numpy as np, face_recognition as fr

def extract_embeddings(img_bytes: bytes) -> List[np.ndarray]:
    img = fr.load_image_file(io.BytesIO(img_bytes))
    boxes = fr.face_locations(img, model="hog")  # use "cnn" if CUDA dlib available
    encs = fr.face_encodings(img, boxes, num_jitters=1)
    return [np.asarray(e, dtype=np.float32) for e in encs]

def find_match(query: np.ndarray, db_embs: np.ndarray, labels: List[str], tau: float = 0.6) -> Tuple[str, float]:
    if db_embs.shape[0] == 0:
        return "unknown", 1.0
    dists = np.linalg.norm(db_embs - query[None, :], axis=1)
    i = int(np.argmin(dists))
    return (labels[i], float(dists[i])) if dists[i] <= tau else ("unknown", float(dists[i]))
