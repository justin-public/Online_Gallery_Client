import os
from ftplib import FTP
from PyQt5.QtCore import *

ftp_host = 'localhost'  # FTP 서버의 호스트 192.168.0.118      
ftp_port =  21      # FTP 서버의 포트

ID = 'admin'
PW = 'admin1234'

class ClientFTPThread(QThread):
    connected = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.connect_chk = False
        self.ftp = FTP()
        self.ftp.set_debuglevel(1)

    def run(self):
        try:
            self.ftp.connect(ftp_host, ftp_port)
            self.ftp.login(ID, PW)
            self.connect_chk = True
            self.connected.emit(True)  # 연결 상태 신호 발생
        except Exception as e:
            print(f"Failed to connect or login to the FTP server: {str(e)}")
            self.connect_chk = False
            self.connected.emit(False)  # 연결 상태 신호 발생

    def download_file(self, remote_filename, local_path):
        self.ftp.cwd('anonymous')
        local_filename = os.path.join(local_path,remote_filename)
        with open(local_filename,'wb') as save_f:
            self.ftp.retrbinary("RETR img_0002.jpg", save_f.write)      # 파일 이름과 디렉토리를 DB와 연동해야함

    def disconnect(self):
        self.ftp.quit()

    