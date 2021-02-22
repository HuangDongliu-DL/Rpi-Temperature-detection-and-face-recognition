#coding=utf-8

import face_recognition
import os
import numpy as np

for i in os.listdir("./My_pic"):
    image = face_recognition.load_image_file("./My_pic/"+i)
    face_encoding = face_recognition.face_encodings(image)[0]
    np.save('./face_encoding/'+i,face_encoding)
