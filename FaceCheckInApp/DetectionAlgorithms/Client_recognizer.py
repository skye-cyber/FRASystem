import os
import pickle
import sys
import time
from pathlib import Path
import cv2
import dlib
import face_recognition
import numpy as np
from django.http import HttpResponse, StreamingHttpResponse
from playsound import playsound

from .attendance_logger import A_LOGGER


class FaceMatch:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        predictor_dir = Path(__file__).resolve().parent
        predictor_path = os.path.join(
            predictor_dir, "shape_predictor_68_face_landmarks.dat")
        self.predictor = dlib.shape_predictor(predictor_path)
        if not os.path.exists(predictor_path):
            print("\033[31mPredictor dat file not found\033[0m")
            return HttpResponse("Predictor file not found", status=500)
            sys.exit(1)

    def shape_to_np(self, shape, dtype="int"):
        coords = np.zeros((68, 2), dtype=dtype)
        for i in range(68):
            coords[i] = (shape.part(i).x, shape.part(i).y)
        return coords

    def align_face(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = self.detector(gray, 1)

        if len(rects) == 0:
            return None

        rect = rects[0]
        shape = self.predictor(gray, rect)
        shape = self.shape_to_np(shape)

        return self.apply_alignment(image, shape)

    def apply_alignment(self, image, landmarks):
        desired_left_eye = (0.35, 0.35)
        desired_face_width = 256
        desired_face_height = 256

        left_eye_pts = landmarks[36:42]
        right_eye_pts = landmarks[42:48]

        left_eye_center = left_eye_pts.mean(axis=0).astype("int")
        right_eye_center = right_eye_pts.mean(axis=0).astype("int")

        dY = right_eye_center[1] - left_eye_center[1]
        dX = right_eye_center[0] - left_eye_center[0]

        if dX == 0 or dY == 0:
            return None  # Cannot align if dX or dY is 0

        angle = np.degrees(np.arctan2(dY, dX)) - 180

        desired_right_eye_x = 1.0 - desired_left_eye[0]
        dist = np.sqrt((dX ** 2) + (dY ** 2))

        if dist == 0:
            return None  # Cannot align if distance is 0

        desired_dist = (desired_right_eye_x -
                        desired_left_eye[0]) * desired_face_width
        scale = desired_dist / dist

        eyes_center = ((left_eye_center[0] + right_eye_center[0]) // 2,
                       (left_eye_center[1] + right_eye_center[1]) // 2)

        eyes_center = (float(eyes_center[0]), float(eyes_center[1]))

        M = cv2.getRotationMatrix2D(eyes_center, angle, scale)
        tX = desired_face_width * 0.5
        tY = desired_face_height * desired_left_eye[1]
        M[0, 2] += (tX - eyes_center[0])
        M[1, 2] += (tY - eyes_center[1])

        (w, h) = (desired_face_width, desired_face_height)
        aligned_face = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC)

        return aligned_face

    def match_faces(self, frame):
        try:
            played = False
            with open(os.path.join(Path(__file__).resolve().parent, "encodings.pickle"), "rb") as f:
                data = pickle.load(f)

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(data["encodings"], face_encoding)
                name = "Unknown"
                face_distances = face_recognition.face_distance(data["encodings"], face_encoding)
                best_match_index = np.argmin(face_distances)

                top, right, bottom, left = face_location

                if matches[best_match_index] and face_distances[best_match_index] < 0.4:
                    name = data["names"][best_match_index]
                    print("\033[92mFace Recognized: {}\033[0m".format(name))
                    playsound(os.path.join(Path(__file__).resolve().parent, 'Confirm.mp3'))
                    print("\033[36mTask completed\033[0m")
                    playsound('Task_completed.mp3')

                    log = A_LOGGER()
                    log.log_attendance(name)
                    log.export_xlsx()

                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

                else:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, 'Unknown❌', (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                    print("\033[31mFace not recognized\033[0m")
                    if played is False:
                        playsound(os.path.join(Path(__file__).resolve().parent, "Nagative_match.mp3"))
                        played = True

            return frame

        except KeyboardInterrupt:
            print("Quit")
            return None

        except KeyError:
            print("KeyError")

        except Exception as e:
            print(f"\033[32m{e}\033[0m")
            # return HttpResponse("Error occurred", status=500)
            return None


if __name__ == "__main__":
    init = FaceMatch()
    init.match_faces()
