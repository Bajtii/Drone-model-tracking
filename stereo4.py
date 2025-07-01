import cv2
import numpy as np
import os

# === Load calibration ===
calib_file = "stereo_calibration.npz"
if not os.path.exists(calib_file):
    raise FileNotFoundError("Calibration file not found.")
data = np.load(calib_file)

mtxL = data['mtxL']
distL = data['distL']
mtxR = data['mtxR']
distR = data['distR']
R = data['R']
T = data['T']
image_size = tuple(data['image_size'])

# === Capture from cameras ===
capL = cv2.VideoCapture(1)
capR = cv2.VideoCapture(2)

retL, frameL = capL.read()
retR, frameR = capR.read()

capL.release()
capR.release()

if not retL or not retR:
    raise RuntimeError("Could not read images from both cameras")

# === Resize to match calibration size ===
if frameL.shape[1::-1] != image_size:
    frameL = cv2.resize(frameL, image_size)
    frameR = cv2.resize(frameR, image_size)
    
# === Convert to grayscale ===
grayL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)
grayR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)

# === Stereo Rectify ===
R1, R2, P1, P2, Q, _, _ = cv2.stereoRectify(
    mtxL, distL, mtxR, distR, image_size, R, T, flags=cv2.CALIB_ZERO_DISPARITY, alpha=0)

mapL1, mapL2 = cv2.initUndistortRectifyMap(mtxL, distL, R1, P1, image_size, cv2.CV_16SC2)
mapR1, mapR2 = cv2.initUndistortRectifyMap(mtxR, distR, R2, P2, image_size, cv2.CV_16SC2)

rectL = cv2.remap(grayL, mapL1, mapL2, cv2.INTER_LINEAR)
rectR = cv2.remap(grayR, mapR1, mapR2, cv2.INTER_LINEAR)

# === Stereo Matching ===
stereo = cv2.StereoSGBM_create(
    minDisparity=0,
    numDisparities=16 * 8,
    blockSize=9,
    P1=8 * 3 * 9**2,
    P2=32 * 3 * 9**2,
    disp12MaxDiff=1,
    uniquenessRatio=10,
    speckleWindowSize=100,
    speckleRange=2,
    preFilterCap=31,
    mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
)
disparity = stereo.compute(rectL, rectR).astype(np.float32) / 16.0

# === Normalize for display ===
disp_vis = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX)
disp_vis = np.uint8(disp_vis)

# === Detect object based on disparity threshold ===
_, thresh = cv2.threshold(disp_vis, 64, 255, cv2.THRESH_BINARY)  # Tune threshold
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

object_center = None
if contours:
    largest_contour = max(contours, key=cv2.contourArea)
    M = cv2.moments(largest_contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        object_center = (cx, cy)

        # Reproject to 3D
        points_3d = cv2.reprojectImageTo3D(disparity, Q)
        point_3d = points_3d[cy, cx]
        X, Y, Z = point_3d
        print(f"Object 3D location: X={X:.2f}, Y={Y:.2f}, Z={Z:.2f}")

        # Visualize center on disparity map
        cv2.circle(disp_vis, (cx, cy), 5, (255, 255, 255), -1)
        cv2.putText(disp_vis, f"({X:.1f}, {Y:.1f}, {Z:.1f})", (cx+10, cy),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 1)

# === Prepare grid display ===
h, w = image_size
rectL_color = cv2.cvtColor(rectL, cv2.COLOR_GRAY2BGR)
rectR_color = cv2.cvtColor(rectR, cv2.COLOR_GRAY2BGR)

half_size = (w // 2, h // 2)
frameL_half = cv2.resize(frameL, half_size)
frameR_half = cv2.resize(frameR, half_size)
rectL_half = cv2.resize(rectL_color, half_size)
rectR_half = cv2.resize(rectR_color, half_size)

top = np.hstack((frameL_half, frameR_half))
bottom = np.hstack((rectL_half, rectR_half))
grid = np.vstack((top, bottom))

# === Display results ===
cv2.imshow("Stereo Camera Grid (Captured and Rectified)", grid)
cv2.imshow("Disparity Map with Object Detection", disp_vis)

cv2.waitKey(0)
cv2.destroyAllWindows()
