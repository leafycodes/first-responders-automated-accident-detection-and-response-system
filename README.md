# First Responders: Automated Accident Detection & Response System - Mini Project for 6th Sem (FRMP6)

FRMP6 is a multi-functional security system integrating AI-based monitoring, real-time networking, cloud storage, and encryption to enhance surveillance and tracking capabilities.  

**This project is developed for research and academic purposes.**  

It utilizes **YOLOv8** for AI-based object detection and tracking. Additionally, the system **tracks the closest responder and hospital** for emergency response. The **cloud deployment is done using Google Colab**, though it is not included in this repository.  

## Project Structure
The project consists of four main components, each focusing on a critical aspect of the system:

### 1. AI/ML Component (`aiml/`)
This module powers AI-driven surveillance features such as object detection and face recognition.
- **`mainsec.py` & `img.py`** - Core AI scripts for security analysis.
- **`best.pt`** - Trained deep learning model for detection.
- **`fr/images/training/`** - Dataset used for training AI models.
- **`aiml_security.log`** - Logs AI-based security operations.
- **`encryption_key.key`** - Possibly used for securing AI-related data.

### 2. CCTV Monitoring (`cctv/`)
Responsible for real-time video surveillance using connected cameras.
- Manages live camera feeds and recording functionalities.
- Facilitates secure storage and streaming of video footage.

### 3. UI/UX (`uiux/`)
The user interface provides an interactive dashboard to monitor and manage security features.
- Contains HTML, CSS, PHP, and JavaScript files.
- Allows users to view CCTV feeds, access alerts, and control system settings.

### 4. GPS Tracking (`gps/`)
This component tracks the real-time location of assets or individuals.
- Provides location-based alerts and geofencing capabilities.
- Integrates with the UI for visual representation on a map.

## Prerequisite Technologies  
In addition to the dependencies listed in `requirements.txt`, the following technologies are essential for the project:  
- **Python** (for AI/ML and backend processing)  
- **YOLOv8** (for object detection and tracking)  
- **Flask / Django** (for backend services)  
- **OpenCV** (for image and video processing)  
- **Google Colab** (for cloud-based model training and execution)  
- **JavaScript, HTML, CSS, PHP** (for UI development)  
- **MySQL / Firebase** (for database and storage management)  

## Installation & Setup
1. Install dependencies from `requirements.txt`:
    ```sh
    pip install -r requirements.txt
    ```
2. Configure the environment as needed.
3. Run the respective scripts to start AI monitoring, video surveillance, UI, or GPS services.

## Contributors
This project was developed by a team of five members, with each contributor focusing on a specific module.  
Collaborators will be added to the repository soon. <br>
Collaborators: @AnaghDas, @shubhub29
