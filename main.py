from io import BytesIO
import json
import re
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
    # print(image)
    # print(face_encoding)
    if isinstance(image, np.ndarray):
        pass
    else:
        return None
    
    try:
        print('try')

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

        print(face_encoding)
        if isinstance(face_encoding, np.ndarray):
            face_encoding = face_encoding.tolist()
            return face_encoding
        else:
            print(' face enc none')
            return None
    except:
        print("error")
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



def to_nparray(image):
    is_base64 = False
    try:
        decoded_bytes = base64.b64decode(image)
        is_base64 = True
    except (base64.binascii.Error, TypeError):
        is_base64 = False

    if is_base64:
        print('base64')
        image_bytes = base64.b64decode(image)
        image = Image.open(BytesIO(image_bytes))
        np_array = np.array(image)
        return np_array
    else:
        print('image')
        image = cv2.imread(image)
        if isinstance(image, np.ndarray):
            return image
        else:
            print('img none')
            return None
        
        # return image
        # if image:
        #     return image
        # else: 
        #     return None


# # import base64
# # import binascii

# # @jaseci_action(act_group=["cv"], allow_remote=True)
# # def convert_octet_stream_to_base64(octet_stream):
# #     base64_data = base64.b64encode(octet_stream).decode('utf-8')
# #     return base64_data



# # def convert_file_to_base64(file_path):
# #     with open(file_path, 'rb') as file:
# #         file_content = file.read()
# #         base64_data = base64.b64encode(file_content).decode('utf-8')
# #         # print(base64_data)
# #         ss = encode_face(base64_data)
# #         print(ss)

# #         return base64_data
    
# # qq = convert_file_to_base64("./zz2.json")


# # with open("./zz2.json", "r") as image_data:
# #     data = json.load(image_data)

# #     # data = "your_string"
# #     encoded = binascii.b2a_base64(data.encode(), newline=False)

# #     data = convert_octet_stream_to_base64(encoded)
# #     print(data)
# #     # print(encoded)
# #     # base64_string = data["image"][0]
# #     # print(base64_string)



# # # Example usage

base64_string = ""
with open("./ztest6.json", "r") as image_data:
# with open("./ztest3.json", "r") as image_data:
# with open("./ztest7.json", "r") as image_data:
    data = json.load(image_data)
    base64_string = data["image"][0]
    # print(base64_string)


# # ss = to_nparray(base64_string)
ss = encode_face(base64_string)
# ss = encode_face("mine.jpeg")
# ss = encode_face("war.jpeg")
# ss = encode_face("my.jpg") none
# ss = encode_face("new.png")
# ss = encode_face("bar.jpeg")
# ss = encode_face("far.jpeg")
# ss = encode_face("face.png")
print(ss)

# # # # encode = []
# ss = encode_face("my.jpg")
# # # ss = encode_face("face.png")
# print(ss)



# # compare_face_encodings()

# # import magic


# # file_path = "/zz2.octet-stream"  # Replace with the path to your file


# # file_type = magic.from_file(file_path, mime=True)

# # print("File type:", file_type)
