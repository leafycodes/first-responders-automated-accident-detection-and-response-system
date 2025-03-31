import cv2
import pandas as pd
from ultralytics import YOLO
import cvzone
import json
import subprocess
import logging
import os
from pathlib import Path
from cryptography.fernet import Fernet

def setup_logging():
    log_file = Path(__file__).resolve().parent / "aiml_security.log"
    logging.basicConfig(
        filename=log_file, 
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

setup_logging()

base_dir = Path(__file__).resolve().parent

model_path = base_dir / ".." / "aiml" / "best.pt"
video_path = base_dir / ".." / "cctv" / "feeder_videos" / "cam1_22032025_1_1718.mp4"
class_list_path = base_dir / ".." / "aiml" / "coco1.txt"
ip_file_path = base_dir / ".." / "cctv" / "feeder_videos" / "source_ip.txt"
json_path = base_dir / ".." / "gps" / "accident_data.json"
gps_script_path = base_dir / ".." / "gps" / "gpssec.py"
encryption_key_path = base_dir / "encryption_key.key"

if not encryption_key_path.exists():
    key = Fernet.generate_key()
    with open(encryption_key_path, "wb") as key_file:
        key_file.write(key)

with open(encryption_key_path, "rb") as key_file:
    key = key_file.read()
cipher = Fernet(key)

for path in [model_path, video_path, class_list_path, ip_file_path, gps_script_path]:
    if not path.exists():
        logging.error(f"Missing critical file: {path}")
        raise FileNotFoundError(f"Security Alert: {path} not found!")
    if not os.access(path, os.R_OK):
        logging.error(f"Permission denied: {path}")
        raise PermissionError(f"Security Alert: No read access to {path}")

try:
    model = YOLO(str(model_path))
except Exception as e:
    logging.error(f"Error loading YOLO model: {e}")
    raise

try:
    with open(class_list_path, "r", encoding='utf-8') as my_file:
        class_list = my_file.read().split("\n")
except Exception as e:
    logging.error(f"Error reading class list: {e}")
    raise

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        logging.info(f"Mouse moved at: {x}, {y}")

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap = cv2.VideoCapture(str(video_path))
if not cap.isOpened():
    logging.error("Error: Unable to open video file.")
    raise RuntimeError("Security Alert: Video file access denied or corrupted.")

count = 0
accident_detected = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    count += 1
    if count % 3 != 0:
        continue

    frame = cv2.resize(frame, (1020, 500))
    results = model.predict(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")

    for index, row in px.iterrows():
        x1, y1, x2, y2 = map(int, row[:4])
        d = int(row[5])
        c = class_list[d]

        color = (0, 255, 0) 
        if c.lower() == "accident":
            color = (0, 0, 255) 
            accident_detected = True

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cvzone.putTextRect(frame, f'{c}', (x1, y1), 1, 1)

    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == 27: 
        break

cap.release()
cv2.destroyAllWindows()

if accident_detected:
    try:
        with open(ip_file_path, "r", encoding='utf-8') as file:
            ip_address = file.read().strip()
    except FileNotFoundError:
        logging.error("IP source file not found!")
        ip_address = "Unknown"
    except Exception as e:
        logging.error(f"Error reading IP file: {e}")
        ip_address = "Unknown"

    accident_data = {"accident": True, "ip_address": ip_address}
    json_data = json.dumps(accident_data).encode() 
    encrypted_data = cipher.encrypt(json_data) 

    with open(json_path, "wb") as json_file:  
        json_file.write(encrypted_data)

    logging.info("Accident detected! Encrypted data saved.")

    try:
        subprocess.run(["python", str(gps_script_path)], check=True)
        logging.info("GPS script executed successfully.")
    except subprocess.SubprocessError as e:
        logging.error(f"Error running GPS script: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")