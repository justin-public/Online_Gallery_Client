import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QFile, QIODevice

class VideoPlayerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 동영상 파일 경로 설정
        self.video_file = "video.mp4"

        # QMediaPlayer 초기화
        self.player = QMediaPlayer()

        # UI 설정
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 640, 480)

        # 재생 버튼 생성 및 클릭 이벤트 연결
        play_button = QPushButton('Play', self)
        play_button.clicked.connect(self.play_video)
        play_button.setGeometry(50, 50, 100, 50)

    def play_video(self):
        media = QMediaContent(QUrl.fromLocalFile(self.video_file))
        self.player.setMedia(media)

        # 동영상 재생 시작
        self.player.play()

        # 재생이 끝나면 파일 삭제
        self.player.stateChanged.connect(self.check_state)

    def check_state(self, state):
        if state == QMediaPlayer.StoppedState:
            # QMediaPlayer가 멈춘 상태일 때 파일 삭제 시도
            self.delete_video_file()

    def delete_video_file(self):
        try:
            # QMediaPlayer의 media를 해제하여 파일 자원을 정리
            self.player.setMedia(QMediaContent())

            # QFile을 사용하여 파일을 닫고 삭제 시도
            file = QFile(self.video_file)
            if file.exists():
                file.close()  # 파일 닫기
                if file.remove():
                    print(f"Deleted {self.video_file}")
                else:
                    print(f"Error deleting {self.video_file}")
            else:
                print(f"File {self.video_file} does not exist.")

        except Exception as e:
            print(f"Error deleting {self.video_file}: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player_window = VideoPlayerWindow()
    player_window.show()
    sys.exit(app.exec_())
