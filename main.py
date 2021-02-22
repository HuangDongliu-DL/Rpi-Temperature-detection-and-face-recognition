#coding=utf-8
#author：huangjianxiong(huangdongliu)
#start time：2020.11.21
#endtime ：2020.12.13
import sys,cv2
import numpy as np
from module import modules
from time import sleep
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QGridLayout,QLabel,QVBoxLayout
from PyQt5 import QtGui
from PyQt5.QtGui import QFont,QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from identity_farewell import Face_reco,MASK_detection,Face_entry


class BASE_Temperate():
    '''
    基础模板
    包括：
        回到首页按钮及其样式，网格化布局对象
    '''
    def __init__(self):
        self.home_Button = QPushButton("回到首页")
        self.home_Button.setStyleSheet("background-color:rgb(204, 255, 153)")
        self.home_Button.setFont(QFont('Times', 25))
        self.grid = QGridLayout()
        self.grid.addWidget(self.home_Button, *(0, 0))
class ID_Temperate():
    '''
    摄像头调用相关模板
    包括：
        回到首页按钮及其样式，网格化布局对象，图片标签，图片转换函数与更新图片函数
    '''
    def __init__(self):
        self.home_Button = QPushButton("回到首页")
        self.home_Button.setStyleSheet("background-color:rgb(204, 255, 153)")
        self.home_Button.setFont(QFont('Times', 25))
        #回到首页按钮
        self.home_Button.clicked.connect(self.close)
        self.image_label = QLabel(self)
        self.grid = QGridLayout()
        self.grid.addWidget(self.home_Button, *(0, 0))
        self.grid.addWidget(self.image_label,*(1,0))
        # 图片标签
        self.disply_width = 740
        self.display_height = 480
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
class SET_Temperate():
    '''
    设置二级目录相关模板
    包括：
        回到上一级按钮及其样式、网格化布局对象
    '''
    def __init__(self):
        self.home_Button = QPushButton("回到上一级")
        self.home_Button.setFont(QFont('Times', 25))
        self.home_Button.setStyleSheet("background-color:rgb(204, 255, 153)")
        self.home_Button.clicked.connect(self.close)
        self.grid = QGridLayout()
        self.grid.addWidget(self.home_Button, *(0, 0))
#主页
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()   #继承父类
        self.initUI()        #在实例化类后直接运行该对象
    def initUI(self):
        grid = QGridLayout()
        positions = [(0,0),(0,1),(1,0),(1,1)]
        #定义四个按钮，并将按钮放在一个列表中
        self.thermometry = QPushButton('温度测量\n')
        self.id = QPushButton('身份识别\n口罩检测')
        self.identity_entry = QPushButton('人脸录入\n')
        self.setting = QPushButton('设置\n')
        buttons = [self.thermometry,self.id,self.identity_entry,self.setting]
        for button,position in zip(buttons,positions):
            button.setFont(QFont('Times',50))
            grid.addWidget(button,*position)
        self.setLayout(grid)
        self.setWindowTitle('F题院赛')
        self.showFullScreen()
# 温度测量界面
class Thermometry(QWidget,BASE_Temperate):
    def __init__(self):
        super().__init__()
        # 开关变量，1是表示打开，0表示关闭
        self.switch = 0
        self.sensor = modules()
        self.text_label = QLabel()
        self.start_Button = QPushButton('开始测量')
        # 判断线程是否暂停
        self.is_pause = False

    def initUI(self):
        # 实例化副线程对象
        self.thread = measure_temperature_thread()
        # 绑定温度更新函数
        self.thread.change_temperature_singal.connect(self.update_temperature)
        self.threshold = self.sensor.read_threshold()
        self.text_label.setText("温度阈值为：%s℃。\n当前温度为：--℃" % str(self.threshold))
        self.text_label.setFont(QFont('Times', 50))
        self.start_Button.setFont(QFont('Times', 50))
        self.start_Button.clicked.connect(self.start)
        self.home_Button.clicked.connect(self.go_home)
        self.grid.addWidget(self.text_label, *(1, 0))
        self.grid.addWidget(self.start_Button, *(2, 0))
        self.setLayout(self.grid)
        self.showFullScreen()
    def start(self):
        # self.switch =0,是属于关闭测量状态。开启测量
        if self.switch == 0:
            self.switch = 1
            self.start_Button.setText("关闭测量")
            self.home_Button.setDisabled(True)

            # 开启红点激光
            self.sensor.laser_start()
            self.thread.start()
        # 关闭测量
        else:
            self.switch = 0
            self.start_Button.setText("开始测量")
            self.home_Button.setDisabled(False)
            # 关闭红点激光
            self.sensor.laser_stop()
    # 温度更新函数
    @pyqtSlot(float)
    def update_temperature(self, temperature):
        if self.switch == 1:
            if temperature >= self.threshold:
                self.sensor.warn()
            else:
                pass
            self.text_label.setText("温度阈值为：%s℃。\n当前温度为：%.2f℃" % (str(self.threshold), temperature))
        else:
            pass

    def go_home(self):
        self.close()
        self.thread.close()
# 温度测量的副线程
class measure_temperature_thread(QThread, Thermometry):
    def __init__(self):
        super().__init__()
    # 自定义信号
    change_temperature_singal = pyqtSignal(float)
    sensor = modules()
    # 启动线程
    def run(self):
        # 就让线程一直运行下去
        while True:
            temperautre_data = round(self.sensor.readObject1(), 2)  # 读取表面温度数据并保留两位小数
            self.change_temperature_singal.emit(temperautre_data)  # 发送信号
            sleep(0.5)
    # 结束线程
    def close(self):
        self.terminate()
# 设置页面
class setting(QWidget,BASE_Temperate):
    def __init__(self):
        super().__init__()
        self.threshold = QPushButton("温度阈值设置\n")
        self.to_quit = QPushButton("退出系统\n")
        self.about_me = QPushButton("关于我们\n")

    def initUI(self):
        self.home_Button.clicked.connect(self.close)
        buttons = [self.threshold, self.about_me, self.to_quit]
        positions = [(1, 0), (2, 0), (3, 0)]
        for button, position in zip(buttons, positions):
            button.setFont(QFont('Times', 50))
            self.grid.addWidget(button, *position)
        self.setLayout(self.grid)
        self.showFullScreen()
# 关于我们页面
class about_us(QWidget,SET_Temperate):
    def __init__(self):
        super().__init__()
        self.text_label = QLabel("三峡大学电气与新能源学院院赛作品" + '\n'
                                "赛题：简易的非接触温度测量与身份识别装置" + '\n'
                                "作者：黄建雄，查传洋，詹若璞" + '\n'
                                "项目开始时间：2020年11月25日" + '\n'
                                "项目完成时间：2020年12月13日")
        self.text_label.setFont(QFont('Times', 25))
    def initUI(self):
        self.grid.addWidget(self.text_label, *(1, 0))
        self.setLayout(self.grid)
        self.showFullScreen()
# 温度阈值设置
class temperature_threshold(QWidget,SET_Temperate):
    def __init__(self):
        super(temperature_threshold, self).__init__()
        self.sensor = modules()
        self.threshold = self.sensor.read_threshold()
        # 定义控件
        self.text_label = QLabel("设置当前阈值为：%s ℃" % self.threshold)
        self.up = QPushButton("温度增加")
        self.down = QPushButton("温度降低")
        self.commit = QPushButton("提交")
        # 定义事件
        self.up.clicked.connect(self.up_func)
        self.down.clicked.connect(self.down_func)
        self.commit.clicked.connect(self.commit_func)
    def initUI(self):
        self.threshold = self.sensor.read_threshold()
        self.text_label.setText("设置当前阈值为：%s ℃" % self.threshold)
        widgets = [self.text_label, self.up, self.down, self.commit]
        positions = [(1, 0), (2, 0), (3, 0), (4, 0)]
        for widget, position in zip(widgets, positions):
            self.grid.addWidget(widget, *(position))
            widget.setFont(QFont('Times', 25))
        self.setLayout(self.grid)
        self.showFullScreen()
    # 调高温度，事件函数
    def up_func(self):
        self.threshold += 1
        self.text_label.setText("设置当前阈值为：%s ℃" % self.threshold)
    # 调低温度，事件函数
    def down_func(self):
        self.threshold -= 1
        self.text_label.setText("设置当前阈值为：%s ℃" % self.threshold)
    # 提交数据，事件函数
    def commit_func(self):
        self.sensor.write_threshold(self.threshold)
        self.text_label.setText("设置阈值成功,当前阈值为：%s ℃" % self.threshold)
class ID(QWidget,ID_Temperate):
    def __init__(self):
        super().__init__()

        #口罩检测按钮
        self.Mask_detection_button = QPushButton("开始口罩检测")
        self.Mask_detection_button.clicked.connect(self.func_mask_detection)
        self.Mask_detection_button.setFont(QFont('Times',30))
        #人脸识别按钮
        self.Face_recognition_button = QPushButton("开始人脸识别")
        self.Face_recognition_button.clicked.connect(self.func_face_recognition)
        self.Face_recognition_button.setFont(QFont('Times',30))
        #关闭，所有检测都是通过这个按钮关闭
        self.Stop_button = QPushButton("结束")
        self.Stop_button.clicked.connect(self.func_stop)
        self.Stop_button.setFont(QFont('Times',30))


        self.grid.addWidget(self.Mask_detection_button,*(2,0))
        self.grid.addWidget(self.Face_recognition_button,*(3,0))
        self.grid.addWidget(self.Stop_button,*(4,0))
    def initUI(self):
        self.Stop_button.setDisabled(True)

        self.setLayout(self.grid)
        self.showFullScreen()
    def func_mask_detection(self):
        '''开始口罩识别'''
        #再开始口罩识别后处理关闭按钮可以执行之外其他按钮都disabled
        self.Stop_button.setDisabled(False)
        self.home_Button.setDisabled(True)
        self.Mask_detection_button.setDisabled(True)
        self.Face_recognition_button.setDisabled(True)
        self.thread = MASK_detection()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
    def func_face_recognition(self):
        '''开始人脸识别'''
        self.Stop_button.setDisabled(False)
        self.home_Button.setDisabled(True)
        self.Mask_detection_button.setDisabled(True)
        self.Face_recognition_button.setDisabled(True)
        self.thread = Face_reco()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
    def func_stop(self):
        '''开始人脸识别'''
        #再关闭最后所有按钮都恢复
        self.home_Button.setDisabled(False)
        self.Mask_detection_button.setDisabled(False)
        self.Face_recognition_button.setDisabled(False)
        self.Stop_button.setDisabled(True)
        self.thread.close()
class Id_entry(QWidget,ID_Temperate):
    def __init__(self):
        super(Id_entry, self).__init__()
        self.Start_Button = QPushButton("开始采集人脸数据")
        self.Start_Button.setFont(QFont('Times',50))
        self.grid.addWidget(self.Start_Button,*(2,0))
        self.Start_Button.clicked.connect(self.Func_Start)
        self.setLayout(self.grid)
    def initUI(self):
        self.Start_Button.setDisabled(False)
        self.Start_Button.setText("开始采集人脸数据")
        self.showFullScreen()
    def Func_Start(self):
        self.Start_Button.setText("正在进行数据采集")
        self.Start_Button.setDisabled(True)

        self.thread = Face_entry()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.finally_signal.connect(self.Func_close)
        self.thread.start()
    def Func_stop(self):
        self.thread.close()
    @pyqtSlot(int)
    def Func_close(self,B):
        self.thread.close()
        self.Start_Button.setText("数据录入成功编号为："+str(B))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 主页界面
    mw = MainWindow()
    # 温度测量界面
    t = Thermometry()
    # 设置页面
    set = setting()
    # 关于我们页面
    ab = about_us()
    # 温度阈值设置页面
    th = temperature_threshold()
    # 身份识别与口罩检测
    id = ID()
    # 人脸数据录入
    id_entry = Id_entry()

    mw.thermometry.clicked.connect(t.initUI)
    mw.setting.clicked.connect(set.initUI)
    mw.id.clicked.connect(id.initUI)
    mw.identity_entry.clicked.connect(id_entry.initUI)

    set.about_me.clicked.connect(ab.initUI)
    set.threshold.clicked.connect(th.initUI)
    set.to_quit.clicked.connect(sys.exit)
    sys.exit(app.exec_())
