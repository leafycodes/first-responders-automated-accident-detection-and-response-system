import cv2
import time
from pathlib import Path

base_dir = Path(__file__).resolve().parent

video_path = base_dir / ".." / "cctv" / "feeder_videos" / "cam1_22032025_1_1718.mp4"
output_dir = base_dir / ".." / "aiml" / "images"

video_path = video_path.resolve()
output_dir = output_dir.resolve()

output_dir.mkdir(parents=True, exist_ok=True)

max_frames = 100
frame_skip = 3  
resize_dim = (1080, 500)

cap = cv2.VideoCapture(str(video_path))
cpt = 0
count = 0

while cpt < max_frames:
    ret, frame = cap.read()
    if not ret:
        break

    count += 1
    if count % frame_skip != 0:
        continue

    frame = cv2.resize(frame, resize_dim)
    cv2.imshow("Test Window", frame)

    output_path = output_dir / f"car_{cpt}.jpg"
    cv2.imwrite(str(output_path), frame)

    time.sleep(0.01)
    cpt += 1

    if cv2.waitKey(5) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()
