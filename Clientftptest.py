import ftplib
import os

# ftp 정보
host='localhost'
user='admin'
passwd='admin1234'

# 파일정보
uploadFile=r'D:\work\CloudGallery_SB\home\f10024\data.csv'

###############
# 파일 다운로드
###############
try:
  # ftp 연결
  with ftplib.FTP() as ftp:
    ftp.connect(host=host,port=21)
    ftp.encoding='utf-8'
    s=ftp.login(user=user,passwd=passwd)
    ftp.cwd('/home/f10024')     # 현재 폴더 이동
    # 파일다운로드
    with open(file=r'D:\work\CloudGallery_SB\home\f10024\data.csv', mode='wb') as rf:
        ftp.retrbinary('RETR data.csv', rf.write)
except Exception as e:
    print(e)


