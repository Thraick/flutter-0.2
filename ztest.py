
# import json
# from deepface.commons import functions
# from deepface.extendedmodels import Age, Gender, Race, Emotion
# from deepface.basemodels import (
#     VGGFace,
#     OpenFace,
#     Facenet,
#     Facenet512,
#     FbDeepFace,
#     DeepID,
#     DlibWrapper,
#     ArcFace,
#     SFace,
# )
# import cv2
# import numpy as np

# import face_recognition


# from io import BytesIO
# from PIL import Image
# import base64
# import face_recognition
# import numpy as np
# import cv2
# from jaseci.jsorc.live_actions import jaseci_action


# # # embedding_objs = DeepFace.represent(img_path = "my.jpg")
# # embedding_objs = DeepFace.represent(img_path = "./face.png")
# # DeepFace.find
# # print(embedding_objs)


# # common dependencies

# # 3rd party dependencies

# # package dependencies


# def to_nparray(image):
#     # is_base64 = False
#     # try:
#     #     decoded_bytes = base64.b64decode(image)
#     #     is_base64 = True
#     # except (base64.binascii.Error, TypeError):
#     #     is_base64 = False

#     # if is_base64:
#     print('base64')
#     image_bytes = base64.b64decode(image)
#     image = Image.open(BytesIO(image_bytes))
#     np_array = np.array(image)
#     return np_array
#     # else:
#     #     print('image')
#     #     image = cv2.imread(image)
#     #     if isinstance(image, np.ndarray):
#     #         return image
#     #     else:
#     #         print('image none')
#     #         return None
    

# def build_model(model_name):
#     """
#     This function builds a deepface model
#     Parameters:
#             model_name (string): face recognition or facial attribute model
#                     VGG-Face, Facenet, OpenFace, DeepFace, DeepID for face recognition
#                     Age, Gender, Emotion, Race for facial attributes

#     Returns:
#             built deepface model
#     """

#     # singleton design pattern
#     global model_obj

#     models = {
#         "VGG-Face": VGGFace.loadModel,
#         "OpenFace": OpenFace.loadModel,
#         "Facenet": Facenet.loadModel,
#         "Facenet512": Facenet512.loadModel,
#         "DeepFace": FbDeepFace.loadModel,
#         "DeepID": DeepID.loadModel,
#         "Dlib": DlibWrapper.loadModel,
#         "ArcFace": ArcFace.loadModel,
#         "SFace": SFace.load_model,
#         "Emotion": Emotion.loadModel,
#         "Age": Age.loadModel,
#         "Gender": Gender.loadModel,
#         "Race": Race.loadModel,
#     }

#     if not "model_obj" in globals():
#         model_obj = {}

#     if not model_name in model_obj:
#         model = models.get(model_name)
#         if model:
#             model = model()
#             model_obj[model_name] = model
#         else:
#             raise ValueError(f"Invalid model_name passed - {model_name}")

#     return model_obj[model_name]




# @jaseci_action(act_group=["cv22"], allow_remote=True)
# def encode_face(
#     img_path,
#     model_name="Facenet",
#     enforce_detection=True,
#     detector_backend="opencv",
#     align=True,
#     normalization="base",
# ):
#     """
#     This function represents facial images as vectors. The function uses convolutional neural
#     networks models to generate vector embeddings.

#     Parameters:
#             img_path (string): exact image path. Alternatively, numpy array (BGR) or based64
#             encoded images could be passed. Source image can have many faces. Then, result will
#             be the size of number of faces appearing in the source image.

#             model_name (string): VGG-Face, Facenet, Facenet512, OpenFace, DeepFace, DeepID, Dlib,
#             ArcFace, SFace

#             enforce_detection (boolean): If no face could not be detected in an image, then this
#             function will return exception by default. Set this to False not to have this exception.
#             This might be convenient for low resolution images.

#             detector_backend (string): set face detector backend to opencv, retinaface, mtcnn, ssd,
#             dlib or mediapipe

#             align (boolean): alignment according to the eye positions.

#             normalization (string): normalize the input image before feeding to model

#     Returns:
#             Represent function returns a list of object with multidimensional vector (embedding).
#             The number of dimensions is changing based on the reference model.
#             E.g. FaceNet returns 128 dimensional vector; VGG-Face returns 2622 dimensional vector.
#     """
#     resp_objs = []

#     model = build_model(model_name)
#     img_path=to_nparray(img_path)

#     # ---------------------------------
#     # we have run pre-process in verification. so, this can be skipped if it is coming from verify.
#     target_size = functions.find_target_size(model_name=model_name)
#     try:
#         print('try')
#         if detector_backend != "skip":
#             img_objs = functions.extract_faces(
#                 img=img_path,
#                 target_size=target_size,
#                 detector_backend=detector_backend,
#                 grayscale=False,
#                 enforce_detection=enforce_detection,
#                 align=align,
#             )

#         else:  # skip
#             if isinstance(img_path, str):
#                 img = functions.load_image(img_path)
#             elif type(img_path).__module__ == np.__name__:
#                 img = img_path.copy()
#             else:
#                 raise ValueError(
#                     f"unexpected type for img_path - {type(img_path)}")
#             # --------------------------------
#             if len(img.shape) == 4:
#                 img = img[0]  # e.g. (1, 224, 224, 3) to (224, 224, 3)
#             if len(img.shape) == 3:
#                 img = cv2.resize(img, target_size)
#                 img = np.expand_dims(img, axis=0)
#             # --------------------------------
#             img_region = [0, 0, img.shape[1], img.shape[0]]
#             img_objs = [(img, img_region, 0)]
#         # ---------------------------------

#         for img, region, _ in img_objs:
#             # custom normalization
#             img = functions.normalize_input(img=img, normalization=normalization)

#             # represent
#             if "keras" in str(type(model)):
#                 # new tf versions show progress bar and it is annoying
#                 embedding = model.predict(img, verbose=0)[0].tolist()
#             else:
#                 # SFace and Dlib are not keras models and no verbose arguments
#                 embedding = model.predict(img)[0].tolist()

#             resp_obj = {}
#             resp_obj["embedding"] = embedding
#             # resp_obj["facial_area"] = region
#             resp_objs.append(resp_obj)

#         return resp_objs[0]["embedding"]
#     except:
#         print('except none')
#         return None

    


# # ss = encode_face('face.png', "Facenet")
# # ss1 = encode_face('my.jpg', "Facenet")
# # ss2 = encode_face('new.png', "Facenet")

# @jaseci_action(act_group=["cv22"], allow_remote=True)
# def compare_face_encodings(face_encoding_list, id_list, face_encoding):
#     face_encoding_list = np.array(face_encoding_list)

#     face_distances = face_recognition.face_distance(
#         face_encoding_list, face_encoding)
#     if len(face_distances) > 0 and np.min(face_distances) < 0.6:
#         match_index = np.argmin(face_distances)
#         face_id = id_list[match_index]

#         return face_id

# # sw = ['1','2']


# # qw = compare_face_encodings([ss, ss1], sw, ss1)
# # print(qw)


# # base64_string = cv2.imread('car.jpeg')
# # base64_string = cv2.imread('bar.jpeg')
# # base64_string = cv2.imread('war.jpeg')
# # base64_string = np.array(base64_string)

# base64_string = ""
# with open("./ztest1.json", "r") as image_data:
#     data = json.load(image_data)
#     base64_string = data["image"][0]
#     print(base64_string)

# ss = encode_face(base64_string, "Facenet")
# print(ss)





