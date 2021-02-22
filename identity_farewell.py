#coding=utf-8
import sys
sys.path.append("/home/pi/develop/F/FaceMaskDetection")
from FaceMaskDetection.tensorflow_infer import inference
import cv2
import os
import face_recognition
import numpy as np
from module import modules
from random import randint
from PyQt5.QtCore import pyqtSignal,QThread
class Face_reco(QThread):
    '''
    人脸识别线程
    '''
    change_pixmap_signal = pyqtSignal(np.ndarray)
    def __init__(self):
        super(Face_reco, self).__init__()
        #用于计数
        self.count = 0

        #人脸特征数据列表
        self.known_face_encodings = []
        #人脸姓名数据列表(需要用姓名来命名)
        self.know_face_name = []
        for i in os.listdir("/home/pi/develop/F/face_encoding/"):
                face_encoding = np.load("/home/pi/develop/F/face_encoding/"+i)
                self.known_face_encodings.append(face_encoding)
                self.know_face_name.append(i.split('.')[0])
        # 实例化相机对象
        self.cap = cv2.VideoCapture(0)
        # 实例化硬件驱动对象
        self.module = modules()
        # 判断摄像头是否打开
        self.is_need_live = True
    def run(self):
        '''
        完成人脸识别功能
        :param frame:需要一帧图片数据 (Opencv Image)
        :return: True or False (Bool)
        '''
        #实例化相机对象
        process_this_frame = True
        while self.is_need_live:
            ret,frame = self.cap.read()
            small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
            rgb_small_frame = small_frame[:,:,::-1]
            #Only process every other frame of video to save time
            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)
                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings,face_encoding,tolerance=0.5)
                    name = "Unkonw"

                    face_distances = face_recognition.face_distance(self.known_face_encodings,face_encoding)
                    best_math_index = np.argmin(face_distances)
                    if matches[best_math_index]:
                        name = self.know_face_name[best_math_index]
                    face_names.append(name)
            process_this_frame = not process_this_frame
            # 显示结果
            for (top,right,bottom,left),name in zip(face_locations,face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                #画一个框框
                cv2.rectangle(frame,(left,top),(right,bottom),(0,0,255),2)
                #cv2.rectangle(frame,(left,bottom-35),(right,bottom),(0,0,255),cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame,name,(left+5,bottom-6),font,1.0,(255,255,255),1)
                # 报警
                if name == "Unkonw":
                    self.count += 1
                if self.count == 15:
                    self.module.warn()
                    self.count = 0

            if ret:
                self.change_pixmap_signal.emit(frame)
    def close(self):
        self.is_need_live = False
        self.cap.release()
class MASK_detection(QThread):
    '''
    口罩识别线程
    '''
    # 创建自定义信号
    change_pixmap_signal = pyqtSignal(np.ndarray)
    def __init__(self):
        super(MASK_detection, self).__init__()
        # 实例化相机对象
        self.cap = cv2.VideoCapture(0)
        # 判断摄像头是否打开
        self.is_need_live = True
    def run(self):
        '''
        实现口罩检测功能,
        :return: true or false
        '''
        # 实例化相机对象
        while self.is_need_live:
            #获取一帧以针的图像
            status,img_raw = self.cap.read()
            #将BGR图片转化为RGB图片
            Rgb_img = cv2.cvtColor(img_raw,cv2.COLOR_BGR2RGB)
            try:
                res,_,xmin,ymin,xmax,ymax = inference(
                    Rgb_img,            #图片
                    conf_thresh = 0.5,  #检测阈值
                    iou_thresh = 0.4,
                    target_shape = (260,260),
                    draw_result = True,
                )
            except TypeError:
                pass
            if status:
                self.change_pixmap_signal.emit(Rgb_img[:,:,::-1])
    def close(self):
        self.is_need_live = False
        self.cap.release()

class Face_entry(QThread):
    # 创建自定义信号
    change_pixmap_signal = pyqtSignal(np.ndarray)
    # 信号完成按钮
    finally_signal = pyqtSignal(int)
    def __init__(self):
        super(Face_entry,self).__init__()
        # 实例化相机对象
        self.cap = cv2.VideoCapture(0)
        # 判断摄像头是否打开
        self.is_need_live = True
        # 记录录入图片的数量
        self.count = 0
        # 一个随机的姓名
        self.name = randint(1000,9999)


    def run(self):
        while self.is_need_live:
            status , frame = self.cap.read()
            small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
            rgb_small_frame = small_frame[:,:,::-1]
            face_locations = face_recognition.face_locations(rgb_small_frame)
            for (top,right,bottom,left) in face_locations:
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame,(left,top),(right,bottom),(0,0,255),2)
            if status:
                self.change_pixmap_signal.emit(frame)
                # 发送完成信号
                self.count += 1
                if self.count % 50 == 0:
                    try:
                        face_encoding = face_recognition.face_encodings(rgb_small_frame,face_locations)[0]
                        np.save("/home/pi/develop/F/face_encoding/"+str(self.name)+"."+str(self.count/5),face_encoding)
                    except:
                        self.count -= 1
                if self.count == 170:
                    self.finally_signal.emit(self.name)
    def close(self):
        self.is_need_live = False
        self.cap.release()
