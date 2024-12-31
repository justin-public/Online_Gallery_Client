import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush
from PyQt5.QtCore import Qt, QRect, QPoint

class CircleTextWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Circle with Text Example')
        self.setGeometry(100, 100, 300, 300)
        
        # Example radius value
        self.circle_radius = 50  # Adjust this value to change the size of the circle

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Set circle properties
        circle_center = self.rect().center()
        
        # Use the instance variable circle_radius
        circle_rect = QRect(
            int(circle_center.x() - self.circle_radius),
            int(circle_center.y() - self.circle_radius),
            int(2 * self.circle_radius),
            int(2 * self.circle_radius)
        )
        
        # Draw the circle
        painter.setBrush(QBrush(Qt.lightGray))
        painter.drawEllipse(circle_rect)

        # Draw the text
        text = "강"
        font = QFont('Arial', 16)
        painter.setFont(font)
        painter.setPen(QColor(Qt.black))
        
        # Calculate text size and position
        text_rect = painter.boundingRect(circle_rect, Qt.AlignCenter, text)
        text_rect.moveCenter(circle_center)
        
        # Draw the text centered in the circle
        painter.drawText(text_rect, Qt.AlignCenter, text)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setCentralWidget(CircleTextWidget())
        self.setGeometry(100, 100, 300, 300)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
