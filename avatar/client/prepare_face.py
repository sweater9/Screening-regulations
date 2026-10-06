"""Crop a portrait to a square, face-only image (usage: prepare_face.py in.jpg out.png [size])."""
import sys
import cv2

src, dst = sys.argv[1], sys.argv[2]
size = int(sys.argv[3]) if len(sys.argv) > 3 else 512
img = cv2.imread(src)
if img is None:
    sys.exit(f"cannot read {src}")
cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces = cascade.detectMultiScale(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 1.1, 5)
if len(faces) == 0:
    sys.exit("no face found; use a frontal, well-lit portrait")
x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
side = int(max(w, h) * 1.8)  # margin so chin/hair are included
cx, cy = x + w // 2, y + h // 2
x0, y0 = max(0, cx - side // 2), max(0, cy - side // 2)
crop = img[y0:y0 + side, x0:x0 + side]
cv2.imwrite(dst, cv2.resize(crop, (size, size), interpolation=cv2.INTER_AREA))
print(f"wrote {dst}")
