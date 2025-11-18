import cv2

print("Scanning camera indexes...")

for index in range(20):   # check 0–9
    print("Scan complete.")
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print("Camera not found on index ",index)
