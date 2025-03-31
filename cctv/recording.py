import cv2
import time
import os
import requests
from datetime import datetime
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feeder_videos")

os.makedirs(output_folder, exist_ok=True)

droidcam_urls = {"cam1": "http:<your_wlan_ip>/video"}

ip_file = os.path.join(output_folder, "source_ip.txt")
if not os.path.exists(ip_file):
    try:
        public_ip = requests.get("https://api64.ipify.org?format=text", timeout=5).text.strip()
        with open(ip_file, "w") as file:
            file.write(public_ip)
        print(f"Public IP saved in {ip_file}: {public_ip}")
    except requests.RequestException:
        print("Failed to fetch public IP. Skipping...")

def get_next_serial():
    existing_files = os.listdir(output_folder)
    serial_numbers = []

    for file in existing_files:
        parts = file.split("_")
        if len(parts) >= 3 and parts[1].isdigit() and parts[2].isdigit():
            try:
                serial_numbers.append(int(parts[2]))
            except ValueError:
                continue

    return max(serial_numbers, default=0) + 1

def record_snippets(cam_id):
    url = droidcam_urls.get(cam_id)
    if not url:
        print(f"Camera {cam_id} URL is missing.")
        return

    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        print(f"Failed to open camera {cam_id}. Check the URL.")
        return

    print(f"Recording started for {cam_id}...")

    while True:
        now = datetime.now()
        date_str = now.strftime("%d%m%Y") 
        time_str = now.strftime("%H%M")   
        serial_number = get_next_serial()  

        snippet_filename = os.path.join(output_folder, f"{cam_id}_{date_str}_{serial_number}_{time_str}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(snippet_filename, fourcc, 20.0, (640, 480))

        start_time = time.time()
        while time.time() - start_time < 10:  
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)

        out.release()
        print(f"Saved {snippet_filename}")

@app.route("/")
def index():
    videos = sorted(os.listdir(output_folder))
    return render_template("index.html", videos=videos)

@app.route("/videos/<filename>")
def get_video(filename):
    return send_from_directory(output_folder, filename)

if __name__ == "__main__":
    from threading import Thread

    record_thread = Thread(target=record_snippets, args=("cam1",), daemon=True)
    record_thread.start()

    app.run(host="0.0.0.0", port=5000, debug=True)
