# 🛰️ Drone Model Tracking Using Stereo Vision

This project implements a **real-time 3D drone tracking system** using a stereo camera setup and classical computer vision techniques. The system reconstructs the drone’s spatial trajectory based on depth information derived from a **calibrated stereo rig**.

> 📍 Optimized for indoor environments using affordable webcams and open-source libraries (OpenCV, NumPy).

---

## 🎯 Objectives

- ✅ Calibrate a stereo vision system using a printed chessboard  
- ✅ Capture synchronized video streams from two webcams  
- ✅ Compute disparity maps and extract depth  
- ✅ Track a drone (or marker) in 3D space  
- ✅ Visualize its position on live plots  

---

## 🧠 Algorithm Description

The system follows a **two-phase pipeline**: **stereo calibration** and **3D tracking**.

### 🔧 Stereo Calibration

1. Detect chessboard corners in both left and right camera frames  
2. Capture valid stereo pairs using the `SPACE` key  
3. Perform:
   - Monocular calibration for each camera  
   - Stereo calibration to compute rotation matrix `R` and translation vector `T`  
4. Apply **image rectification** to align stereo images horizontally

📸 Example calibration steps:

<p align="center">
  <img src="https://github.com/user-attachments/assets/bea68b14-f4af-40aa-9bf6-8f152d1d8c7b" width="30%" />
  <img src="https://github.com/user-attachments/assets/fc5b2436-17bb-44a4-b301-035a30a380cc" width="30%" />
  <img src="https://github.com/user-attachments/assets/2504c4ed-71ed-415c-b1cb-679e89619da9" width="30%" />
</p>

---

### 📐 Depth Estimation & Drone Tracking

- Computes **disparity maps** using OpenCV’s `StereoSGBM` algorithm  
- Applies **rectification maps** for pixel correspondence  
- Uses **contour detection** or color-based filtering to localize the drone  
- Computes **3D coordinates** based on disparity and camera matrices  
- **Plots 3D trajectory** of the drone in real time using matplotlib

📊 Sample output:

<p align="center">
  <img src="https://github.com/user-attachments/assets/e879e29c-ee57-4547-a029-2a1609b10b8b" width="45%" />
  <img src="https://github.com/user-attachments/assets/99f9c240-6fa3-484a-b9b8-fb7670cb4ff4" width="45%" />
  <br/><br/>
  <img src="https://github.com/user-attachments/assets/9f28aa7e-2cad-478b-a797-824c22f0ef41" width="60%" />
</p>

---

## 🧪 System Assumptions

| Parameter             | Details                                   |
|----------------------|-------------------------------------------|
| Calibration pattern  | A3 chessboard, 14×10 (13×9 internal corners) |
| Cameras              | 2× USB 2K Quad-HD webcams (F-A489 model)  |
| Environment          | Indoor with stable lighting               |
| Target object        | Mini drone or colored marker              |
| Stereo baseline      | Rigid stereo rig with fixed spacing       |

---

## 🛠️ Tools & Technologies

### 🔧 Hardware

- 🖥️ 2× USB Quad-HD webcams (F-A489 model or similar)  
- 📏 A3 printed calibration chessboard  
- 🚁 Lightweight quadcopter drone or color marker  

### 💻 Software

- 🐍 Python 3.x  
- 📷 OpenCV – stereo vision, image processing, calibration  
- 🔢 NumPy – matrix and array operations  
- 📈 Matplotlib – 3D visualization of tracked points  

---

## 🚀 How to Run

1. **Connect both USB cameras** to your system  
2. **Calibrate stereo setup**:

```bash
python stereo_calibrate.py

## 🔍 Sample Results

- ✔️ Accurate disparity and depth reconstruction  
- ✔️ Stable 3D localization  
- ✔️ Live 3D visualization of drone path  

<p align="center">
  <img src="https://github.com/user-attachments/assets/9f28aa7e-2cad-478b-a797-824c22f0ef41" width="60%" />
</p>

---

## 🧩 Possible Improvements

| Feature                          | Status       |
|---------------------------------|--------------|
| Kalman filter for smoother tracking | 🚧 Planned   |
| Integration with drone flight API    | 🚧 Planned   |
| Web dashboard (Plotly / WebSocket)   | 🧪 Prototype |
| Outdoor calibration + tracking        | ❌ Not yet   |

---

## 📄 License

OpenCV is free for academic and commercial use.  
This project is released under an open **educational & research license**.
