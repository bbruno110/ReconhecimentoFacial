import face_recognition
import os
import cv2
import numpy as np


class FaceRecognition:
    def __init__(self):
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.face_confidence = []  # Adicionado para armazenar os níveis de confiança
        self.known_face_encodings = []
        self.known_face_names = []
        self.min_confidence = 0.58  # Defina o nível mínimo de confiança
        self.resolution = (320, 240)

        # Carregue as imagens de rostos conhecidos
        for image in os.listdir('img/'):
            face_image = face_recognition.load_image_file(f'img/{image}')
            face_encoding = face_recognition.face_encodings(face_image)[0]
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(os.path.splitext(image)[0])  # Remova a extensão

        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(3, self.resolution[0])  # Largura
        self.video_capture.set(4, self.resolution[1])  # Altura
        self.video_capture.set(cv2.CAP_PROP_FPS, 24)

    def run_recognition(self):
        while True:
            ret, frame = self.video_capture.read()

            self.face_locations = []
            self.face_encodings = []
            self.face_names = []
            self.face_confidence = []  # Limpe a lista de níveis de confiança

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
                    confidence = float(confidence)  # Converter confiança para float
                    if confidence >= 0.58:
                        rectangle_color = (0, 255, 0)  # Verde para correspondências
                    else:
                        rectangle_color = (0, 0, 255)  # Vermelho para confiança insuficiente

                    text = f'{name} ({confidence:.2f})'  # Exibe o nome e o nível de confiança
                else:
                    rectangle_color = (0, 0, 255)  # Vermelho para desconhecidos
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
