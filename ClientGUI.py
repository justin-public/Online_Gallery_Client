import sys
import qrcode
import io
from PyQt5 import uic, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
#from ClientFTP import *
from threading import Lock, Thread, Event
import time
from socket import *
#from ftplib import FTP, error_perm
import ftplib
import os
import json
import random
import shutil
import psutil               # 이 모듈을 사용하여 파일이 열려 있는지 확인
import qrcode.constants
import win32file
import win32con
import cv2
from PIL import Image
from moviepy.editor import *
import moviepy.editor as mpy
from moviepy.video.fx.all import crop
import subprocess

Client_Gui = uic.loadUiType('PAGE/Connectwait.ui')[0]
image_view = uic.loadUiType('PAGE/imageview.ui')[0]
image_view1 = uic.loadUiType('PAGE/imageview1.ui')[0]
video_win_monitor1 = uic.loadUiType('PAGE/screen.ui')[0]
video_win_monitor2 = uic.loadUiType('PAGE/screen.ui')[0]
QR_win_monitor1 = uic.loadUiType('PAGE/QRlayout.ui')[0]

class QR_Widget(QMainWindow,QR_win_monitor1):
    def __init__(self,screen_geometry,image_path, x, y, width, height,parent=None):
        super(QR_Widget, self).__init__(parent)
        self.setGeometry(screen_geometry)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.initUI(image_path, x, y, width, height)
        self.showFullScreen()
    
    def initUI(self,image_path,x,y,width,height):
        self.label = QLabel(self)
        pixmap = QPixmap(image_path)
        self.label.setGeometry(QRect(x, y, width, height))
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        self.label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        self.circle_fistname(painter, 92, 1250, 830, "강")
        self.circle_fistname(painter, 92, 1250, 942, "송")

        self.Username_draw(painter,"강감찬",1350, 840)
        self.Username_draw(painter,"송시헌",1350, 950)

        self.Comment_data_draw(painter,"이 텍스트는 두 줄로 표시됩니다. 한글이 길어지면 줄바꿈\n됩니다.안녕하세요 반갑습니다.",1430,840)
        self.Comment_data_draw(painter,"이 텍스트는 두 줄로 표시됩니다. 한글이 길어지면 줄바꿈\n됩니다.안녕하세요 반갑습니다.",1430,950)

        self.Comment_date_draw(painter,"24.8.8 16:01",1430, 880)
        self.Comment_date_draw(painter,"24.8.9 16:02",1430, 990)

    def circle_fistname(self, painter, circle_diameter, circle_x, circle_y, firstname):
        self.firstname_text_color_inside = QColor(0, 0, 0)    # 원형 글씨 색상 설정
        self.firstname_text_color_outside = QColor(255, 0, 0)
        self.firstname_font_size_inside = 35
        circle_color = QColor(100, 150, 255)
        painter.setBrush(circle_color)
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        firstname_rect = QRect(circle_x, circle_y, circle_diameter, circle_diameter)
        painter.drawEllipse(firstname_rect)
        painter.setPen(self.firstname_text_color_inside)
        firstname_font_inside = QFont()       
        firstname_font_inside.setPointSize(self.firstname_font_size_inside) 
        painter.setFont(firstname_font_inside)
        painter.drawText(firstname_rect, Qt.AlignCenter,firstname)
    
    def Username_draw(self, painter, _name, _position_x, _position_y):
        self.Username_text_outside = _name
        self.Username_font_size_outside = 17
        Username_font_outside = QFont()
        Username_font_outside.setPointSize(self.Username_font_size_outside)
        Username_font_outside.setWeight(QFont.Bold)
        painter.setFont(Username_font_outside)
        Username_text_rect = QRect(_position_x, _position_y, 92, 60)
        painter.drawText(Username_text_rect, Qt.AlignLeft, self.Username_text_outside)

    def Comment_data_draw(self, painter, _comment_data, _position_x, _position_y):
        self.Commentdata_text_data = _comment_data
        self.Commentdata_font_size_data = 13
        Commentdata_font_history = QFont()
        Commentdata_font_history.setPointSize(self.Commentdata_font_size_data)
        painter.setFont(Commentdata_font_history)
        Commentdata_text_data_rect = QRect(_position_x, _position_y, 550, 200)
        painter.drawText(Commentdata_text_data_rect, Qt.AlignLeft | Qt.TextWordWrap, self.Commentdata_text_data)

    def Comment_date_draw(self, painter, _comment_date, _position_x, _position_y):
        self.Commentdate_text_data = _comment_date
        self.Commentdate_font_size_data = 13
        Commentdate_font_datetime = QFont()
        Commentdate_font_datetime.setPointSize(self.Commentdate_font_size_data)
        Commentdate_font_datetime.setWeight(QFont.Bold)
        painter.setFont(Commentdate_font_datetime)
        Commentdate_text_datatime_rect = QRect(_position_x, _position_y, 550, 200)
        painter.drawText(Commentdate_text_datatime_rect, Qt.AlignLeft, self.Commentdate_text_data)

class VideoWindow(QMainWindow, video_win_monitor1):
    def __init__(self, screen_geometry,sel,video_path,parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setGeometry(screen_geometry)
        self.initUI()
        
        if sel == 1:
            self.playlist = QMediaPlaylist()
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
            self.playlist.setCurrentIndex(0)
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
            self.mediaPlayer.setPlaylist(self.playlist)
            self.mediaPlayer.setVolume(0)
            self.mediaPlayer.play()

    def initUI(self):
        self.setupUi(self)
        self.videoOutput = self.makeVideoWidget()
        self.mediaPlayer = self.makeMediaPlayer()

    def makeMediaPlayer(self):
        mediaplayer = QMediaPlayer(self)
        mediaplayer.setVideoOutput(self.videoOutput)
        return mediaplayer

    def makeVideoWidget(self):
        videoOutput = QVideoWidget(self)
        videoOutput.setStyleSheet("background-color: black;")
        vbox = QVBoxLayout()
        vbox.addWidget(videoOutput)
        self.setCentralWidget(videoOutput)
        return videoOutput
    
    def delete_video(self, video_path):
        try:
            print(video_path)
            self.mediaPlayer.setMedia(QMediaContent())
            file = QFile(video_path)
            if file.exists():
                file.close()
                if file.remove():
                    print(f"Deleted {video_path}")
                else:
                    print(f"Error deleting {video_path}")
            else:
                print(f"File {video_path} does not exist.")
        except Exception as e:
            print(f"Error deleting {video_path}: {e}")
    
    def ratio_delete_video(self, video_path):
        try:
            print(video_path)
            self.mediaPlayer.setMedia(QMediaContent())
            file = QFile(video_path)
            if file.exists():
                file.close()
                if file.remove():
                    print(f"Deleted {video_path}")
                else:
                    print(f"Error deleting {video_path}")
            else:
                print(f"File {video_path} does not exist.")
        except Exception as e:
            print(f"Error deleting {video_path}: {e}")

class VideoWindow1(QMainWindow, video_win_monitor2):
    def __init__(self, screen_geometry,sel,video_path,parent=None):
        super(VideoWindow1, self).__init__(parent)
        self.setGeometry(screen_geometry)
        self.initUI()
        if sel == 1:
            self.playlist = QMediaPlaylist()
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
            self.playlist.setCurrentIndex(0)
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
            self.mediaPlayer.setPlaylist(self.playlist)
            self.mediaPlayer.setVolume(0)
            self.mediaPlayer.play()

    def initUI(self):
        self.setupUi(self)
        self.videoOutput = self.makeVideoWidget()
        self.mediaPlayer = self.makeMediaPlayer()

    def makeMediaPlayer(self):
        mediaplayer = QMediaPlayer(self)
        mediaplayer.setVideoOutput(self.videoOutput)
        return mediaplayer

    def makeVideoWidget(self):
        videoOutput = QVideoWidget(self)
        videoOutput.setStyleSheet("background-color: black;")
        vbox = QVBoxLayout()
        vbox.addWidget(videoOutput)
        self.setCentralWidget(videoOutput)
        return videoOutput
    
    def delete_video(self, video_path):
        try:
            print(video_path)
            self.mediaPlayer.setMedia(QMediaContent())
            file = QFile(video_path)
            if file.exists():
                file.close()
                if file.remove():
                    print(f"Deleted {video_path}")
                else:
                    print(f"Error deleting {video_path}")
            else:
                print(f"File {video_path} does not exist.")
        except Exception as e:
            print(f"Error deleting {video_path}: {e}")
    
    def ratio_delete_video(self, video_path):
        try:
            print(video_path)
            self.mediaPlayer.setMedia(QMediaContent())
            file = QFile(video_path)
            if file.exists():
                file.close()
                if file.remove():
                    print(f"Deleted {video_path}")
                else:
                    print(f"Error deleting {video_path}")
            else:
                print(f"File {video_path} does not exist.")
        except Exception as e:
            print(f"Error deleting {video_path}: {e}")

class ImageWidget(QWidget,image_view):
    def __init__(self,screen_geometry,image_path,parent=None):
        super(ImageWidget, self).__init__(parent)
        self.setGeometry(screen_geometry)
        self.initUI(image_path)
    
    def initUI(self,image_path):
        self.ContentsImage = QPixmap(image_path)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.ContentsImage)
        
class ImageWidget1(QWidget,image_view1):
    def __init__(self,screen_geometry,image_path,QRimage_path,parent=None):
        super(ImageWidget, self).__init__(parent)
        self.setGeometry(screen_geometry)
        self.initUI(image_path, QRimage_path)
    
    def initUI(self,image_path, QRimage_path):
        self.ContentsImage = QPixmap(image_path)
        self.second_image_pixmap = QPixmap(QRimage_path)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.ContentsImage)
        second_image_rect = QRect(1020, 830, 200, 200)
        painter.drawPixmap(second_image_rect, self.second_image_pixmap)

        self.circle_fistname(painter, 92, 1250, 830, "강")
        self.circle_fistname(painter, 92, 1250, 942, "송")

        self.Username_draw(painter,"강감찬",1350, 840)
        self.Username_draw(painter,"송시헌",1350, 950)

        self.Comment_data_draw(painter,"이 텍스트는 두 줄로 표시됩니다. 한글이 길어지면 줄바꿈\n됩니다.안녕하세요 반갑습니다.",1430,840)
        self.Comment_data_draw(painter,"이 텍스트는 두 줄로 표시됩니다. 한글이 길어지면 줄바꿈\n됩니다.안녕하세요 반갑습니다.",1430,950)

        self.Comment_date_draw(painter,"24.8.8 16:01",1430, 880)
        self.Comment_date_draw(painter,"24.8.9 16:02",1430, 990)
    
    def circle_fistname(self, painter, circle_diameter, circle_x, circle_y, firstname):
        self.firstname_text_color_inside = QColor(0, 0, 0)    # 원형 글씨 색상 설정
        self.firstname_text_color_outside = QColor(255, 0, 0)
        self.firstname_font_size_inside = 35
        circle_color = QColor(100, 150, 255)
        painter.setBrush(circle_color)
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        firstname_rect = QRect(circle_x, circle_y, circle_diameter, circle_diameter)
        painter.drawEllipse(firstname_rect)
        painter.setPen(self.firstname_text_color_inside)
        firstname_font_inside = QFont()       
        firstname_font_inside.setPointSize(self.firstname_font_size_inside) 
        painter.setFont(firstname_font_inside)
        painter.drawText(firstname_rect, Qt.AlignCenter,firstname)
    
    def Username_draw(self, painter, _name, _position_x, _position_y):
        self.Username_text_outside = _name
        self.Username_font_size_outside = 17
        Username_font_outside = QFont()
        Username_font_outside.setPointSize(self.Username_font_size_outside)
        Username_font_outside.setWeight(QFont.Bold)
        painter.setFont(Username_font_outside)
        Username_text_rect = QRect(_position_x, _position_y, 92, 60)
        painter.drawText(Username_text_rect, Qt.AlignLeft, self.Username_text_outside)

    def Comment_data_draw(self, painter, _comment_data, _position_x, _position_y):
        self.Commentdata_text_data = _comment_data
        self.Commentdata_font_size_data = 13
        Commentdata_font_history = QFont()
        Commentdata_font_history.setPointSize(self.Commentdata_font_size_data)
        painter.setFont(Commentdata_font_history)
        Commentdata_text_data_rect = QRect(_position_x, _position_y, 550, 200)
        painter.drawText(Commentdata_text_data_rect, Qt.AlignLeft | Qt.TextWordWrap, self.Commentdata_text_data)

    def Comment_date_draw(self, painter, _comment_date, _position_x, _position_y):
        self.Commentdate_text_data = _comment_date
        self.Commentdate_font_size_data = 13
        Commentdate_font_datetime = QFont()
        Commentdate_font_datetime.setPointSize(self.Commentdate_font_size_data)
        Commentdate_font_datetime.setWeight(QFont.Bold)
        painter.setFont(Commentdate_font_datetime)
        Commentdate_text_datatime_rect = QRect(_position_x, _position_y, 550, 200)
        painter.drawText(Commentdate_text_datatime_rect, Qt.AlignLeft, self.Commentdate_text_data)

class Image_delete(QObject):
    def __init__(self,image_path,parent=None):
        super(Image_delete, self).__init__(parent)
        self.initUI(image_path)
    
    def initUI(self, image_path):
        self.delete_image(image_path)
        #pass
    
    def delete_image(self, image_path):
        try:
            os.remove(image_path)
            print(f"Deleted: {image_path}")
        except OSError as e:
            print(f"Error deleting {image_path}: {e}")

class Ratio_video(QObject):
    def __init__(self,video_path):
        super().__init__()
        self.initUI(video_path)
    
    def initUI(self, video_path):
        media_content = QMediaContent(QUrl.fromLocalFile(video_path))
        
        #output_dir = r'c:\work\CloudGallery_CE\output_video'
        output_dir = r'D:\work\CloudGallery_CE\output_video'
        self.resize_video(video_path ,output_dir, 1920, 1080)  # 1920, 1080
    
    def resize_video(self, input_file ,output_dir, target_width, target_height):
        input_file_path = os.path.abspath(input_file)
        input_dir, input_filename = os.path.split(input_file_path)
        input_name, input_ext = os.path.splitext(input_filename)

        output_file = os.path.join(output_dir, f"{input_name}_resized{input_ext}")

        # FFmpeg 명령어 준비
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', input_file_path,                        # 입력 파일
            '-vf', f'scale={target_width}:{target_height}', # 비디오 필터 (해상도 조정)
            '-c:a', 'copy',                               # 오디오는 그대로 복사
            '-c:v', 'h264',                               # 비디오 코덱을 H.264로 설정
            '-crf', '23',                                 # 비디오 품질 설정
            '-y',                                        # 이미 존재하는 파일 덮어쓰기
            output_file                                  # 출력 파일
        ]
    
        try:
            subprocess.run(ffmpeg_cmd, check=True)
            print(f"비디오가 {output_file} 경로에 저장되었습니다.")
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg 명령어 실행 실패: {e}")
        
class ClientGUI(QWidget, Client_Gui):
    file_extension_cmd = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super(ClientGUI, self).__init__(parent)
        self.thread = None
        self.worker = None
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.client_socket_thread = ClientThread()
        self.client_socket_thread.start()
        self.client_socket_thread.command.connect(self.slot_logic)
    
    def kill_process_using_file(self , file_path):
        for proc in psutil.process_iter():
            try:
                # 프로세스가 파일을 사용 중인지 확인
                if file_path in proc.open_files():
                    print(f"{proc.name()} 프로세스가 {file_path} 파일을 사용 중입니다. 종료 시도 중...")
                    proc.kill()
                    print(f"{proc.name()} 프로세스를 종료했습니다.")
            except Exception as e:
                print(f"에러 발생: {e}")
    
    def slot_logic(self, sel, sel1):
        self.stagemsg = sel
        if self.stagemsg == 0:
            self.Connectstatuslb.setText("접속 대기중..")
            self.Connectstatuslb.setFont(QtGui.QFont("Arial",75))
            
        if self.stagemsg == 1:
            self.Connectstatuslb.setText("접속중..")
            self.Connectstatuslb.setFont(QtGui.QFont("Arial",75))
            #------------ home
            folder_path = r'D:\work\CloudGallery_CE\view'
            #------------ office
            #folder_path = r'c:\work\CloudGallery_CE\view'
            #output_video_path = r'D:\work\CloudGallery_CE\output_video'
            qr_output_dir = r'D:\work\CloudGallery_CE\QR'
            #qr_output_dir = r'c:\work\CloudGallery_CE\QR'
            image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.png') or f.endswith('.jpg')]
            video_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.avi') or f.endswith('.mp4')]
            QRimage_files = [os.path.join(qr_output_dir, f) for f in os.listdir(qr_output_dir) if f.endswith('.png') or f.endswith('.jpg')]
            
            output_video_path = r'D:\work\CloudGallery_CE\output_video'
            video_files_ = [os.path.join(output_video_path, f) for f in os.listdir(output_video_path) if f.endswith('.avi') or f.endswith('.mp4')]
            
            screen_count = QApplication.desktop().screenCount()
            if screen_count == 1:
                screen1_geometry = QApplication.desktop().screenGeometry(0)
                
                if len(image_files) >= 1:
                    self.imageobj = ImageWidget(screen1_geometry, image_files[0])
                    self.imageobj.close()
                    self.imageobjdel = Image_delete(image_files[0])
                
                if len(video_files) >= 1:
                    self.videoobj = VideoWindow(screen1_geometry,0,video_files[0])
                    self.videoobj.delete_video(video_files[0])
                
                if len(video_files_) >= 1:
                    self.videoobj = VideoWindow(screen1_geometry,0,video_files_[0])
                    self.videoobj.close()
                    self.videoobj.delete_video(video_files_[0])

                if len(QRimage_files) >= 1:
                    self.qroobj = QR_Widget(screen1_geometry, QRimage_files[0], 1020, 830, 200, 200)
                    self.qroobj.close()
                    self.imageobjdel = Image_delete(QRimage_files[0])
            
            
            """
            screen_count = QApplication.desktop().screenCount()
            if screen_count == 1:
                screen1_geometry = QApplication.desktop().screenGeometry(0)
                
                if len(image_files) >= 1:
                    self.imageobj = ImageWidget(screen1_geometry, image_files[0])
                    self.imageobj.close()
                    self.imageobjdel = Image_delete(image_files[0])
                    
                if len(QRimage_files) >= 1:
                    self.qroobj = QR_Widget(screen1_geometry, QRimage_files[0], 1020, 830, 200, 200)
                    self.qroobj.close()
                    self.imageobjdel = Image_delete(QRimage_files[0])
                
                if len(video_files) >= 1:
                    self.videoobj = VideoWindow(screen1_geometry,0,video_files[0])
                    self.videoobj.delete_video(video_files[0])
                    output_video_path = r'D:\work\CloudGallery_CE\output_video'
                    video_files_ = [os.path.join(output_video_path, f) for f in os.listdir(output_video_path) if f.endswith('.avi') or f.endswith('.mp4')]
                    if len(video_files_) >= 1:
                        self.videoobj = VideoWindow(screen1_geometry,0,video_files_[0])
                        self.videoobj.close()
                        self.videoobj.ratio_delete_video(video_files_[0])
            """
            # 스크린 2개인 경우 닫기 이벤트 예외 처리 추가해야함
            
        if self.stagemsg == 2:
            self.Connectstatuslb.setText("로딩중..")
            self.Connectstatuslb.setFont(QtGui.QFont("Arial",75))
            # DB 연동
            # 랜덤으로 바뀌는 리스트(서버 패킷)를 받아서 파일이름을 remote_filename 에 복사
            # ----------------- 주의 ----------------------------
            folder_name = sel1.replace('.', '-')
            print(folder_name)
            f = ftplib.FTP()
            f.set_debuglevel(2)
            f.connect('121.140.54.39',1000)
            #f.connect('192.168.0.114',1000)
            f.login('admin', 'admin1234')
            try:
                f.cwd(f'/lasthouse/{folder_name}')
                #f.cwd(f'{folder_name}')
            except ftplib.error_perm as e:
                if str(e).startswith('550'):
                    print(f"Directory '/lasthouse/{folder_name}' does not exist.")
                    #print(f"Directory '{folder_name}' does not exist.")
                    #f.quit()    # ----->
                    #exit()      # ----->
                    
            entries = f.nlst()
            print(entries)
            #------ home
            local_path = r'D:\work\CloudGallery_CE\view'
            #------ office
            #local_path = r'c:\work\CloudGallery_CE\view'
            
            #local_path = r'D:\work\CloudGallery_CE'
            #folder_name_path = 'view'
            #destination_folder = os.path.abspath(os.path.join(r'D:\work\CloudGallery_CE', folder_name_path))
            
            if not os.path.exists(local_path):
                os.makedirs(local_path)
            
            for filename in entries:
                local_filename = os.path.join(local_path,filename)
                try:
                    with open(local_filename, 'wb') as save_f:
                        f.retrbinary(f"RETR {filename}", save_f.write)
                except ftplib.error_perm as e:
                    if str(e).startswith('550'):
                       print(f"Permission denied or file not found for: {filename}")
                    else:
                         print(f"FTP error: {e}")
                except Exception as e:
                    print(f"Error retrieving file: {filename} - {e}")
            
            f.quit()               
            self.stagemsg = 3
            #-----------------------------------------------------
        if self.stagemsg == 3:
            # ------ home
            #folder_path = r'D:\work\CloudGallery_CE\view'
            # ------ PC
            folder_path = r'D:\work\CloudGallery_CE\view'
            #qr_output_dir = r'c:\work\CloudGallery_CE\QR'
            #output_video_path = r'D:\work\CloudGallery_CE\output_video'
            #folder_path = r'D:\work\CloudGallery_CE'
            image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.png') or f.endswith('.jpg')]
            video_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.avi') or f.endswith('.mp4')]
            #video_files_ = [os.path.join(output_video_path, f) for f in os.listdir(output_video_path) if f.endswith('.avi') or f.endswith('.mp4')]
            
            screen_count = QApplication.desktop().screenCount()
            if screen_count == 1:
                screen1_geometry = QApplication.desktop().screenGeometry(0)
                
                # 이미지 1개인 경우
                if len(image_files) == 1:
                    self.imageobj = ImageWidget(screen1_geometry, image_files[0])
                    self.imageobj.showFullScreen()
                       
                # 동영상 1개인 경우
                if len(video_files) == 1:
                    Ratio_video(video_files[0])
                    #output_video_path = r'c:\work\CloudGallery_CE\output_video'
                    output_video_path = r'D:\work\CloudGallery_CE\output_video'
                    video_files_ = [os.path.join(output_video_path, f) for f in os.listdir(output_video_path) if f.endswith('.avi') or f.endswith('.mp4')]
                    if len(video_files_) == 1:
                        self.videoobj = VideoWindow(screen1_geometry,1,video_files[0])
                        self.videoobj.showFullScreen()
                        
                        
            if screen_count >= 2:
                screen1_geometry = QApplication.desktop().screenGeometry(0)
                screen2_geometry = QApplication.desktop().screenGeometry(1)
                
                # 이미지 1개 동영상 1개인 경우 QR 이미지 1개인 경우
                if len(image_files) == 1 and len(video_files) == 1:
                    self.imageobj = ImageWidget(screen1_geometry, image_files[0], QRimage_files[0])
                    self.imageobj.showFullScreen()

                    Ratio_video(video_files[0])
                    output_video_path = r'D:\work\CloudGallery_CE\output_video'
                    #output_video_path = r'c:\work\CloudGallery_CE\output_video'
                    video_files_ = [os.path.join(output_video_path, f) for f in os.listdir(output_video_path) if f.endswith('.avi') or f.endswith('.mp4')]
                    #qr_output_dir = r'D:\work\CloudGallery_CE\QR'
                    qr_output_dir = r'c:\work\CloudGallery_CE\QR'
                    QRimage_files_ = [os.path.join(qr_output_dir, f) for f in os.listdir(qr_output_dir) if f.endswith('.png') or f.endswith('.jpg')]
                    if len(video_files_) == 1 and len(QRimage_files_):
                        self.videoobj = VideoWindow(screen2_geometry,1,video_files[0])
                        self.videoobj.showFullScreen()
                        self.qroobj = QR_Widget(screen2_geometry, QRimage_files_[0], 1020, 830, 200, 200)
                        self.qroobj.showFullScreen()
                
                # 이미지 2개인 경우 , 동영상 2개인 경우 예외 처리 추가 해야함 
        if self.stagemsg == 4:
            folder_path = r'D:\work\CloudGallery_CE\view'
            image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.png') or f.endswith('.jpg')]  # 이미지 파일인 경우
            output_video_path = r'D:\work\CloudGallery_CE\view'
            video_files_ = [os.path.join(output_video_path, f) for f in os.listdir(output_video_path) if f.endswith('.avi') or f.endswith('.mp4')]
            #qr_output_dir = r'D:\work\CloudGallery_CE\QR'
            #QRimage_files_ = [os.path.join(qr_output_dir, f) for f in os.listdir(qr_output_dir) if f.endswith('.png') or f.endswith('.jpg')]
            
            print(sel1)
            screen_count = QApplication.desktop().screenCount()
            if screen_count == 1:
                print("Error 0")
                if len(image_files) == 1:
                    print("Error 1")
                    imagefilename = os.path.basename(image_files[0])
                    filesplit = str(sel1).split('/')
                    print(filesplit[1])
                    print(imagefilename)
                    if  filesplit[1] == imagefilename:
                        print("Error 2")
                        url = 'http://172.30.1.1:8501'
                        self.generate_qr_code(url, filesplit[0], filesplit[2])

                        qr_output_dir = r'D:\work\CloudGallery_CE\QR'
                        QRimage_files_ = [os.path.join(qr_output_dir, f) for f in os.listdir(qr_output_dir) if f.endswith('.png') or f.endswith('.jpg')]
                        
                        if len(QRimage_files_) == 1:
                            print("Error 3")
                            screen1_geometry = QApplication.desktop().screenGeometry(0)
                            self.qroobj = QR_Widget(screen1_geometry, QRimage_files_[0], 1020, 830, 200, 200)
                            self.qroobj.showFullScreen()

            """
            if len(image_files) == 1:
                imagefilename = os.path.basename(image_files[0])
                filesplit = str(sel1).split('/')
                print(filesplit)
                if  filesplit[1] == imagefilename:
                    print(filesplit[0])
                    print(filesplit[1])
                    print(imagefilename)
                    url = 'http://172.30.1.1:8501'
                    self.generate_qr_code(url, filesplit[0], filesplit[2])
            
                qr_output_dir = r'D:\work\CloudGallery_CE\QR'
                QRimage_files_ = [os.path.join(qr_output_dir, f) for f in os.listdir(qr_output_dir) if f.endswith('.png') or f.endswith('.jpg')]
            
                screen_count = QApplication.desktop().screenCount()
                if screen_count == 1:
                    screen1_geometry = QApplication.desktop().screenGeometry(0)
                    if len(QRimage_files_) == 1:
                        screen1_geometry = QApplication.desktop().screenGeometry(0)
                        self.qroobj = QR_Widget(screen1_geometry, QRimage_files_[0], 1020, 830, 200, 200)
                        self.qroobj.showFullScreen()

            if len(video_files_) == 1:
                videofilename = os.path.basename(video_files_[0])
                filesplit = str(sel1).split('/')
                if filesplit[1] == videofilename:
                    print(filesplit[0])
                    print(filesplit[1])
                    print(videofilename)
                    url = 'http://172.30.1.1:8501'
                    self.generate_qr_code(url, filesplit[0], filesplit[2])
                
                qr_output_dir = r'D:\work\CloudGallery_CE\QR'    
                QRimage_files_ = [os.path.join(qr_output_dir, f) for f in os.listdir(qr_output_dir) if f.endswith('.png') or f.endswith('.jpg')]
                screen_count = QApplication.desktop().screenCount()
                if screen_count == 1:
                    screen1_geometry = QApplication.desktop().screenGeometry(0)
                    if len(QRimage_files_) == 1:
                        screen1_geometry = QApplication.desktop().screenGeometry(0)
                        self.qroobj = QR_Widget(screen1_geometry, QRimage_files_[0], 1020, 830, 200, 200)
                        self.qroobj.showFullScreen()
            """




    
    def generate_qr_code(self, url, id_number, qrimagename):
        data = f"{url}?id={id_number}"
        
        qr_folder_path = r'D:\work\CloudGallery_CE\QR'
        full_path = os.path.join(qr_folder_path, qrimagename)
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save(full_path)                     
        
HOST = '121.140.54.39'
#HOST = '192.168.0.114'
PORT = 6060
BUFSIZE = 1024
ADDR = (HOST, PORT)

class ClientThread(QThread):
    command = pyqtSignal(int, str)
    QRcommand = pyqtSignal(int, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_stage = True

    pyqtSlot(int)
    def run(self):
        while True:
            clientSocket = socket(AF_INET, SOCK_STREAM)
            try:
                clientSocket.connect(ADDR)
                print('Connected to server')
                while True:
                    try:
                        data = clientSocket.recv(1024)
                        #print(data)
                        self.servercommand = data.decode('utf-8')
                        try:
                            self.servercommand = self.servercommand.replace("'", '"')
                            data_dict = json.loads(self.servercommand)
                            #print("Received JSON data:", data_dict)
                            if 'csv_data' in data_dict:
                                csv_data = data_dict['csv_data']
                                for item in csv_data:
                                    self.display_id = item['Display ID']
                                    self.ip = item['IP']
                                    self.display_port = item['Display Port']
                                    if self.ip == "121.140.54.39":
                                        self.stage_msg = 2
                                        self.command.emit(self.stage_msg, self.ip)

                            if 'sel_data' in data_dict : 
                                sel_data = data_dict['sel_data']
                                print(sel_data)
                                for item in sel_data:
                                    # 여기서 매칭 작업을 진행해야함
                                    #print(f"ID: {item['ID']}, Path: {item['path']}, Image: {item['image']}, QR Code: {item['qr_code']}") 
                                    self.contentsid = item['ID']
                                    self.itemimage = item['image']
                                    self.qrid = item['qr_code']
                                    
                                    self.itemimage_contentsid = self.contentsid + '/' + self.itemimage + '/' + self.qrid
                                    self.stage_msg = 4
                                    self.command.emit(self.stage_msg, self.itemimage_contentsid)
                                
                                
                        
                        
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON: {e}")
                        
                        """
                        self.servercommand = data.decode('utf-8')
                        try:
                            self.servercommand = self.servercommand.replace("'", '"')
                            data_list = json.loads(self.servercommand)
                            for item in data_list:
                                self.display_id = item['Display ID']
                                self.ip = item['IP']
                                self.display_port = item['Display Port']
                                if self.ip == "121.140.54.39":
                                #if self.ip == "192.168.0.114":
                                    print("IP check")
                                    self.stage_msg = 2
                                    self.command.emit(self.stage_msg, self.ip)           # emit 은 여러개를 던질수 있다.              
                                    #print("PC 매칭..")
                                    #if display_id == "C001D1" and display_port == ""
                                #print(display_id)
                                #print(ip)
                                #print(display_port)
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON: {e}")
                        """
                        self.ftpcommand = self.servercommand.split(',')
                        if self.ftpcommand[1] == 'close':
                            self.stage_msg = 1
                            nullvalue = ''
                            self.command.emit(self.stage_msg, nullvalue)
                        
                        # 이부분 중요함
                        #---------------------------------------------------#
                        #self.ftpcommand = self.servercommand.split(',')
                        #print(self.ftpcommand[1])
                        #if self.ftpcommand[1] == 'close':
                            #self.stage_msg = 1
                            #nullvalue = ''
                            #self.command.emit(self.stage_msg, nullvalue)
                        
                        #if self.ftpcommand[1] == 'close1':
                            #self.stage_msg = 4
                            #nullvalue = ''
                            #self.command.emit(self.stage_msg, nullvalue)
                        
                        #if self.ftpcommand[1] == 'open':
                            #self.stage_msg = 2
                            #self.command.emit(self.stage_msg)
                        #---------------------------------------------------#
                        print('Message sent')
                        time.sleep(5)
                    except Exception as e:
                        print('Error sending message:', e)
                        break
            except Exception as e:
                self.stage_msg = False
                nullvalue = ''
                self.command.emit(self.stage_msg,nullvalue)
                print('Connection failed:', e)
                time.sleep(1)
            finally:
                clientSocket.close()
                print('Connection closed\n')

def main():
    app = QApplication(sys.argv)
    win = ClientGUI()
    win.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.CustomizeWindowHint)
    win.showFullScreen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
