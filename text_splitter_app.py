import sys
import os
import importlib
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QSpinBox, QMessageBox,
    QTextEdit, QProgressBar, QListWidget, QListWidgetItem, QCheckBox, QGroupBox, QFrame, QSplitter
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon, QPixmap


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
        self.setGeometry(100, 100, 900, 650)
        
        # Set window icon
        try:
            self.setWindowIcon(QIcon('app_icon.ico'))
        except:
            pass  # Fallback if icon file not found
            
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 12, 20, 12)
        main_layout.setSpacing(16)

        # Header with icon and subtitle
        header = QFrame()
        header.setStyleSheet('''
            QFrame { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4338ca, stop:1 #7c3aed); 
                border-radius: 16px; 
                border: 2px solid rgba(255,255,255,0.2);
                margin: 4px;
            }
        ''')
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(24, 16, 24, 16)
        header_layout.setSpacing(12)
        icon = QLabel()
        icon_pix = QPixmap(48, 48)
        icon_pix.fill(QColor('#ffffff'))
        icon.setPixmap(icon_pix)
        icon.setStyleSheet('''
            border-radius: 24px; 
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f59e0b, stop:1 #d97706); 
            margin: 6px;
            border: 3px solid #ffffff;
        ''')
        
        # Add a text overlay for the icon
        icon_text = QLabel('📄')
        icon_text.setFont(QFont('Segoe UI Emoji', 24))
        icon_text.setAlignment(Qt.AlignCenter)
        icon_text.setStyleSheet('background: transparent; color: #ffffff;')
        icon_text.setParent(icon)
        icon_text.setGeometry(12, 12, 24, 24)
        header_layout.addWidget(icon)
        title_sub = QVBoxLayout()
        title_sub.setSpacing(2)
        title = QLabel('Text File Splitter')
        title.setFont(QFont('Segoe UI', 24, QFont.Bold))
        title.setStyleSheet('color: #ffffff;')
        subtitle = QLabel('Split your text files easily and beautifully ✨')
        subtitle.setFont(QFont('Segoe UI', 12))
        subtitle.setStyleSheet('color: #f3f4f6;')
        title_sub.addWidget(title)
        title_sub.addWidget(subtitle)
        header_layout.addLayout(title_sub)
        header_layout.addStretch()
        header.setLayout(header_layout)
        main_layout.addWidget(header)

        # Card layout for main content
        card = QFrame()
        card.setStyleSheet('QFrame { background: #ffffff; border-radius: 12px; border: 1px solid #e5e7eb; }')
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(24, 16, 24, 16)
        card_layout.setSpacing(12)

        # File selection and preview with splitter
        splitter = QSplitter(Qt.Horizontal)
        left_panel = QFrame()
        left_panel.setStyleSheet('QFrame { background: #f9fafb; border-radius: 8px; border: 1px solid #e5e7eb; }')
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(16, 12, 16, 12)
        left_layout.setSpacing(8)
        self.label = QLabel('📁 No files selected. Drag and drop files here or use Browse.')
        self.label.setAcceptDrops(True)
        self.setAcceptDrops(True)
        self.label.setStyleSheet('padding: 12px; font-size: 11pt; color: #6b7280; background: #ffffff; border: 2px dashed #d1d5db; border-radius: 8px; text-align: center;')
        left_layout.addWidget(self.label)
        self.file_list = QListWidget()
        self.file_list.setAlternatingRowColors(True)
        self.file_list.setStyleSheet('''
            QListWidget { 
                border-radius: 8px; 
                background: #ffffff; 
                font-size: 11pt; 
                border: 1px solid #e5e7eb;
                padding: 4px;
            } 
            QListWidget::item { 
                padding: 8px; 
                border-radius: 4px; 
                margin: 2px;
            }
            QListWidget::item:hover { 
                background: #f3f4f6; 
            }
            QListWidget::item:selected {
                background: #dbeafe;
                color: #1f2937;
            }
        ''')
        left_layout.addWidget(self.file_list)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        self.btn_browse = QPushButton('📂 Browse Files')
        self.btn_browse.setToolTip('Select one or more text files to split')
        self.btn_browse.setStyleSheet('''
            QPushButton { 
                border-radius: 8px; 
                padding: 8px 16px; 
                font-size: 11pt; 
                font-weight: 500;
                background: #3b82f6; 
                color: #ffffff;
                border: none;
            } 
            QPushButton:hover { 
                background: #2563eb; 
            }
            QPushButton:pressed {
                background: #1d4ed8;
            }
        ''')
        self.btn_browse.clicked.connect(self.browse_file)
        btn_layout.addWidget(self.btn_browse)
        self.btn_output = QPushButton('📁 Output Directory')
        self.btn_output.setToolTip('Choose where split files will be saved')
        self.btn_output.setStyleSheet('''
            QPushButton { 
                border-radius: 8px; 
                padding: 8px 16px; 
                font-size: 11pt; 
                font-weight: 500;
                background: #10b981; 
                color: #ffffff;
                border: none;
            } 
            QPushButton:hover { 
                background: #059669; 
            }
            QPushButton:pressed {
                background: #047857;
            }
        ''')
        self.btn_output.clicked.connect(self.select_output_dir)
        btn_layout.addWidget(self.btn_output)
        left_layout.addLayout(btn_layout)
        self.output_label = QLabel(f'📍 Output: {self.output_dir}')
        self.output_label.setStyleSheet('color: #6b7280; font-size: 10pt; padding: 8px 0; font-weight: 500;')
        left_layout.addWidget(self.output_label)
        left_panel.setLayout(left_layout)
        splitter.addWidget(left_panel)

        right_panel = QFrame()
        right_panel.setStyleSheet('QFrame { background: #f9fafb; border-radius: 8px; border: 1px solid #e5e7eb; }')
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(16, 12, 16, 12)
        right_layout.setSpacing(8)
        preview_label = QLabel('📄 File Preview')
        preview_label.setFont(QFont('Segoe UI', 12, QFont.Bold))
        preview_label.setStyleSheet('color: #374151; padding: 4px 0;')
        right_layout.addWidget(preview_label)
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setFont(QFont('Consolas', 10))
        self.preview.setStyleSheet('''
            QTextEdit { 
                background: #ffffff; 
                border-radius: 8px; 
                font-size: 10pt; 
                border: 1px solid #e5e7eb;
                padding: 8px;
                line-height: 1.5;
            }
        ''')
        right_layout.addWidget(self.preview)
        right_panel.setLayout(right_layout)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 400])
        card_layout.addWidget(splitter)

        # Settings and progress
        settings_progress = QHBoxLayout()
        settings_progress.setSpacing(12)
        settings_box = QFrame()
        settings_box.setStyleSheet('QFrame { background: #f3f4f6; border-radius: 10px; border: 1px solid #e5e7eb; }')
        settings_layout = QHBoxLayout()
        settings_layout.setContentsMargins(16, 8, 16, 8)
        settings_layout.setSpacing(12)
        files_label = QLabel('⚙️ Split into:')
        files_label.setStyleSheet('font-size: 12pt; font-weight: bold; color: #1f2937;')
        settings_layout.addWidget(files_label)
        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(2)
        self.spinbox.setMaximum(100)
        self.spinbox.setValue(self.settings.get('last_num_files', 2))
        self.spinbox.setToolTip('Number of files to split each text file into')
        self.spinbox.setStyleSheet('''
            QSpinBox { 
                border-radius: 6px; 
                padding: 6px 12px; 
                font-size: 12pt; 
                font-weight: bold;
                border: 2px solid #d1d5db;
                background: #ffffff;
                min-width: 80px;
                color: #1f2937;
            }
            QSpinBox:focus {
                border: 2px solid #3b82f6;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                background: #f3f4f6;
                border: none;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background: #e5e7eb;
            }
        ''')
        settings_layout.addWidget(self.spinbox)
        files_suffix = QLabel('files')
        files_suffix.setStyleSheet('font-size: 12pt; font-weight: bold; color: #374151;')
        settings_layout.addWidget(files_suffix)
        settings_layout.addStretch()
        self.theme_checkbox = QCheckBox('🌙 Dark Theme')
        self.theme_checkbox.setChecked(self.theme == 'dark')
        self.theme_checkbox.setToolTip('Toggle between light and dark mode')
        self.theme_checkbox.setStyleSheet('QCheckBox { font-size: 11pt; font-weight: 500; color: #374151; }')
        self.theme_checkbox.stateChanged.connect(self.toggle_theme)
        settings_layout.addWidget(self.theme_checkbox)
        settings_box.setLayout(settings_layout)
        settings_progress.addWidget(settings_box)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setFixedHeight(32)
        self.progress.setStyleSheet('''
            QProgressBar { 
                border-radius: 10px; 
                text-align: center; 
                font-weight: bold; 
                font-size: 11pt; 
                background: #f3f4f6;
                border: 1px solid #e5e7eb;
                color: #374151;
            } 
            QProgressBar::chunk { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3b82f6, stop:1 #1d4ed8); 
                border-radius: 10px; 
            }
        ''')
        settings_progress.addWidget(self.progress)

        self.btn_split = QPushButton('✂️ Split Files')
        self.btn_split.setToolTip('Split the selected files into the specified number of parts')
        self.btn_split.setFixedHeight(36)
        self.btn_split.setStyleSheet('''
            QPushButton { 
                border-radius: 10px; 
                font-weight: bold; 
                font-size: 12pt; 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #dc2626, stop:1 #b91c1c); 
                color: #ffffff;
                border: none;
                padding: 0 20px;
            } 
            QPushButton:hover { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #b91c1c, stop:1 #991b1b); 
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #991b1b, stop:1 #7f1d1d);
            }
        ''')
        self.btn_split.clicked.connect(self.split_file)
        settings_progress.addWidget(self.btn_split)

        card_layout.addLayout(settings_progress)
        card.setLayout(card_layout)
        main_layout.addWidget(card)

        self.setLayout(main_layout)
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
            self.output_label.setText(f'📍 Output: {self.output_dir}')
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
