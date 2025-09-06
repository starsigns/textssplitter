import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QSpinBox, QMessageBox
)
import os

class TextSplitterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.file_path = None

    def init_ui(self):
        self.setWindowTitle('Text File Splitter')
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout()

        self.label = QLabel('No file selected')
        layout.addWidget(self.label)

        self.btn_browse = QPushButton('Browse Text File')
        self.btn_browse.clicked.connect(self.browse_file)
        layout.addWidget(self.btn_browse)

        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(2)
        self.spinbox.setMaximum(100)
        self.spinbox.setValue(2)
        layout.addWidget(QLabel('Number of files to split into:'))
        layout.addWidget(self.spinbox)

        self.btn_split = QPushButton('Split File')
        self.btn_split.clicked.connect(self.split_file)
        layout.addWidget(self.btn_split)

        self.setLayout(layout)

    def browse_file(self):
        file_dialog = QFileDialog()
        path, _ = file_dialog.getOpenFileName(self, 'Open Text File', '', 'Text Files (*.txt)')
        if path:
            self.file_path = path
            self.label.setText(f'Selected: {os.path.basename(path)}')

    def split_file(self):
        if not self.file_path:
            QMessageBox.warning(self, 'No File', 'Please select a text file first.')
            return
        num_files = self.spinbox.value()
        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        total_lines = len(lines)
        if num_files > total_lines:
            QMessageBox.warning(self, 'Too Many Files', 'Number of files exceeds number of lines in the file.')
            return
        lines_per_file = total_lines // num_files
        extra = total_lines % num_files
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        dir_name = os.path.dirname(self.file_path)
        for i in range(num_files):
            start = i * lines_per_file + min(i, extra)
            end = start + lines_per_file + (1 if i < extra else 0)
            out_path = os.path.join(dir_name, f'{base_name}_part{i+1}.txt')
            with open(out_path, 'w', encoding='utf-8') as out_f:
                out_f.writelines(lines[start:end])
        QMessageBox.information(self, 'Done', f'Successfully split into {num_files} files.')

def main():
    app = QApplication(sys.argv)
    window = TextSplitterApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
