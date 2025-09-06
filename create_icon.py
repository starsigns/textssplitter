import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont, QBrush, QColor
from PyQt5.QtCore import Qt

def create_app_icon():
    # Create a 64x64 icon
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Draw gradient background circle
    gradient = QBrush(QColor('#4338ca'))
    painter.setBrush(gradient)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(2, 2, 60, 60)
    
    # Draw text splitter symbol
    painter.setPen(QColor('#ffffff'))
    painter.setFont(QFont('Arial', 24, QFont.Bold))
    painter.drawText(pixmap.rect(), Qt.AlignCenter, '📄')
    
    painter.end()
    
    # Save as icon
    pixmap.save('app_icon.ico')
    pixmap.save('app_icon.png')
    
    return 'app_icon.ico'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    icon_path = create_app_icon()
    print(f"Icon created: {icon_path}")
    app.quit()
