import cv2
import numpy as np
import os

# ========== CONFIGURATION ==========
camera_left_id = 1
camera_right_id = 2
chessboard_size = (20, 13)        # 21x14 squares → 20x13 inner corners
square_size = 0.02                # meters
save_dir = "calib_images"
max_pairs = 10

# Create folder for saving images
os.makedirs(save_dir, exist_ok=True)

# ========== OBJECT POINTS SETUP ==========
objp = np.zeros((chessboard_size[0]*chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
objp *= square_size

# ========== OPEN CAMERAS ==========
capL = cv2.VideoCapture(camera_left_id) 
capR = cv2.VideoCapture(camera_right_id)

if not capL.isOpened() or not capR.isOpened():
    print("Cannot open one or both cameras.")
    exit()

# ========== CAPTURE & DETECT LOOP ==========
print(" Press SPACE to capture a valid stereo pair (chessboard visible in both views). ESC to finish.")

objpoints = []
imgpoints_left = []
imgpoints_right = []
image_size = None
pair_index = 0

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

while True:
    retL, frameL = capL.read()
    retR, frameR = capR.read()
    if not retL or not retR:
        print("Frame capture failed.")
        break

    grayL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)
    grayR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)

    retL, cornersL = cv2.findChessboardCorners(grayL, chessboard_size, None)
    retR, cornersR = cv2.findChessboardCorners(grayR, chessboard_size, None)

    displayL = frameL.copy()
    displayR = frameR.copy()

    if retL:
        cornersL = cv2.cornerSubPix(grayL, cornersL, (11, 11), (-1, -1), criteria)
        cv2.drawChessboardCorners(displayL, chessboard_size, cornersL, retL)

    if retR:
        cornersR = cv2.cornerSubPix(grayR, cornersR, (11, 11), (-1, -1), criteria)
        cv2.drawChessboardCorners(displayR, chessboard_size, cornersR, retR)

    preview = cv2.hconcat([displayL, displayR])
    cv2.imshow("Stereo Chessboard Detection", preview)

    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break
    elif key == 32 and retL and retR:  # SPACE and valid corners
        print(f"Captured pair {pair_index}")
        objpoints.append(objp)
        imgpoints_left.append(cornersL)
        imgpoints_right.append(cornersR)
        image_size = grayL.shape[::-1]

        # Save raw images
        cv2.imwrite(os.path.join(save_dir, f"left{pair_index:02d}.jpg"), frameL)
        cv2.imwrite(os.path.join(save_dir, f"right{pair_index:02d}.jpg"), frameR)
        pair_index += 1

        if pair_index >= max_pairs:
            print(" Reached max pairs.")
            break

# ========== RELEASE CAMERAS ==========
capL.release()
capR.release()
cv2.destroyAllWindows()

# ========== CALIBRATION ==========
if len(objpoints) < 5: 
    print("Not enough valid pairs for calibration.")
    exit()

print(" Calibrating cameras...")

# Calibrate single cameras
retL, mtxL, distL, _, _ = cv2.calibrateCamera(objpoints, imgpoints_left, image_size, None, None)
retR, mtxR, distR, _, _ = cv2.calibrateCamera(objpoints, imgpoints_right, image_size, None, None)

# Stereo calibration
flags = cv2.CALIB_FIX_INTRINSIC
ret, mtxL, distL, mtxR, distR, R, T, E, F = cv2.stereoCalibrate(
    objpoints, imgpoints_left, imgpoints_right,
    mtxL, distL, mtxR, distR,
    image_size, criteria=criteria, flags=flags)

# Save results
np.savez("stereo_calibration.npz",
         mtxL=mtxL, distL=distL,
         mtxR=mtxR, distR=distR,
         R=R, T=T, E=E, F=F,
         image_size=image_size)

print(" Stereo calibration complete.")
print(" Calibration saved to 'stereo_calibration.npz'")
print(" Rotation:\n", R)
print("Translation:\n", T)
