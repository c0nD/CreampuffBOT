from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QProgressBar, QLabel, QFileDialog, QTextEdit
from PyQt5.QtCore import Qt
import driver
import os

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setFixedSize(500, 350)

        # Layout
        layout = QVBoxLayout()

        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setRange(0,100)
        layout.addWidget(self.progress)

        # Status update text bar
        self.status = QTextEdit()
        self.status.setReadOnly(True)
        layout.addWidget(self.status)

        # Input path button
        self.input_button = QPushButton('Choose Input Folder')
        self.input_button.clicked.connect(self.choose_input)
        layout.addWidget(self.input_button)

        # Output path button
        self.output_button = QPushButton('Choose Output File')
        self.output_button.clicked.connect(self.choose_output)
        layout.addWidget(self.output_button)

        # Start process button
        self.start_button = QPushButton('Start Processing')
        self.start_button.clicked.connect(self.start_processing)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

        # Set up the stylesheet
        self.setStyleSheet("""
            QWidget {
                font: 12pt 'Segoe UI';
                background: #333;
                color: #CCC;
            }

            QProgressBar {
                border: 2px solid #CCC;
                border-radius: 5px;
                text-align: center;
            }

            QProgressBar::chunk {
                background-color: #88C;
                width: 1px;
            }

            QPushButton {
                border: 2px solid #88C;
                border-radius: 5px;
                padding: 5px;
                color: #88C;
                background: #555;
            }

            QPushButton:hover {
                background: #88C;
                color: #FFF;
            }

            QTextEdit {
                background: #555;
                border: 2px solid #88C;
                border-radius: 5px;
                color: #CCC;
            }
        """)

    def choose_input(self):
        self.input_dir = QFileDialog.getExistingDirectory(self, 'Choose Input Folder')
        self.status.append(f'Input folder: {self.input_dir}')

    def choose_output(self):
        self.output_file, _ = QFileDialog.getSaveFileName(self, 'Choose Output File', filter="CSV files (*.csv)")
        self.status.append(f'Output file: {self.output_file}')

    def start_processing(self):
        if hasattr(self, 'input_dir') and hasattr(self, 'output_file'):
            # Calculate the total number of images in the input directory
            total_images = len([name for name in os.listdir(self.input_dir) if os.path.isfile(os.path.join(self.input_dir, name))])
            self.progress.setRange(0, total_images)
            progress = 0
            self.status.append('Processing started...')
            def progress_callback():
                nonlocal progress
                progress += 1
                self.progress.setValue(progress)
            def status_callback(status):
                self.status.append(status)
            # Call process_images here, passing progress_callback and status_callback
            driver.process_images(self.input_dir, self.output_file, progress_callback, status_callback)
        else:
            self.status.append('Please choose an input folder and an output file before starting.')

app = QApplication([])
window = MainWindow()
window.setWindowTitle('CreampuffBOT')  # Set the window title to 'CreampuffBOT'
window.show()
app.exec_()
