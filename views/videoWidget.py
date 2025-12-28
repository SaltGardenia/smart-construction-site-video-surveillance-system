import cv2
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import datetime
import hat


class videoWidget(QWidget):

    videoUpdata = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.cameraState = False # 摄像头状态
        self.videoCapture = None

        self.recordingStartTime = None # 记录视频录制开始时间
        self.videoWriter = None # 定义视频输出对象

        self.current_videos_path = 'videos/工地.mp4' # 默认播放路径
        self.is_playing = False # 避免误点击

        self.initUI() # 初始化UI
        self.timer = QTimer() # 定时器
        self.timer.timeout.connect(self.update)
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.play_frame)
        self.timer3 = QTimer() # 云检测定时器
        self.timer3.timeout.connect(self.check_viedo)


    def initUI(self):
        """
        初始化UI
        :return:
        """

        # Btn
        self.playBtn = QPushButton('播放')
        self.stopBtn = QPushButton('暂停')
        self.cameraBtn = QPushButton('开启摄像头')
        self.cloudBtn = QPushButton('云检测')

        self.playBtn.clicked.connect(self.play)
        self.stopBtn.clicked.connect(self.stop)
        self.cameraBtn.clicked.connect(self.camera)
        self.cloudBtn.clicked.connect(self.cloud)

        self.btnLayout = QHBoxLayout()
        for btn in [self.playBtn, self.stopBtn, self.cameraBtn, self.cloudBtn]:
            btn.setMaximumWidth(100)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.btnLayout.addWidget(btn)

        # video
        self.videoLable = QLabel(self)
        self.videoLable.setFixedSize(660, 520)
        self.videoLable.setPixmap(QPixmap('images/icon.png').scaled(self.videoLable.size()))
        # layout
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.btnLayout)
        self.layout.addWidget(self.videoLable)
        self.setLayout(self.layout)


    def play(self):
        """
        播放视频
        :return:
        """

        if self.current_videos_path and not self.is_playing:
            self.start_video()


    def stop(self):
        """
        暂停播放
        :return:
        """

        if self.is_playing:
            self.stop_video()


    def camera(self):
        """
        打开摄像头
        :return:
        """

        if not self.cameraState:
            self.startCamera()
        else:
            self.stopCamera()


    def startCamera(self):
        """
        开启摄像头
        :return:
        """

        try:
            if self.cameraState == True:
                self.stopCamera()

            self.videoCapture = cv2.VideoCapture(0)
            if self.videoCapture.isOpened():
                self.timer.start(33)
                self.cameraBtn.setText('关闭摄像头')
                self.cameraState = True
            self.startRecording()
        except Exception as e:
            print(e)


    def stopCamera(self):
        """
        关闭摄像头
        :return:
        """

        try:
            self.cameraState = False
            self.timer.stop()
            if self.videoCapture:
                self.videoCapture.release()
                self.videoCapture = None
            if self.videoWriter:
                self.videoWriter.release()
                self.videoWriter = None
            self.recordingStartTime = None
            self.cameraBtn.setText('打开摄像头')
            self.videoLable.setPixmap(QPixmap('images/icon.png').scaled(self.videoLable.size()))
        except Exception as e:
            print(e)



    def update(self):
        """
        更新摄像头画面
        :return:
        """

        try:
            if self.videoCapture:
                ret, frame = self.videoCapture.read()
                if ret:
                    frameResize = cv2.resize(frame, (660, 520))

                    # 时间戳的显示
                    now = datetime.datetime.now()
                    nowStr = now.strftime("%Y-%m-%d %H:%M:%S")
                    cv2.putText(frameResize, nowStr, (5, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 2, cv2.LINE_AA)

                    if self.videoWriter:
                        self.videoWriter.write(frameResize)

                    diffTime = (now - self.recordingStartTime).total_seconds() # 时间差并转为秒数

                    # 录制视频

                    if self.recordingStartTime and diffTime >= 20:
                        self.startRecording()

                    frameRgb = cv2.cvtColor(frameResize, cv2.COLOR_BGR2RGB)
                    h, w, ch = frameRgb.shape
                    img = QImage(frameRgb.data, w, h, 3*w, QImage.Format_RGB888)
                    self.videoLable.setPixmap(QPixmap.fromImage(img))
        except Exception as e:
            print(e)


    def startRecording(self):
        """
        录制视频
        :return:
        """

        try:
            if self.videoWriter:
                self.videoWriter.release()

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            now = datetime.datetime.now()
            filename = now.strftime("%Y%m%d%H%M%S") + '.mp4'
            filepath = f'./videos/{filename}'
            self.videoWriter = cv2.VideoWriter(filepath, fourcc, 33, (660, 520))
            # 开始记录时间
            self.recordingStartTime = now

            self.videoUpdata.emit()

        except Exception as e:
            print(e)




    def cloud(self):
        """
        调用云模型
        :return:
        """

        file_name = self.current_videos_path.split('/')[-1].split('.')[0]
        save_path = f'check_videos/{file_name}_check.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.videoCapture = cv2.VideoCapture(self.current_videos_path)
        self.video_check_writer = cv2.VideoWriter(save_path, fourcc, 33, (660, 520))
        self.timer3.start()
        self.check_viedo()



    def check_viedo(self):
        """
        检测
        :return:
        """

        if self.videoCapture:
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                temp_path = 'images/temp.jpg'
                cv2.imwrite(temp_path, frame_rgb)

                date_dict = hat.hat_check(temp_path)

                label_list = date_dict['detection_classes']
                boxes_list = date_dict['detection_boxes']
                scores_list = date_dict['detection_scores']
                print(label_list, boxes_list, scores_list)

                #使用OpenCV操作图片
                # img = cv2.imread(file_path)
                #解析
                for i in range(len(boxes_list)):
                    box = boxes_list[i]
                    y1, x1, y2, x2 = box[0], box[1], box[2], box[3] #字符串
                    y1 = int(float(y1))
                    x1 = int(float(x1))
                    y2 = int(float(y2))
                    x2 = int(float(x2))
                    label = label_list[i]
                    score = scores_list[i]
                    #绘制矩形     图片    左上角    右下角     颜色      粗细
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                text = '{0}({1:0.2f}%)'.format(label, score * 100)
                cv2.putText(frame, text, (x1+10, y1+10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                print('检测完成')
                self.videoCapture.release()
                self.videoCapture = None
                self.video_check_writer.release()
                self.videoWriter = None
                self.timer3.stop()


    def start_video(self):
        """
        播放视频
        :return:
        """

        self.stopCamera() # 停止摄像头
        # 获取视频对象
        self.videoCapture = cv2.VideoCapture(self.current_videos_path)
        if self.videoCapture.isOpened():
            self.is_playing = True
            self.timer2.start(33)
        else:
            self.videoLable.setText('无法打开视频')



    def play_frame(self):
        """
        绘制播放视频的画面
        :return:
        """

        if self.videoCapture:
            ret, frame = self.videoCapture.read()
            if ret:
                frameResize = cv2.resize(frame, (660, 520))
                frameRgb = cv2.cvtColor(frameResize, cv2.COLOR_BGR2RGB)
                h, w, ch = frameRgb.shape
                img = QImage(frameRgb.data, w, h, 3*w, QImage.Format_RGB888)
                self.videoLable.setPixmap(QPixmap.fromImage(img))
        else:
            self.videoLable.setText('无法打开视频')

    def stop_video(self):
        """
        停止播放
        :return:
        """

        self.is_playing = False
        self.timer2.stop()
        if self.videoCapture:
            self.videoCapture.release()
            self.videoCapture = None


    def show_first_frame(self, video_path):
        """
        显示视频第一帧
        :param video_path:
        :return:
        """
        try:
            self.stop_video()
            self.stopCamera()
            self.current_videos_path = video_path
            video_cap = cv2.VideoCapture(self.current_videos_path)
            if video_cap.isOpened():
                ret, frame = video_cap.read()
                if ret:
                    frameResize = cv2.resize(frame, (660, 520))
                    frameRgb = cv2.cvtColor(frameResize, cv2.COLOR_BGR2RGB)
                    h, w, ch = frameRgb.shape
                    img = QImage(frameRgb.data, w, h, 3*w, QImage.Format_RGB888)
                    self.videoLable.setPixmap(QPixmap.fromImage(img))
                video_cap.release()
            else:
                self.videoLable.setText('无法打开视频')
        except Exception as e:
            print(e)
