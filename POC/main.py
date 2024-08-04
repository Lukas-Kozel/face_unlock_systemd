import face_recognition
import cv2
import os
import numpy as np
import pyautogui
import time
import dbus
import logging
import subprocess

# Setup logging
logging.basicConfig(filename='/home/luky/playground/face_recognition_unlock/POC/systemd/logs/face_unlock.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

def is_screen_locked_and_not_saver():
    try:
        session_bus = dbus.SessionBus()
        screensaver = session_bus.get_object('org.gnome.ScreenSaver', '/org/gnome/ScreenSaver')
        iface = dbus.Interface(screensaver, 'org.gnome.ScreenSaver')
        is_locked = iface.GetActive()

        if is_locked:
            # Check if the screen is in DPMS (Display Power Management Signaling) off state
            dpms_state = subprocess.check_output("xset -q | grep 'Monitor is' | awk '{print $3}'", shell=True).decode('utf-8').strip()
            if dpms_state == 'Off':
                logging.info("Screen is locked but in saver mode (DPMS off).")
                return False
            else:
                logging.info("Screen is locked and not in saver mode.")
                return True
        else:
            return False
    except Exception as e:
        logging.error(f"Error checking screen lock and saver status: {e}")
        return False

def recognize_face():
    known_faces = np.load('/home/luky/playground/face_recognition_unlock/POC/known_faces.npy', allow_pickle=True)
    known_names = np.load('/home/luky/playground/face_recognition_unlock/POC/known_names.npy', allow_pickle=True)

    authorized_folder = '/home/luky/playground/face_recognition_unlock/POC/authorized'
    unauthorized_folder = '/home/luky/playground/face_recognition_unlock/POC/unauthorized'
    cap = cv2.VideoCapture(0)
    with open('/home/luky/playground/face_recognition_unlock/POC/pswd.txt', 'r') as file:
        password = file.readline().strip()

    os.makedirs(authorized_folder, exist_ok=True)
    os.makedirs(unauthorized_folder, exist_ok=True)
    
    while True:
        if is_screen_locked_and_not_saver():
            ret, frame = cap.read()
            rgb_frame = frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_faces, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_faces, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]

                label = 'Luky' if name == 'Luky' else 'Unknown'
                timestamp = time.strftime("%Y%m%d-%H%M%S")

                if label == 'Luky':
                    pyautogui.press('left')
                    pyautogui.typewrite(password)
                    pyautogui.press('enter')
                    cv2.imwrite(os.path.join(authorized_folder, f'authorized_{timestamp}.jpg'), frame)
                    logging.info(f"Authorized access by {label} at {timestamp}")
                    time.sleep(2)
                    cap.release()
                    return
                else:
                    cv2.imwrite(os.path.join(unauthorized_folder, f'unauthorized_{timestamp}.jpg'), frame)
                    logging.warning(f"Unauthorized access attempt by {label} at {timestamp}")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        time.sleep(1)  # Check every second

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    recognize_face()
