# main_fallback.py 
import cv2, os, time
from deepface import DeepFace

def find_camera_index():
    for backend in (cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY):
        try:
            for idx in range(3):
                cap = cv2.VideoCapture(idx, backend)
                time.sleep(0.05)
                if cap.isOpened():
                    cap.release()
                    return idx, backend
                cap.release()
        except Exception:
            pass
    return None, None

idx, backend = find_camera_index()
if idx is None:
    print("No camera available. Falling back to image mode.")
    img_path = r"C:\Users\advai\Pictures\face.jpg"
    if not os.path.exists(img_path):
        raise SystemExit("No camera and no test image found. Put an image at " + img_path)
    img = cv2.imread(img_path)
    print("Analyzing image:", img_path)
    print(DeepFace.analyze(img, actions=['emotion'], enforce_detection=False))
else:
    print("Using camera index", idx, "backend", backend)
    cap = cv2.VideoCapture(idx, backend)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame read failed.")
            break
        try:
            res = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            dom = res[0]['dominant_emotion'] if isinstance(res, list) else res.get('dominant_emotion')
            cv2.putText(frame, f"Emotion: {dom}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0),2)
        except Exception as e:
            cv2.putText(frame, "Analyzing...", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255),2)
        cv2.imshow("Demo", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
