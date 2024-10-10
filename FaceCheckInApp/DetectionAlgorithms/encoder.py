import os
# import numpy as np
import pickle
import sys

import face_recognition
# import cv2
from playsound import playsound


def encode_faces(dataset_path):
    known_encodings = []
    known_names = []
    image_count = 0

    try:

        names_show = False

        for root, dirs, files in os.walk(dataset_path):

            if names_show is False:
                print(f"\033[95mNames \033[92m{dirs}\033[0m")
                names_show = True

            for file in files:

                if file.lower().endswith(('.jpg', '.png', '.jpeg')):
                    print(f"\033[36mEncode -> {file}\033[0m")
                    image_path = os.path.join(root, file)
                    image = face_recognition.load_image_file(image_path)
                    face_encodings = face_recognition.face_encodings(image)

                    if len(face_encodings) > 0:
                        image_count += 1
                        known_encodings.append(face_encodings[0])
                        known_names.append(os.path.basename(root))

                    else:
                        print(
                            f"\033[31mNo face encodings found in the {image_path}\033[0m")

        # Save the encodings and names

        data = {"encodings": known_encodings, "names": known_names}
        with open("UserEncodings.pickle", "ab") as f:
            f.write(pickle.dumps(data))

        if image_count > 0:
            print(
                f"\033[36mEncoded [\033[33m{image_count}\033[36m] faces\033[0m")

        elif image_count < 1:
            print("\033[31mMade 0 encodings\033[0m")
            playsound("encoder_error.mp3")

    except KeyboardInterrupt:
        print("Quit")
        sys.exit(1)

    except KeyError:
        print("KeyError")

    except Exception as e:
        print(f"\033[32m{e}\033[0m")


if __name__ == "__main__":
    encode_faces()
