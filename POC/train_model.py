import face_recognition
import os
import numpy as np

def train_model():
    known_faces = []
    known_names = []

    # Iterate through each user's directory in 'face_data'
    for user_name in os.listdir('/home/luky/playground/face_recognition_unlock/POC/face_data'):
        user_folder = os.path.join('/home/luky/playground/face_recognition_unlock/POC/face_data', user_name)
        
        if os.path.isdir(user_folder):
            for filename in os.listdir(user_folder):
                if filename.endswith('.jpg'):
                    image_path = os.path.join(user_folder, filename)
                    image = face_recognition.load_image_file(image_path)
                    encodings = face_recognition.face_encodings(image)
                    if encodings:  # Check if any face encodings are found
                        encoding = encodings[0]
                        known_faces.append(encoding)
                        known_names.append(user_name)  # Append the user name

    if known_faces:
        np.save('known_faces.npy', known_faces)
        np.save('known_names.npy', known_names)
        print(f"Training complete. Encoded {len(known_faces)} faces.")
    else:
        print("No faces were found in the training images. Please capture clear images with visible faces.")

if __name__ == '__main__':
    train_model()
