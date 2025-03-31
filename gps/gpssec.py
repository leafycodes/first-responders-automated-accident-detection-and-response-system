from flask import Flask, render_template, jsonify
import requests
import random
import threading
import webbrowser
import os
import json
import time
from pathlib import Path
from cryptography.fernet import Fernet


app = Flask(__name__, template_folder="templates")

base_dir = Path(__file__).resolve().parent

encryption_key_path = base_dir / "encryption_key.key"
accident_data_path = base_dir / "accident_data.json"

if not encryption_key_path.exists():
    raise FileNotFoundError("Encryption key not found! GPS script cannot decrypt data.")

with open(encryption_key_path, "rb") as key_file:
    key = key_file.read()
cipher = Fernet(key)

def get_accident_data():
    try:
        with open(accident_data_path, "rb") as f:
            encrypted_data = f.read()

        decrypted_data = cipher.decrypt(encrypted_data).decode() 
        data = json.loads(decrypted_data)

        if data.get("accident") and data.get("ip_address"):
            return data["ip_address"]
        else:
            return None
    except Exception as e:
        print("Error decrypting accident data:", e)
        return None

def get_location_from_ip(ip_address):
    try:
        response = requests.get(f"https://ipapi.co/{ip_address}/json/")
        data = response.json()

        if "latitude" in data and "longitude" in data:
            lat = float(data["latitude"])
            lon = float(data["longitude"])

            min_lat, max_lat = 20.23, 20.38
            min_lon, max_lon = 85.75, 85.92

            if not (min_lat <= lat <= max_lat and min_lon <= lon <= max_lon):
                print("⚠️ IP location outside Bhubaneswar, resetting to KIIT College.")
                lat, lon = 20.2961, 85.8245 

            print(f"📍 Accident Location: {lat}, {lon}") 
            return {"lat": lat, "lon": lon}

    except Exception as e:
        print("Error fetching IP location:", e)

    return {"lat": 20.2961, "lon": 85.8245}

def generate_responders(accident_lat, accident_lon):
    num_responders = random.randint(4, 10)  
    responders = []
    for _ in range(num_responders):
        offset_lat = random.uniform(-0.045, 0.045) 
        offset_lon = random.uniform(-0.045, 0.045)
        responders.append({"lat": accident_lat + offset_lat, "lon": accident_lon + offset_lon})
    return responders

def get_nearest_responder(accident_lat, accident_lon, responders):
    return min(responders, key=lambda r: (r['lat'] - accident_lat)**2 + (r['lon'] - accident_lon)**2)

HOSPITALS = [
    {"lat": 20.3082, "lon": 85.8254}, {"lat": 20.3165, "lon": 85.8190}, {"lat": 20.2993, "lon": 85.8334},
    {"lat": 20.3110, "lon": 85.8350}, {"lat": 20.3215, "lon": 85.8412}, {"lat": 20.2985, "lon": 85.8104},
    {"lat": 20.2954, "lon": 85.8181}, {"lat": 20.3193, "lon": 85.8127}, {"lat": 20.3229, "lon": 85.8293},
    {"lat": 20.3052, "lon": 85.8277}, {"lat": 20.3145, "lon": 85.8111}, {"lat": 20.2932, "lon": 85.8392},
    {"lat": 20.3298, "lon": 85.8143}, {"lat": 20.3325, "lon": 85.8321}, {"lat": 20.2981, "lon": 85.8249},
    {"lat": 20.3097, "lon": 85.8198}, {"lat": 20.3256, "lon": 85.8405}, {"lat": 20.3129, "lon": 85.8194},
    {"lat": 20.3086, "lon": 85.8302}, {"lat": 20.3152, "lon": 85.8283}, {"lat": 20.2967, "lon": 85.8199},
    {"lat": 20.2902, "lon": 85.8258}, {"lat": 20.3074, "lon": 85.8129}, {"lat": 20.3304, "lon": 85.8382},
    {"lat": 20.3355, "lon": 85.8224}, {"lat": 20.2945, "lon": 85.8373}, {"lat": 20.3118, "lon": 85.8252},
    {"lat": 20.3239, "lon": 85.8209}, {"lat": 20.3267, "lon": 85.8295}, {"lat": 20.3058, "lon": 85.8229}
]

def get_nearest_hospital(accident_lat, accident_lon):
    return min(HOSPITALS, key=lambda h: (h['lat'] - accident_lat)**2 + (h['lon'] - accident_lon)**2)

@app.route("/")
def index():
    return render_template("accident_response_simulation.html")

@app.route("/get_accident_data")
def get_accident_data_api():
    ip_address = get_accident_data()
    
    if not ip_address:
        return jsonify({"error": "No accident detected"}), 400

    accident_location = get_location_from_ip(ip_address)
    responders = generate_responders(accident_location["lat"], accident_location["lon"])
    nearest_responder = get_nearest_responder(accident_location["lat"], accident_location["lon"], responders)
    hospital = get_nearest_hospital(accident_location["lat"], accident_location["lon"])

    return jsonify({
        "accident": accident_location,
        "responders": responders,
        "nearest_responder": nearest_responder,
        "hospital": hospital
    })

def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")

def run_server():
    print("🚨 Accident detected! Starting GPS tracking system...")
    if not os.environ.get("WERKZEUG_RUN_MAIN"):  
        threading.Timer(1.5, open_browser).start()
    app.run(debug=True)

if __name__ == "__main__":
    while True:
        ip_address = get_accident_data()
        if ip_address:
            run_server()
            break  
        time.sleep(3)  
