import face_recognition
import cv2
import numpy as np

def recognize_face():
    known_faces = np.load('/home/luky/playground/face_recognition_unlock/POC/known_faces.npy', allow_pickle=True)
    known_names = np.load('/home/luky/playground/face_recognition_unlock/POC/known_names.npy', allow_pickle=True)

    cap = cv2.VideoCapture(0)

    while True:
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
            print(name)
            
            # Corrected label assignment
            if name == 'Luky':
                label = 'Luky'
            elif name == 'Terka':
                label = 'Terezie'
            else:
                label = 'unknown'

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with the name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, label, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    recognize_face()
