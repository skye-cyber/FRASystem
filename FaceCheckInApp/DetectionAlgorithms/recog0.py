import os
import pickle
from pathlib import Path
import cv2
import face_recognition
import numpy as np
from playsound import playsound
from .attendance_logger import A_LOGGER


class FaceMatch:
    def __init__(self):
        pass

    def match_faces(self, frame):
        try:
            played = False
            with open(os.path.join(Path(__file__).resolve().parent, "encodings.pickle"), "rb") as f:
                data = pickle.load(f)

            print("\033[35mBegin\033[0m")
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            recognized = False
            employee_name = None
            face_data = []

            if not face_encodings:
                print("\033[93mNo Faces Detected\033[0m")

            else:
                print("\033[35mFind faces\033[0m")

            for face_encoding, face_location in zip(face_encodings, face_locations):
                print("\033[35mFaces detected\033[0m")
                matches = face_recognition.compare_faces(data["encodings"], face_encoding)
                name = "Unknown"
                face_distances = face_recognition.face_distance(data["encodings"], face_encoding)
                best_match_index = np.argmin(face_distances)

                top, right, bottom, left = face_location

                if matches[best_match_index] and face_distances[best_match_index] < 0.4:
                    print("\033[32mFound a match\033[0m")
                    name = data["names"][best_match_index]
                    try:
                        pass
                        playsound(os.path.join(Path(__file__).resolve().parent, 'Confirm.mp3'))
                        playsound(os.path.join(Path(__file__).resolve().parent, 'TaskCompleted.mp3'))
                    except Exception as e:
                        print(f"Error playing sound: {e}")

                    log = A_LOGGER()
                    log.log_attendance(name)
                    log.export_xlsx()

                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                    recognized = True
                    employee_name = name
                else:
                    print("\033[31mNo match found\033[0m")
                    try:
                        pass
                        playsound(os.path.join(Path(__file__).resolve().parent, 'NegativeMatch.mp3'))
                    except Exception as e:
                        print(f"Error playing sound: {e}")
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, 'Unknown❌', (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                    if not played:
                        played = True

                face_data.append({
                    'top': top,
                    'right': right,
                    'bottom': bottom,
                    'left': left,
                    'recognized': recognized,
                    'name': name
                })

            return frame, recognized, employee_name, face_data

        except Exception as e:
            print(f"Error: {e}")
            return None, False, None, []


if __name__ == "__main__":
    init = FaceMatch()
    init.match_faces()

