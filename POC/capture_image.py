import cv2
import os
import threading

# Global variables
count = 0
capture = False
user_name = ""

def capture_callback():
    global capture
    capture = True
    threading.Timer(1, capture_callback).start()  # Schedule the next callback

def capture_images(user):
    global count
    global capture
    global user_name
    
    user_name = user
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    user_folder = f'/home/luky/playground/face_recognition_unlock/POC/face_data/{user_name}'
    os.makedirs(user_folder, exist_ok=True)

    # Start the timer callback
    capture_callback()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if capture:
            for (x, y, w, h) in faces:
                count += 1
                face = frame[y:y+h, x:x+w]
                cv2.imwrite(f'{user_folder}/face{count}.jpg', face)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            capture = False  # Reset capture flag

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 30:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    user_name = input("Enter the user's name: ")
    capture_images(user_name)
    exit()
