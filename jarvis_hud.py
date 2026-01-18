# jarvis_hud_fixed.py
# Futuristic Stark-style HUD UI with Dark Mode, Voice Reply, and System Stats

import sys
import psutil
import threading

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QTextEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from input.voice_input import listen_from_mic
from core.command_processor import process_command

# ---------------- Voice Engine (THREAD-SAFE) ----------------
import pyttsx3

class VoiceEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)
        self.lock = threading.Lock()

    def speak(self, text: str):
        if not text:
            return

        def _speak():
            with self.lock:
                self.engine.say(text)
                self.engine.runAndWait()

        threading.Thread(target=_speak, daemon=True).start()


# ---------------- Main Window ----------------
class JarvisHUD(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("STARK_IND_OS v4.2")
        self.setGeometry(100, 100, 1200, 700)

        self.voice = VoiceEngine()
        self.dark_mode = True

        self.init_ui()
        self.apply_dark_mode()

        # System stats timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)

    # ---------------- UI Layout ----------------
    def init_ui(self):
        central = QWidget(self)
        self.setCentralWidget(central)

        main_layout = QGridLayout(central)

        # Header
        self.header = QLabel("STARK_IND_OS v4.2  |  CORE ONLINE")
        self.header.setFont(QFont("Orbitron", 16))
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.header, 0, 0, 1, 3)

        # Left stats panel
        self.cpu = QProgressBar()
        self.ram = QProgressBar()
        self.net = QProgressBar()

        for bar in (self.cpu, self.ram, self.net):
            bar.setMaximum(100)

        stats_layout = QVBoxLayout()
        stats_layout.addWidget(QLabel("CPU Usage"))
        stats_layout.addWidget(self.cpu)
        stats_layout.addWidget(QLabel("RAM Usage"))
        stats_layout.addWidget(self.ram)
        stats_layout.addWidget(QLabel("Network Activity"))
        stats_layout.addWidget(self.net)

        stats_widget = QWidget()
        stats_widget.setLayout(stats_layout)
        main_layout.addWidget(stats_widget, 1, 0)

        # Center HUD display
        self.core_display = QLabel("◉ SYSTEMS ONLINE ◉\nAwaiting Command…")
        self.core_display.setFont(QFont("Orbitron", 14))
        self.core_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.core_display, 1, 1)

        # Right chat panel
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.append("Jarvis: Systems online, Sir. How can I assist you today?")
        main_layout.addWidget(self.chat, 1, 2)

        # Bottom controls
        self.listen_btn = QPushButton("🎤 Listen")
        self.listen_btn.clicked.connect(self.listen_action)

        self.dark_btn = QPushButton("🌙 Toggle Dark Mode")
        self.dark_btn.clicked.connect(self.toggle_dark_mode)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.listen_btn)
        bottom_layout.addWidget(self.dark_btn)

        bottom_widget = QWidget()
        bottom_widget.setLayout(bottom_layout)
        main_layout.addWidget(bottom_widget, 2, 0, 1, 3)

    # ---------------- Actions ----------------
    def listen_action(self):
        # Update UI: Listening
        self.core_display.setText("🎤 Listening…")
        QApplication.processEvents()

        # Voice input
        command = listen_from_mic()
        self.chat.append(f"You: {command}")

        # Processing
        self.core_display.setText("⚙ Processing…")
        QApplication.processEvents()

        result = process_command(command)

        # Output
        self.chat.append(f"Jarvis: {result}")
        self.core_display.setText("✅ Command Executed")

        self.voice.speak(result)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.apply_dark_mode()

    # ---------------- Styling ----------------
    def apply_dark_mode(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QWidget { background-color: #0b0f14; color: #00e5ff; }
                QProgressBar { border: 1px solid #00e5ff; text-align: center; }
                QProgressBar::chunk { background-color: #00e5ff; }
                QPushButton { background-color: #111820; border: 1px solid #00e5ff; padding: 6px; }
                QTextEdit { background-color: #05080c; border: 1px solid #00e5ff; }
            """)
        else:
            self.setStyleSheet("")

    # ---------------- Stats ----------------
    def update_stats(self):
        self.cpu.setValue(int(psutil.cpu_percent()))
        self.ram.setValue(int(psutil.virtual_memory().percent))
        self.net.setValue(int(psutil.net_io_counters().bytes_sent % 100))


# ---------------- App Entry ----------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = JarvisHUD()
    window.show()
    sys.exit(app.exec())