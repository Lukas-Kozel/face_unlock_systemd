import face_recognition
import os
import numpy as np

def train_model():
    known_faces = []
    known_names = []

    for filename in os.listdir('face_data'):
        if filename.endswith('.jpg'):
            image = face_recognition.load_image_file(f'face_data/{filename}')
            encodings = face_recognition.face_encodings(image)
            if encodings:  # Check if any face encodings are found
                encoding = encodings[0]
                known_faces.append(encoding)
                known_names.append('Luky')  # Replace 'Luky' with your actual name

    if known_faces:
        np.save('known_faces.npy', known_faces)
        np.save('known_names.npy', known_names)
    else:
        print("No faces were found in the training images. Please capture clear images with visible faces.")

if __name__ == '__main__':
    train_model()
