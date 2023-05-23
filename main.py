import json
import face_recognition
import numpy as np
from imutils import face_utils
import dlib
import cv2
from jaseci.jsorc.live_actions import jaseci_action

@jaseci_action(act_group=["cv"], allow_remote=True)
def encode_face(image):
    # initialize dlib's face detector (HOG-based) and the facial landmark predictor
    p = "shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(p)

    image = cv2.imread(image)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    rects = detector(gray, 0)

    # Loop over the face detections
    for rect in rects:
        # Determine the facial landmarks for the face region and convert them to a NumPy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # Extract the face ROI, encode it as a vector, and recognize the face
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        face_encodings = face_recognition.face_encodings(image, [(y, x + w, y + h, x)])
        if len(face_encodings) == 0:
            continue
        face_encoding = face_encodings[0]

    face_encoding = face_encoding.tolist()
    return face_encoding


@jaseci_action(act_group=["cv"], allow_remote=True)
def compare_face_encodings(face_encoding_list, id_list, face_encoding):
    face_encoding_list = np.array(face_encoding_list)
    
    face_distances = face_recognition.face_distance(face_encoding_list, face_encoding)
    if len(face_distances) > 0 and np.min(face_distances) < 0.6:
        match_index = np.argmin(face_distances)
        face_id = id_list[match_index]

        return face_id



# ss = encode_face('database/Jolie/img1.jpeg')
# ss2 = encode_face('database/Tharick/timg2.jpg')

# q = []
# q.append(ss)
# w= ['jolie']


# we = compare_face_encodings(q,w,ss2)
# print(we)