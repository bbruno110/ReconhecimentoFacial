import face_recognition
import os
import cv2
import numpy as np
import requests
import zipfile

class FaceRecognition:
    def __init__(self):
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.face_confidence = [] 
        self.known_face_encodings = []
        self.known_face_names = []
        self.min_confidence = 0.58  # Defina o nível mínimo de confiança
        self.resolution = (320, 240)


        url = "https://face-door-back.onrender.com/download"
        response = requests.get(url)


        zip_path = 'arquivo.zip'
        with open(zip_path, 'wb') as f:
            f.write(response.content)


        if not os.path.exists('img'):
            os.makedirs('img')

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('img')

        if os.path.exists(zip_path):
            os.remove(zip_path)

        undefined_file_path = os.path.join('img', 'undefined.png')
        if os.path.exists(undefined_file_path):
            os.remove(undefined_file_path)
        for image in os.listdir('img/'):
            face_image = face_recognition.load_image_file(f'img/{image}')
            face_encoding = face_recognition.face_encodings(face_image)[0]
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(os.path.splitext(image)[0])

        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(3, self.resolution[0])
        self.video_capture.set(4, self.resolution[1])
        self.video_capture.set(cv2.CAP_PROP_FPS, 24)

    def run_recognition(self):
        while True:
            ret, frame = self.video_capture.read()
            self.face_locations = []
            self.face_encodings = []
            self.face_names = []
            self.face_confidence = []

            small_frame = cv2.resize(frame, (0, 0), fx=0.24, fy=0.24)
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = 'Desconhecido'
                confidence = 0

                if True in matches:
                    first_match_index = matches.index(True)
                    confidence = 1 - face_recognition.face_distance([self.known_face_encodings[first_match_index]], face_encoding)

                    if confidence >= self.min_confidence:
                        name = self.known_face_names[first_match_index]

                self.face_names.append(name)
                self.face_confidence.append(confidence)
                self.face_locations.append(face_location)

            for (top, right, bottom, left), name, confidence in zip(self.face_locations, self.face_names, self.face_confidence):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                if name != 'Desconhecido':
                    confidence = float(confidence)
                    if confidence >= 0.45:
                        rectangle_color = (0, 255, 0)
                        
                    else:
                        rectangle_color = (0, 0, 255)

                    text = f'{name} ({confidence:.2f})'
                else:
                    rectangle_color = (0, 0, 255)
                    text = f'{name}'

                cv2.rectangle(frame, (left, top), (right, bottom), rectangle_color, 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), rectangle_color, -1)
                cv2.putText(frame, text, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
            cv2.imshow('frame', frame)

            if cv2.waitKey(1) == ord('q'):
                break

        self.video_capture.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()
