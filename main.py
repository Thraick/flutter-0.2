from io import BytesIO
import json
from PIL import Image
import base64
import face_recognition
import numpy as np
from imutils import face_utils
import dlib
import cv2
from jaseci.jsorc.live_actions import jaseci_action


@jaseci_action(act_group=["cv"], allow_remote=True)
def encode_face(image):
    # initialize dlib's face detector (HOG-based) and the facial landmark predictor
    p = "shape_predictor_68_face_landmarks.dat"  # change
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(p)

    image = to_nparray(image)
    # print(face_encoding)
    if isinstance(image, np.ndarray):
        pass
    else:
        return None

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    rects = detector(gray, 0)
    face_encoding = None
    

    # Loop over the face detections
    for rect in rects:
        # Determine the facial landmarks for the face region and convert them to a NumPy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # Extract the face ROI, encode it as a vector, and recognize the face
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        face_encodings = face_recognition.face_encodings(
            image, [(y, x + w, y + h, x)])
        if len(face_encodings) == 0:
            continue
        face_encoding = face_encodings[0]

    # print(face_encoding)
    if isinstance(face_encoding, np.ndarray):
        face_encoding = face_encoding.tolist()
        return face_encoding
    else:
        return None


@jaseci_action(act_group=["cv"], allow_remote=True)
def compare_face_encodings(face_encoding_list, id_list, face_encoding):
    face_encoding_list = np.array(face_encoding_list)

    face_distances = face_recognition.face_distance(
        face_encoding_list, face_encoding)
    if len(face_distances) > 0 and np.min(face_distances) < 0.6:
        match_index = np.argmin(face_distances)
        face_id = id_list[match_index]

        return face_id


# @jaseci_action(act_group=["cv"], allow_remote=True)
def to_nparray(image):
    is_base64 = False
    try:
        decoded_bytes = base64.b64decode(image)
        is_base64 = True
    except (base64.binascii.Error, TypeError):
        is_base64 = False

    if is_base64:
        image_bytes = base64.b64decode(image)
        image = Image.open(BytesIO(image_bytes))
        np_array = np.array(image)
        return np_array
    else:
        image = cv2.imread(image)
        if image:
            return image
        else: 
            return None






# # Example usage

# base64_string = ""
# with open("./ztest3.json", "r") as image_data:
#     data = json.load(image_data)
#     base64_string = data["image"][0]
#     # print(base64_string)


# ss = encode_face(base64_string)
# # ss = encode_face("tring")

# # # # encode = []
# # ss = encode_face("1111.png")
# # # ss = encode_face("face.png")
# print(ss)



# compare_face_encodings()

