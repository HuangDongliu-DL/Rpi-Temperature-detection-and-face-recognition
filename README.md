## 一、项目说明

1. 题目：一种简易的无接触温度测量与身份识别装置(2020年电赛F题)

2. 题目链接：https://www.nuedc-training.com.cn/index/news/details/new_id/227

4. 实现功能：

   - 无接触温度测量（包括红点标识，可设置阈值、超过阈值报警）【报警是通过蜂鸣器实现】
   - 检测是否符合防疫标准（口罩检测）
   - 身份检测（人脸识别，识别不通过是会报警）
   - 身份录入

5. 硬件列表：

   - Raspberry pi 4B（4G RAM） 
   - 32G 内存卡
   - Raspberry camera
   - 有源蜂鸣器
   - 红点激光
   - MLX90614非接触式红外测量传感器
   - LED可触屏显示屏
   - 杜邦线若干

6. Raspberry pi 线路连接

   - MXL90614线路连接

       VIN -- 5V（2）

       GND -- GND（6）

       SCL -- SCL（5）

       SDA -- SDA （3）

   - 蜂鸣器线路连接

       VIN -- GPIO16（36）

       GND -- GND（34）

   - 红点激光线路连接

       VIN -- 5V（4）

       GND -- GPIO26（37）

7. 开发环境简述：

   - Python3
   - numpy
   - OpenCv2
   - tensorflow
   - dlib
   - PyQt5

8. 参考开源库/框架：

   - AIZOOTech/FaceMaskDetection(https://github.com/AIZOOTech/FaceMaskDetection)
   - ageitgey/face_recognition(https://github.com/ageitgey/face_recognition)


## 二、项目文件目录说明

1. \_\_pycache\_\_  \

   Python脚本运行产生缓存文件，可删除无影响

2. face_encoding \

   用于存储人脸特征数据

3. FaceMaskDetection \

   GITHUB上口罩检测的开源库

4. My_pic \

   用于存储预处理图片

5. data.conf

   以JSON格式存储温度阈值数据

6. face_encoding.py

   用于提取My_pic中照片的人脸数据并存储在face_encoding \ 中

7. identity_farewell.py

   QT的副线程对象，包括与摄像头相关的操作例如：人脸识别、口罩检测、人脸录入。

8. module.py

   蜂鸣器、红点激光、红外测温模板的硬件驱动对象

9. main.py

   主函数，包括QT框架的布局，总体的调度，以及各种功能的实现。

## 三、GUI界面展示

- 主页
  <img src='https://dongliu-1301367244.cos.ap-shanghai.myqcloud.com/img/%E4%B8%BB%E9%A1%B5.jpg'>

- 温度测量页面
  <img src="https://dongliu-1301367244.cos.ap-shanghai.myqcloud.com/img/%E6%B8%A9%E5%BA%A6%E6%B5%8B%E9%87%8F%E9%A1%B5%E9%9D%A2.jpg">

- 温度阈值设置页面

  <img src="https://dongliu-1301367244.cos.ap-shanghai.myqcloud.com/img/%E6%B8%A9%E5%BA%A6%E9%98%88%E5%80%BC%E8%AE%BE%E7%BD%AE%E9%A1%B5%E9%9D%A2.jpg">

- 口罩检测与人脸识别页面

  <img src="https://dongliu-1301367244.cos.ap-shanghai.myqcloud.com/img/%E5%8F%A3%E7%BD%A9%E6%A3%80%E6%B5%8B%E4%B8%8E%E8%BA%AB%E4%BB%BD%E8%AF%86%E5%88%AB%E9%A1%B5%E9%9D%A2.jpg">

- 人脸录入页面

  <img src="https://dongliu-1301367244.cos.ap-shanghai.myqcloud.com/img/%E4%BA%BA%E8%84%B8%E5%BD%95%E5%85%A5%E9%A1%B5%E9%9D%A2.jpg">

- 设置页面

  <img src="https://dongliu-1301367244.cos.ap-shanghai.myqcloud.com/img/%E8%AE%BE%E7%BD%AE%E9%A1%B5%E9%9D%A2.jpg">

- 关于我们页面

  <img src="https://dongliu-1301367244.cos.ap-shanghai.myqcloud.com/img/%E5%85%B3%E4%BA%8E%E6%88%91%E4%BB%AC%E9%A1%B5%E9%9D%A2.jpg">

- 部分功能演示照片

  <img src="https://dongliu-1301367244.cos.ap-shanghai.myqcloud.com/img/%E4%BA%BA%E8%84%B8%E8%AF%86%E5%88%AB.jpg">

  <img src="https://dongliu-1301367244.cos.ap-shanghai.myqcloud.com/img/%E5%8F%A3%E7%BD%A9%E8%AF%86%E5%88%AB(A).jpg">

  <img src="https://dongliu-1301367244.cos.ap-shanghai.myqcloud.com/img/%E5%8F%A3%E7%BD%A9%E6%A3%80%E6%B5%8B(B).jpg">

  

## 四、代码架构

#### 1.main.py

```python
class BASE_Tmperate:
        '''
    基础模板
    包括：
        回到首页按钮及其样式，网格化布局对象
    '''
class ID_Temperate():
    '''
    摄像头调用相关模板
    包括：
        回到首页按钮及其样式，网格化布局对象，图片标签，图片转换函数与更新图片函数
    '''
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """使用Opencv图片更新图片框"""
    def convert_cv_qt(self, cv_img):
        """将Opencv图片格式转化为QPixmap"""
class SET_Temperate():
    '''
    设置二级目录相关模板
    包括：
        回到上一级按钮及其样式、网格化布局对象
    '''
class MainWindow(QWidget):
    '''主页的基本样式'''
    
class Thermometry(QWidget,BASE_Temperate):
    '''温度测量界面'''
    def start(self):
        '''开始测量函数'''
    @pyqtSlot(float)
    def update_temperature(self, temperature):
        '''温度更新函数'''
    def go_home(self):
        '''回到首页函数'''

class measure_temperature_thread(QThread, Thermometry):
    '''温度测量的副线程'''
    def run(self):
        '''开启线程'''
    def close(self):
        '''关闭线程'''

class setting(QWidget,BASE_Temperate):
    '''设置页面'''

class about_us(QWidget,SET_Temperate):
    '''关于我们页面'''
    

class temperature_threshold(QWidget,SET_Temperate):
    '''温度阈值设置'''
    def up_func(self):
		'''调高温度，事件函数'''
    def down_func(self):
        '''调低温度，事件函数'''
    def commit_func(self):
        '''提交数据，事件函数'''
        
class ID(QWidget,ID_Temperate):
    '''身份识别与口罩检测'''
    def func_mask_detection(self):
        '''开始口罩识别'''
    def func_face_recognition(self):
        '''开始人脸识别'''
    def func_stop(self):
        '''停止'''
       
class Id_entry(QWidget,ID_Temperate):
	'''身份录入'''
    def Func_Start(self):
        '''开始'''
    def Func_stop(self):
        '''停止'''
    @pyqtSlot(int)
    def Func_close(self,B):
        '''停止事件'''
```

#### 2.identity_farewell.py

```python
class Face_reco(QThread):
    '''
    人脸识别线程
    '''
    def run(self):
        '''
        完成人脸识别功能
        :param frame:需要一帧图片数据 (Opencv Image)
        :return: True or False (Bool)
        '''
    def close(self):
        '''关闭'''
        
class MASK_detection(QThread):
    '''
    口罩识别线程
    '''
    def run(self):
        '''
        实现口罩检测功能,
        :return: true or false
        '''
    def close(self):

class Face_entry(QThread):
	'''
	人脸录入
	'''
    def run(self):
		'''开启'''
    def close(self):
		'''关闭'''

```

#### 2.module.py

```python
class modules:
    def __init__(self, address=0x5A):
    def readAmbient(self):
    def readObject1(self):
    def readObject2(self):
    def _readTemp(self, reg):
    #开启激光
    def laser_start(self):
    #关闭激光
    def laser_stop(self):
    #蜂鸣器警报
    def warn(self):
    #读取阈值数据
    def read_threshold(self):
    #写入阈值数据
    def write_threshold(self,data):
```

## 五、代码迁移注意

- identity_farewell.py

  需要将该文件中`sys.path.append("/home/pi/develop/F/FaceMaskDetection")`,路径改为所在文件夹路径。

- FaceMaskDetection/tensorflow_infer.py

  需要将该文件中`sys.path.append("/home/pi/develop/F/FaceMaskDetection")`,路径改为所在文件夹路径。