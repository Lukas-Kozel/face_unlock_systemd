import cv2
import os
import threading

# Global variable to keep track of capture count
count = 0
capture = False

def capture_callback():
    global capture
    capture = True
    threading.Timer(1, capture_callback).start()  # Schedule the next callback

def capture_images():
    global count
    global capture
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    os.makedirs('face_data', exist_ok=True)

    # Start the timer callback
    capture_callback()

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if capture:
            for (x, y, w, h) in faces:
                count += 1
                face = frame[y:y+h, x:x+w]
                cv2.imwrite(f'face_data/face{count}.jpg', face)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            capture = False  # Reset capture flag

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 30:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    capture_images()
