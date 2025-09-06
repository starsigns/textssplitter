import sys
import os
import importlib
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QSpinBox, QMessageBox,
    QTextEdit, QProgressBar, QListWidget, QListWidgetItem, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor


class TextSplitterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = self.load_settings()
        self.file_paths = []
        self.output_dir = self.settings.get('last_directory', os.getcwd())
        self.theme = self.settings.get('last_theme', 'light')
        self.init_ui()
        self.apply_theme(self.theme)

    def init_ui(self):
        self.setWindowTitle('Text File Splitter')
        self.setGeometry(100, 100, 600, 500)
        layout = QVBoxLayout()

        # File selection and drag-and-drop
        self.label = QLabel('No files selected. Drag and drop files here or use Browse.')
        self.label.setAcceptDrops(True)
        self.setAcceptDrops(True)
        layout.addWidget(self.label)

        self.file_list = QListWidget()
        layout.addWidget(self.file_list)

        btn_layout = QHBoxLayout()
        self.btn_browse = QPushButton('Browse Text Files')
        self.btn_browse.clicked.connect(self.browse_file)
        btn_layout.addWidget(self.btn_browse)

        self.btn_output = QPushButton('Select Output Directory')
        self.btn_output.clicked.connect(self.select_output_dir)
        btn_layout.addWidget(self.btn_output)
        layout.addLayout(btn_layout)

        self.output_label = QLabel(f'Output Directory: {self.output_dir}')
        layout.addWidget(self.output_label)

        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(2)
        self.spinbox.setMaximum(100)
        self.spinbox.setValue(self.settings.get('last_num_files', 2))
        layout.addWidget(QLabel('Number of files to split into:'))
        layout.addWidget(self.spinbox)

        # Theme toggle
        self.theme_checkbox = QCheckBox('Dark Theme')
        self.theme_checkbox.setChecked(self.theme == 'dark')
        self.theme_checkbox.stateChanged.connect(self.toggle_theme)
        layout.addWidget(self.theme_checkbox)

        # File preview
        layout.addWidget(QLabel('File Preview:'))
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        layout.addWidget(self.preview)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.btn_split = QPushButton('Split File(s)')
        self.btn_split.clicked.connect(self.split_file)
        layout.addWidget(self.btn_split)

        self.setLayout(layout)

        self.file_list.itemSelectionChanged.connect(self.update_preview)

    def browse_file(self):
        file_dialog = QFileDialog()
        paths, _ = file_dialog.getOpenFileNames(self, 'Open Text Files', self.output_dir, 'Text Files (*.txt)')
        if paths:
            self.file_paths = paths
            self.file_list.clear()
            for p in self.file_paths:
                self.file_list.addItem(QListWidgetItem(p))
            self.label.setText(f'Selected {len(self.file_paths)} file(s).')
            self.update_preview()
            self.save_settings()

    def select_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select Output Directory', self.output_dir)
        if dir_path:
            self.output_dir = dir_path
            self.output_label.setText(f'Output Directory: {self.output_dir}')
            self.save_settings()

    def split_file(self):
        if not self.file_paths:
            QMessageBox.warning(self, 'No File', 'Please select at least one text file first.')
            return
        num_files = self.spinbox.value()
        self.progress.setValue(0)
        total_files = len(self.file_paths)
        for idx, file_path in enumerate(self.file_paths):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                total_lines = len(lines)
                if num_files > total_lines:
                    QMessageBox.warning(self, 'Too Many Files', f'File {os.path.basename(file_path)}: Number of files exceeds number of lines.')
                    continue
                lines_per_file = total_lines // num_files
                extra = total_lines % num_files
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                for i in range(num_files):
                    start = i * lines_per_file + min(i, extra)
                    end = start + lines_per_file + (1 if i < extra else 0)
                    out_path = os.path.join(self.output_dir, f'{base_name}_part{i+1}.txt')
                    with open(out_path, 'w', encoding='utf-8') as out_f:
                        out_f.writelines(lines[start:end])
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Error splitting {file_path}: {e}')
            self.progress.setValue(int((idx+1)/total_files*100))
        self.progress.setValue(100)
        QMessageBox.information(self, 'Done', f'Successfully split {total_files} file(s).')
        self.save_settings()

    def update_preview(self):
        selected = self.file_list.selectedItems()
        if not selected:
            self.preview.clear()
            return
        file_path = selected[0].text()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                preview_text = ''.join([next(f) for _ in range(20)])
            self.preview.setText(preview_text)
        except Exception:
            self.preview.setText('(Could not preview file)')


    # Drag and drop support
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls() if u.toLocalFile().endswith('.txt')]
        if files:
            self.file_paths = files
            self.file_list.clear()
            for p in self.file_paths:
                self.file_list.addItem(QListWidgetItem(p))
            self.label.setText(f'Selected {len(self.file_paths)} file(s).')
            self.update_preview()
            self.save_settings()

    # Theme support
    def apply_theme(self, theme):
        app = QApplication.instance()
        palette = QPalette()
        if theme == 'dark':
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
            palette.setColor(QPalette.HighlightedText, Qt.black)
        else:
            palette = app.style().standardPalette()
        app.setPalette(palette)

    def toggle_theme(self):
        self.theme = 'dark' if self.theme_checkbox.isChecked() else 'light'
        self.apply_theme(self.theme)
        self.save_settings()

    # Settings persistence
    def load_settings(self):
        try:
            import settings
            return {
                'last_directory': getattr(settings, 'last_directory', os.getcwd()),
                'last_num_files': getattr(settings, 'last_num_files', 2),
                'last_theme': getattr(settings, 'last_theme', 'light'),
            }
        except Exception:
            return {'last_directory': os.getcwd(), 'last_num_files': 2, 'last_theme': 'light'}

    def save_settings(self):
        try:
            with open('settings.py', 'w', encoding='utf-8') as f:
                f.write(f"last_directory = '{self.output_dir}'\n")
                f.write(f"last_num_files = {self.spinbox.value()}\n")
                f.write(f"last_theme = '{self.theme}'\n")
        except Exception:
            pass

def main():
    app = QApplication(sys.argv)
    window = TextSplitterApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
