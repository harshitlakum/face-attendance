import io, cv2, numpy as np
from PIL import Image

def basic_antispoof(img_bytes: bytes) -> bool:
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    arr = np.array(img)
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    # Heuristic 1: excessive saturation (screen glare / white wash)
    if (gray > 250).mean() > 0.25:
        return False
    # Heuristic 2: low high-frequency variance (printed photo)
    lap = cv2.Laplacian(gray, cv2.CV_64F).var()
    if lap < 30:
        return False
    return True
