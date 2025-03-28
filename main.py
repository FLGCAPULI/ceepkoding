import sys
import json
import random
from datetime import datetime
from PySide6.QtCore import (Qt, QTimer, QTime, QSettings, QUrl, QSize, 
                           QRect, QPoint, QEasingCurve, Property, QPropertyAnimation)
from PySide6.QtWidgets import QGraphicsOpacityEffect
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QHBoxLayout, QLabel, QPushButton, QProgressBar,
                              QSystemTrayIcon, QMenu, QDialog, QSpinBox,
                              QCheckBox, QFormLayout, QDialogButtonBox,
                              QSlider, QMessageBox, QStyle)
from PySide6.QtGui import (QIcon, QAction, QColor, QPalette, QPainter, 
                          QBrush, QConicalGradient, QFont, QFontDatabase, QPen)
from PySide6.QtMultimedia import QSoundEffect

# Motivational quotes and activity suggestions
MOTIVATIONAL_QUOTES = [
    "Stay focused and keep shipping!",
    "The secret of getting ahead is getting started.",
    "Productivity is never an accident.",
    "Concentrate all your thoughts upon the work at hand.",
    "Small daily improvements lead to stunning results."
]

STRETCHES = [
    "Stretch your arms overhead and hold for 10 seconds.",
    "Roll your shoulders backward 10 times.",
    "Touch your toes and hold for 15 seconds.",
    "Stretch your neck by tilting your head to each side.",
    "Do a seated spinal twist to loosen your back."
]

EYE_REST_TIPS = [
    "Look at something 20 feet away for 20 seconds.",
    "Close your eyes and take 10 deep breaths.",
    "Blink rapidly for a few seconds to moisten your eyes.",
    "Massage your temples to relieve eye strain.",
    "Do a quick eye-rolling exercise."
]

BREATHING_EXERCISES = [
    "Inhale for 4 seconds, hold for 7 seconds, exhale for 8 seconds.",
    "Take 5 deep belly breaths.",
    "Practice box breathing: Inhale, hold, exhale, hold (4 seconds each).",
    "Try alternate nostril breathing for 1 minute.",
    "Do a quick 5-5-5 breathing exercise: Inhale, hold, exhale (5 seconds each)."
]

SNACK_SUGGESTIONS = [
    "Grab a handful of nuts for a quick energy boost.",
    "Enjoy a piece of dark chocolate.",
    "Have a banana or an apple.",
    "Try some yogurt with honey.",
    "Munch on carrot sticks or cucumber slices."
]

POSTURE_TIPS = [
    "Sit up straight and align your ears with your shoulders.",
    "Adjust your chair so your feet are flat on the floor.",
    "Pull your shoulders back and relax them.",
    "Keep your screen at eye level to avoid neck strain.",
    "Engage your core muscles to support your back."
]

MEDITATION_PROMPTS = [
    "Close your eyes and focus on your breath for 1 minute.",
    "Visualize a peaceful place and relax for 2 minutes.",
    "Repeat a calming mantra like 'I am focused and calm.'",
    "Do a quick body scan to release tension.",
    "Listen to a guided meditation for 3 minutes."
]

MUSIC_SUGGESTIONS = [
    "Listen to your favorite upbeat song.",
    "Play some calming instrumental music.",
    "Try lo-fi beats to relax and focus.",
    "Enjoy a classical music piece.",
    "Dance to a fun tune for 2 minutes."
]

WATER_REMINDERS = [
    "Time to hydrate! Drink a glass of water.",
    "Stay refreshed with a sip of water.",
    "Your body needs water. Take a break and drink up.",
    "Hydration is key. Grab your water bottle.",
    "Don't forget to drink water to stay energized."
]

PHYSICAL_ACTIVITIES = [
    "Do 10 jumping jacks to get your blood flowing.",
    "Try 5 squats to stretch your legs.",
    "Take a quick walk around the room.",
    "Do a 1-minute plank to strengthen your core.",
    "Stretch your arms and legs with a quick yoga pose."
]

COFFEE_TEA_BREAKS = [
    "Brew a cup of your favorite tea.",
    "Enjoy a sip of coffee to recharge.",
    "Try a herbal tea for a calming break.",
    "Make a latte and savor the moment.",
    "Take a moment to enjoy your favorite beverage."
]

class CircularProgress(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self.width = 200
        self.height = 200
        self.progress_width = 10
        self.progress_rounded_cap = True
        self.progress_color = QColor(0, 122, 204)
        self.max_value = 100
        self.text = "25:00"
        self.setFixedSize(self.width, self.height)
        self.is_hovered = False
        self.timer_active = False
        
        # Create circular buttons
        self.start_btn = QPushButton("", self)
        self.start_btn.setFixedSize(120, 120)
        self.start_btn.setStyleSheet("""
            QPushButton {
                border-radius: 60px;
                background-color: #0078D4;
                color: white;
                border: none;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #106EBE;
            }
            QPushButton:pressed {
                background-color: #005A9E;
            }
        """)
        # Add play text
        self.start_btn.setText("START")
        self.start_btn.setFont(QFont("Arial", 16))
        self.start_btn.hide()
        
        self.pause_btn = QPushButton("", self)
        self.pause_btn.setFixedSize(120, 120)
        self.pause_btn.setStyleSheet("""
            QPushButton {
                border-radius: 60px;
                background-color: #0078D4;
                color: white;
                border: none;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #106EBE;
            }
            QPushButton:pressed {
                background-color: #005A9E;
            }
        """)
        # Add pause text
        self.pause_btn.setText("PAUSE")
        self.pause_btn.setFont(QFont("Arial", 16))
        self.pause_btn.hide()
        self.start_btn.move(self.width//2 - 60, self.height//2 - 60)
        self.pause_btn.move(self.width//2 - 60, self.height//2 - 60)
        
        # Install event filter for hover detection
        self.setMouseTracking(True)

    def _get_value(self):
        return self._value

    def _set_value(self, value):
        self._value = value
        self.update()

    def set_value(self, value):
        # Simple direct update without animation
        self._value = value
        self.update()

    def set_text(self, text):
        self.text = text
        self.update()
    
    def set_timer_active(self, active):
        self.timer_active = active
        self.update()
        
    def enterEvent(self, event):
        self.is_hovered = True
        if self.timer_active:
            # Show pause button when timer is active
            self.pause_btn.setText("PAUSE")
            self.fade_in_animation(self.pause_btn)
            self.start_btn.hide()  # Hide start button when timer is active
        else:
            # Show start button when timer is inactive
            self.start_btn.setText("START")
            self.fade_in_animation(self.start_btn)
            self.pause_btn.hide()  # Hide pause button when timer is inactive
        self.update()
        
    def fade_in_animation(self, button):
        # Create opacity effect for fade in
        self.effect = QGraphicsOpacityEffect(button)
        button.setGraphicsEffect(self.effect)
        
        # Create the animation
        self.anim = QPropertyAnimation(self.effect, b"opacity")
        self.anim.setDuration(200)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()
        
        # Show the button
        button.show()
        
    def leaveEvent(self, event):
        self.is_hovered = False
        self.start_btn.hide()
        self.pause_btn.hide()
        self.update()
        
    def paintEvent(self, event):
        width = self.width - self.progress_width
        height = self.height - self.progress_width
        margin = self.progress_width / 2
        value = self._value * 360 / self.max_value

        paint = QPainter(self)
        paint.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create rect for drawing
        rect = QRect(margin, margin, width, height)

        # Set pen for drawing the progress arc
        pen = QPen()
        pen.setWidth(self.progress_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap if self.progress_rounded_cap else Qt.PenCapStyle.SquareCap)
        pen.setColor(self.progress_color)
        paint.setPen(pen)

        # Draw background track
        background_pen = QPen()
        background_pen.setWidth(self.progress_width)
        background_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        background_pen.setColor(QColor(62, 62, 66, 50))
        paint.setPen(background_pen)
        paint.drawArc(rect, 0, 360 * 16)
        
        # Draw progress arc
        pen = QPen()
        pen.setWidth(self.progress_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap if self.progress_rounded_cap else Qt.PenCapStyle.SquareCap)
        pen.setColor(self.progress_color)
        paint.setPen(pen)

        # Draw the progress arc
        paint.drawArc(rect, -90 * 16, -value * 16)
        
        # Draw the timer text in the center
        font = paint.font()
        font.setPointSize(24)
        font.setBold(True)
        paint.setFont(font)
        paint.setPen(QColor(189, 189, 189))  # Same color as the timer label
        paint.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text)

        # End painting
        paint.end()

class CeepKoding(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CeepKoding")
        self.setFixedSize(300, 400)
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DesktopIcon))
        
        # Initialize state
        self.settings = QSettings("CeepKoding", "Settings")
        self.timer = QTimer(self)
        self.current_time = QTime(0, 25, 0)
        self.is_paused = False
        self.session_type = "Pomodoro"
        self.completed_pomodoros = 0
        self.alarm_active = False
        
        # Sound effects
        self.alert_sound = QSoundEffect()
        self.alert_sound.setSource(QUrl.fromLocalFile("alert.wav"))
        self.alert2_sound = QSoundEffect()
        self.alert2_sound.setSource(QUrl.fromLocalFile("alert2.wav"))
        self.complete_sound = QSoundEffect()
        self.complete_sound.setSource(QUrl.fromLocalFile("complete.wav"))
        self.start_sound = QSoundEffect()
        self.start_sound.setSource(QUrl.fromLocalFile("start.wav"))
        
        # Initialize UI
        self.init_ui()
        self.load_settings()
        self.apply_dark_theme(self.settings.value("dark_mode", True, bool))
        self.update_display()

        # Timer setup
        self.timer.timeout.connect(self.update_timer)
        
        # System tray
        self.init_system_tray()
        
        # Keyboard shortcuts
        self.init_shortcuts()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        # Set window style
        self.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                background-color: #0078D4;
                color: white;
                border: none;
                font-weight: bold;
                transition: background-color 0.3s;
            }
            QPushButton:hover {
                background-color: #106EBE;
            }
            QPushButton:pressed {
                background-color: #005A9E;
            }
            QPushButton:disabled {
                background-color: #C8C8C8;
            }
            QLabel {
                color: #ADADAD;
                transition: color 0.3s;
            }
            #alarmButton {
                padding: 15px 20px;
                font-size: 16px;
                background-color: #D83B01;
            }
            #alarmButton:hover {
                background-color: #F25022;
            }
        """)

        # Circular progress with integrated timer display
        self.progress = CircularProgress()
        self.main_layout.addWidget(self.progress, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Connect the circular buttons to timer functions
        self.progress.start_btn.clicked.connect(self.start_timer)
        self.progress.pause_btn.clicked.connect(self.pause_timer)
        
        # Only keep reset button centered below the circle
        self.reset_btn = QPushButton("Reset", clicked=self.reset_timer)
        self.main_layout.addWidget(self.reset_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Alarm button (hidden by default)
        self.alarm_btn = QPushButton("Stop Alarm & Continue", clicked=self.stop_alarm_and_continue)
        self.alarm_btn.setObjectName("alarmButton")
        self.alarm_btn.hide()
        self.main_layout.addWidget(self.alarm_btn)

        # Menu
        menu = self.menuBar()
        settings_menu = menu.addMenu("Settings")
        settings_action = QAction("Preferences", self, triggered=self.show_settings)
        self.dark_mode_action = QAction("Dark Mode", self, checkable=True, 
                                      toggled=lambda: self.toggle_dark_mode())
        settings_menu.addAction(settings_action)
        settings_menu.addAction(self.dark_mode_action)

    def init_system_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.windowIcon())
        
        menu = QMenu()
        show_action = QAction("Show", self, triggered=self.show)
        quit_action = QAction("Quit", self, triggered=self.close)
        menu.addAction(show_action)
        menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    def init_shortcuts(self):
        self.start_shortcut = QAction(self)
        self.start_shortcut.setShortcut("Ctrl+S")
        self.start_shortcut.triggered.connect(self.start_timer)
        self.addAction(self.start_shortcut)
        
        self.pause_shortcut = QAction(self)
        self.pause_shortcut.setShortcut("Ctrl+P")
        self.pause_shortcut.triggered.connect(self.pause_timer)
        self.addAction(self.pause_shortcut)
        
        self.reset_shortcut = QAction(self)
        self.reset_shortcut.setShortcut("Ctrl+R")
        self.reset_shortcut.triggered.connect(self.reset_timer)
        self.addAction(self.reset_shortcut)

    def apply_dark_theme(self, enable):
        dark_palette = QPalette()
        if enable:
            dark_palette.setColor(QPalette.ColorRole.Window, QColor(45, 45, 48))
            dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 26))
            dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.Button, QColor(62, 62, 66))
            dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 122, 204))
            dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        self.setPalette(dark_palette if enable else self.style().standardPalette())
        
        # Fade back in
        fade_in = QPropertyAnimation(self, b"windowOpacity")
        fade_in.setDuration(200)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.start()

    def toggle_dark_mode(self):
        self.settings.setValue("dark_mode", self.dark_mode_action.isChecked())
        self.apply_dark_theme(self.dark_mode_action.isChecked())

    def start_timer(self):
        if not self.timer.isActive():
            self.timer.start(1000)
            self.is_paused = False
            self.progress.set_timer_active(True)
            # Update button text to pause
            self.progress.pause_btn.setText("PAUSE")

    def pause_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.is_paused = True
            self.progress.set_timer_active(False)
            # Update button text to show resume
            self.progress.pause_btn.setText("RESUME")
        else:
            self.is_paused = False
            self.timer.start(1000)
            self.progress.set_timer_active(True)
            # Update button text back to pause
            self.progress.pause_btn.setText("PAUSE")

    def reset_timer(self):
        self.timer.stop()
        self.current_time = QTime(0, self.get_current_duration(), 0)
        self.update_display()
        self.progress.set_timer_active(False)

    def update_timer(self):
        self.current_time = self.current_time.addSecs(-1)
        self.update_display()
        
        if self.current_time == QTime(0, 0, 0):
            self.timer.timeout.disconnect()
            self.session_complete()

    def session_complete(self):
        self.play_sound()
        self.show_notification()
        self.show_activity_suggestion()
        
        # Bring app to foreground
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
        self.show()
        self.activateWindow()
        
        # Show alarm button and hide timer controls
        self.alarm_active = True
        self.progress.hide()
        self.alarm_btn.show()
        self.reset_btn.setEnabled(False)
        self.progress.set_timer_active(False)

    def show_activity_suggestion(self):
        if self.session_type == "Pomodoro":
            activity = random.choice([
                random.choice(STRETCHES),
                random.choice(EYE_REST_TIPS),
                random.choice(BREATHING_EXERCISES),
                random.choice(SNACK_SUGGESTIONS),
                random.choice(POSTURE_TIPS),
                random.choice(MEDITATION_PROMPTS),
                random.choice(MUSIC_SUGGESTIONS),
                random.choice(WATER_REMINDERS),
                random.choice(PHYSICAL_ACTIVITIES),
                random.choice(COFFEE_TEA_BREAKS)
            ])
            self.tray_icon.showMessage(
                "Activity Suggestion",
                activity,
                QSystemTrayIcon.MessageIcon.Information,
                5000
            )

    def switch_session_type(self):
        # Switch session type directly
        self._update_session_type()
        
    def stop_alarm_and_continue(self):
        # Stop the alarm sound
        if self.session_type == "Pomodoro":
            self.alert_sound.stop()
            self.complete_sound.play()
            # Switch to break session
            self.switch_session_type()
        else:
            self.alert2_sound.stop()
            self.start_sound.play()
            # Switch to pomodoro session
            self.switch_session_type()
            
        # Show timer again and hide alarm button
        self.alarm_active = False
        self.progress.show()
        self.alarm_btn.hide()
        self.reset_btn.setEnabled(True)
        
        # Connect timer and start if auto-restart is enabled
        self.timer.timeout.connect(self.update_timer)
        if self.settings.value("auto_restart", False, bool):
            self.start_timer()
        else:
            # Ensure timer is in inactive state if not auto-restarting
            self.progress.set_timer_active(False)

    def _update_session_type(self):
        if self.session_type == "Pomodoro":
            self.completed_pomodoros += 1
            if self.completed_pomodoros % self.settings.value("pomodoros_before_long", 4, int) == 0:
                self.session_type = "Long Break"
                self.current_time = QTime(0, self.settings.value("long_break", 15, int), 0)
            else:
                self.session_type = "Short Break"
                self.current_time = QTime(0, self.settings.value("short_break", 5, int), 0)
        else:
            self.session_type = "Pomodoro"
            self.current_time = QTime(0, self.settings.value("pomodoro", 25, int), 0)
        
        # Update display
        self.update_display()

    def apply_dark_theme(self, enable):
        # Create fade effect for theme transition
        fade = QPropertyAnimation(self, b"windowOpacity")
        fade.setDuration(200)
        fade.setStartValue(1.0)
        fade.setEndValue(0.0)
        fade.finished.connect(lambda: self._complete_theme_change(enable))
        fade.start()

    def _complete_theme_change(self, enable):
        dark_palette = QPalette()
        if enable:
            dark_palette.setColor(QPalette.ColorRole.Window, QColor(45, 45, 48))
            dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 26))
            dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.Button, QColor(62, 62, 66))
            dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 122, 204))
            dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        self.setPalette(dark_palette if enable else self.style().standardPalette())
        
        # Fade back in
        fade_in = QPropertyAnimation(self, b"windowOpacity")
        fade_in.setDuration(200)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.start()

    def play_sound(self):
        if self.settings.value("sound_enabled", True, bool):
            if self.session_type == "Pomodoro":
                self.alert_sound.play()
            else:
                self.alert2_sound.play()

    def show_notification(self):
        self.tray_icon.showMessage(
            "Session Complete",
            f"{self.session_type} finished!",
            QSystemTrayIcon.MessageIcon.Information,
            3000
        )

    def update_display(self):
        time_text = self.current_time.toString("mm:ss")
        self.progress.set_text(time_text)
        total_seconds = self.get_current_duration() * 60
        remaining = self.current_time.minute() * 60 + self.current_time.second()
        self.progress.set_value(int((1 - remaining/total_seconds) * 100))

    def get_current_duration(self):
        return {
            "Pomodoro": self.settings.value("pomodoro", 25, int),
            "Short Break": self.settings.value("short_break", 5, int),
            "Long Break": self.settings.value("long_break", 15, int)
        }[self.session_type]

    def show_settings(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Preferences")
        layout = QFormLayout(dialog)

        pomodoro_spin = QSpinBox()
        pomodoro_spin.setRange(1, 60)
        pomodoro_spin.setValue(self.settings.value("pomodoro", 25, int))
        
        short_break_spin = QSpinBox()
        short_break_spin.setRange(1, 30)
        short_break_spin.setValue(self.settings.value("short_break", 5, int))
        
        long_break_spin = QSpinBox()
        long_break_spin.setRange(1, 60)
        long_break_spin.setValue(self.settings.value("long_break", 15, int))
        
        pomodoros_before_spin = QSpinBox()
        pomodoros_before_spin.setRange(1, 10)
        pomodoros_before_spin.setValue(self.settings.value("pomodoros_before_long", 4, int))

        auto_restart_check = QCheckBox("Auto restart sessions")
        auto_restart_check.setChecked(self.settings.value("auto_restart", False, bool))

        sound_check = QCheckBox("Enable sound notifications")
        sound_check.setChecked(self.settings.value("sound_enabled", True, bool))

        layout.addRow("Pomodoro (min):", pomodoro_spin)
        layout.addRow("Short Break (min):", short_break_spin)
        layout.addRow("Long Break (min):", long_break_spin)
        layout.addRow("Pomodoros before long break:", pomodoros_before_spin)
        layout.addRow(auto_restart_check)
        layout.addRow(sound_check)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(lambda: self.save_settings(
            pomodoro_spin.value(),
            short_break_spin.value(),
            long_break_spin.value(),
            pomodoros_before_spin.value(),
            auto_restart_check.isChecked(),
            sound_check.isChecked()
        ))
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        dialog.exec()

    def save_settings(self, pomodoro, short_break, long_break, pomodoros_before, auto_restart, sound_enabled):
        self.settings.setValue("pomodoro", pomodoro)
        self.settings.setValue("short_break", short_break)
        self.settings.setValue("long_break", long_break)
        self.settings.setValue("pomodoros_before_long", pomodoros_before)
        self.settings.setValue("auto_restart", auto_restart)
        self.settings.setValue("sound_enabled", sound_enabled)
        self.reset_timer()

    def load_settings(self):
        self.dark_mode_action.setChecked(self.settings.value("dark_mode", True, bool))

    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        if self.settings.contains("geometry"):
            self.restoreGeometry(self.settings.value("geometry"))
        if self.settings.contains("windowState"):
            self.restoreState(self.settings.value("windowState"))
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CeepKoding()
    window.show()
    sys.exit(app.exec())