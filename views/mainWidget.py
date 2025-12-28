import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from views.videoWidget import videoWidget

class mainWidget(QWidget):
    def __init__(self):
        super(mainWidget, self).__init__()
        self.setWindowTitle('智慧工地视频监控系统')
        self.resize(1300, 700)
        self.setWindowIcon(QIcon('images/icon.png'))
        pixmap = QPixmap('images/bg.jpg').scaled(self.size())
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)

        self.videoPath = 'videos/'

        self.initUI() # 初始化控件

        self.updateFileList() # 更新视频列表


    def initUI(self):
        self.titleLabel = QLabel('智慧工地', self)
        self.titleLabel.setGeometry(575, 15, 300, 30)
        self.titleLabel.setStyleSheet("color:white; font:35px")
        self.totalLayout = QHBoxLayout()
        self.setLayout(self.totalLayout)
        self.leftLayout = QVBoxLayout()
        self.midLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()
        self.totalLayout.addLayout(self.leftLayout)
        self.totalLayout.addLayout(self.midLayout)
        self.totalLayout.addLayout(self.rightLayout)
        self.left1 = QLabel('监控视频数：4个\n已检测视频数:10个\n未检测视频数:13个', self)
        self.left2 = QLabel('当前工地异常情况:\n无安全帽:10个\n未穿反光衣:13个')
        self.left1.setStyleSheet("color:white; font:20xp; padding:10px")
        self.left2.setStyleSheet("color:white; font:20px; padding:10px")
        self.leftLayout.addWidget(self.left1)
        self.leftLayout.addWidget(self.left2)

        self.vidoeWidget = videoWidget()
        self.midLayout.addWidget(self.vidoeWidget)
        self.vidoeWidget.videoUpdata.connect(self.updateFileList)

        self.right1 = QLabel('工地实时监控列表>>', self)
        self.right2 = QLabel('工地实时监测列表>>', self)
        self.right1.setStyleSheet("color:white; font:20px; padding:10px")
        self.right2.setStyleSheet("color:white; font:20px; padding:10px")

        self.view1 = QListView()
        self.view2 = QListView()
        self.rightLayout.addWidget(self.right1)
        self.rightLayout.addWidget(self.view1)
        self.rightLayout.addWidget(self.right2)
        self.rightLayout.addWidget(self.view2)

        self.totalLayout.setStretchFactor(self.leftLayout, 2)
        self.totalLayout.setStretchFactor(self.midLayout, 6)
        self.totalLayout.setStretchFactor(self.rightLayout, 2)

        self.leftLayout.setContentsMargins(10, 30, 0, 0)
        self.midLayout.setContentsMargins(30, 30, 0, 0)
        self.rightLayout.setContentsMargins(0, 30, 0, 0)


    def updateFileList(self):
        """
        更新列表
        :return:
        """
        self.videoList = self.getVideoList(self.videoPath)

        self.slm1 = QStringListModel() # 创建数据模型
        self.slm1.setStringList(self.videoList) # 给数据模型绑定数据
        self.view1.setModel(self.slm1) # 添加数据模型

        self.view1.clicked.connect(self.list_view_click)


    def getVideoList(self, path):
        """
        获取path路径下的文件夹中的所有视频内容
        :param path:
        :return:
        """
        files = os.listdir(path)
        return files


    def list_view_click(self, item):
        """
        列表点击事件
        :param item: 被点击对象
        :return:
        """

        # 获取点击路径
        index = item.row()
        filename = self.videoList[index]
        file_path = self.videoPath + filename

        # 预览
        self.vidoeWidget.current_videos_path = file_path
        self.vidoeWidget.show_first_frame(file_path)
