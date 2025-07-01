**🛰️ Drone Model Tracking Using Stereo Vision**

This project implements a 3D drone tracking system using a stereo camera setup and computer vision techniques. The system reconstructs the 3D trajectory of a drone model in real-time based on depth information derived from a calibrated stereo rig.

**📍 Designed for indoor use with affordable hardware and open-source libraries (OpenCV, NumPy).**


**🎯 Project Objectives**

Calibrate a stereo vision system using a chessboard pattern.

Capture synchronized video from two cameras.

Compute disparity maps and reconstruct depth.

Detect and track a drone's position in 3D space.

Plot the real-time position of the drone based on disparity.


**🧪 System Assumptions**

Stereo calibration uses a 14×10 chessboard (13×9 internal corners) printed on A3 paper.

Tracking occurs indoors with constant lighting.

A marker or small drone model is used for testing.

Cameras are mounted on a rigid stereo frame with known baseline.


**🧰 Tools & Technologies**

🔧 Hardware

2× USB Quad-HD 2K webcams (F-A489 model)

A3 calibration chessboard

Lightweight quadcopter drone

💻 Software

Python

OpenCV – image capture, stereo matching, calibration

NumPy – numerical operations


**🖼️ Calibration Workflow**

![image](https://github.com/user-attachments/assets/bea68b14-f4af-40aa-9bf6-8f152d1d8c7b)
![image](https://github.com/user-attachments/assets/fc5b2436-17bb-44a4-b301-035a30a380cc)
![image](https://github.com/user-attachments/assets/2504c4ed-71ed-415c-b1cb-679e89619da9)

Detect chessboard corners in both camera views.

Capture valid stereo image pairs (SPACE) and save.

Perform:

Monocular calibration for each camera

Stereo calibration to compute rotation R and translation T

Apply image rectification to align stereo images.


**🧠 Depth Estimation & Drone Tracking**

Compute disparity maps using StereoSGBM algorithm (high accuracy).

Apply image rectification for better pixel alignment.

Use contour detection on disparity map to find drone location.

Plot and annotate 3D position of the drone.


**🏁 How to Run**

Connect both cameras.

Place and move chessboard in front of both views.

Run the calibration script:
python stereo_calibrate.py

Capture 10 valid chessboard pairs (press SPACE).

Run the tracking script:
python drone_tracking.py


**🔍 Sample Results**

Disparity maps showing depth variation
![image](https://github.com/user-attachments/assets/e879e29c-ee57-4547-a029-2a1609b10b8b)

Plotted position of drone in each frame
![image](https://github.com/user-attachments/assets/9f28aa7e-2cad-478b-a797-824c22f0ef41)
![image](https://github.com/user-attachments/assets/99f9c240-6fa3-484a-b9b8-fb7670cb4ff4)

Robust calibration using OpenCV’s reliable vision tools


**🧩 Possible Improvements**

Real-time visual tracking with Kalman filtering

Integration with drone control API

Web dashboard for 3D visualization

Outdoor calibration & tracking


**📄 License**

OpenCV is licensed for free commercial use.

This project is intended for educational and research purposes.
