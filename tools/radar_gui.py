"""
Radar Ultrasónico -- PySide6 Valorant Green Edition
"""

import sys
import math

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QSlider, QLabel, QSpinBox, QCheckBox,
    QFrame, QSizePolicy, QMessageBox,
)
from PySide6.QtCore import Qt, QTimer, QByteArray, Signal
from PySide6.QtGui import (
    QPainter, QColor, QFont, QPixmap, QPen, QBrush, QRadialGradient,
)
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo

# ───────────────────────────────────────────────
# CONSTANTS
# ───────────────────────────────────────────────
GREEN_PHOSPHOR = QColor(0, 255, 136)
GREEN_BRIGHT = QColor(180, 255, 200)
GREEN_DIM = QColor(0, 180, 96)
GREEN_DARK = QColor(0, 60, 35)
GREEN_GLOW_10 = QColor(0, 255, 136, 10)
GREEN_GLOW_20 = QColor(0, 255, 136, 20)

RED_ALERT = QColor(255, 68, 85)

BG_PRIMARY = QColor(10, 18, 28)
BG_RADAR = QColor(8, 14, 22)

TEXT_LIGHT = QColor(220, 218, 214)
TEXT_DIM = QColor(110, 120, 118)

TRAIL_ALPHA = 12
FPS = 60
SWEEP_SPEED_MIN = 5
SWEEP_SPEED_MAX = 200
THRESHOLD_MIN = 2
THRESHOLD_MAX = 100

VALORANT_QSS = """
QMainWindow {
    background-color: #0A1118;
}

QLabel {
    background: transparent;
    font-size: 14px;
    color: #E4E8E3;
}
QLabel#titleLabel {
    font-size: 26px;
    font-weight: 900;
    color: #00FF88;
    letter-spacing: 2.5px;
}
QLabel#headerTitle {
    font-size: 51px;
    font-weight: 900;
    color: #00FF88;
    letter-spacing: 3.5px;
}
QLabel#valueLabel {
    color: #00FF88;
    font-weight: 700;
    font-size: 15px;
}
QLabel#statusLabel {
    color: #B2BCB7;
    font-size: 13px;
}
QLabel#statusLight {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 6px 12px;
    border-radius: 3px;
}

QComboBox {
    background-color: #1A2635;
    color: #F0F3EF;
    border: 1px solid #00FF8866;
    border-radius: 4px;
    padding: 8px 10px 8px 12px;
    font-size: 14px;
    min-height: 34px;
}
QComboBox:hover {
    border: 1px solid #00FF88;
    background-color: #1E2C3E;
}
QComboBox:focus {
    border: 1px solid #00FF88;
}
QComboBox:disabled {
    background-color: #0E1620;
    color: #4A5A56;
    border: 1px solid #2A3A3A;
}
QComboBox::drop-down {
    border: none;
    width: 26px;
}
QComboBox QAbstractItemView {
    background-color: #1A2635;
    color: #E0DDD8;
    border: 1px solid #00FF88;
    selection-background-color: #00FF88;
    selection-color: #0A1118;
    outline: none;
}

QPushButton {
    background-color: transparent;
    color: #00FF88;
    border: 1px solid #00FF88;
    border-radius: 4px;
    padding: 9px 20px;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 1px;
}
QPushButton:hover {
    background-color: #00FF8818;
}
QPushButton:pressed {
    background-color: #00FF8840;
}
QPushButton:disabled {
    color: #4A5A56;
    border: 1px solid #2A3A3A;
}

QPushButton#connectBtn {
    background-color: #FFFFFF;
    color: #0A1118;
    font-weight: 800;
    font-size: 16px;
    border: 2px solid #00FF88;
    border-radius: 4px;
    padding: 12px 20px;
    letter-spacing: 2px;
}
QPushButton#connectBtn:hover {
    background-color: #E8FFEE;
    border: 2px solid #33FFAA;
}
QPushButton#connectBtn:pressed {
    background-color: #CCEED8;
}
QPushButton#connectBtn:disabled {
    background-color: #1A2A22;
    color: #4A6A5A;
    border: 2px solid #1A3A2A;
}

QPushButton#refreshBtn {
    min-width: 40px;
    max-width: 40px;
    min-height: 36px;
    max-height: 36px;
    padding: 0;
    font-size: 16px;
    font-weight: 800;
    border: 1px solid #00FF8866;
}
QPushButton#refreshBtn:hover {
    border: 1px solid #00FF88;
}

QSlider::groove:horizontal {
    border: none;
    height: 4px;
    background: #1A2635;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #00FF88;
    border: 2px solid #1A2635;
    width: 18px;
    height: 18px;
    margin: -8px 0;
    border-radius: 9px;
}
QSlider::handle:horizontal:hover {
    background: #33FFAA;
}
QSlider::sub-page:horizontal {
    background: #00FF88;
    border-radius: 2px;
}

QSpinBox {
    background-color: #1A2635;
    color: #00FF88;
    border: 1px solid #00FF8866;
    border-radius: 4px;
    padding: 5px 8px;
    font-size: 14px;
    font-weight: 700;
    min-height: 34px;
}
QSpinBox:hover {
    border: 1px solid #00FF88;
}
QSpinBox:focus {
    border: 1px solid #00FF88;
}
QSpinBox:disabled {
    background-color: #0E1620;
    border: 1px solid #2A3A3A;
    color: #4A5A56;
}

QCheckBox {
    color: #E4E8E3;
    font-size: 14px;
    spacing: 10px;
}
QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border: 1.5px solid #00FF8866;
    border-radius: 4px;
    background: #1A2635;
}
QCheckBox::indicator:hover {
    border: 1.5px solid #00FF88;
}
QCheckBox::indicator:checked {
    background: #00FF88;
    border: 1.5px solid #00FF88;
}

QFrame#divider {
    background-color: #00FF8822;
    max-height: 1px;
    min-height: 1px;
}
"""

# ───────────────────────────────────────────────
# RADAR WIDGET
# ───────────────────────────────────────────────
class RadarWidget(QWidget):
    new_data = Signal(int, int)

    def __init__(self):
        super().__init__()
        self.setMinimumSize(500, 400)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.buffer = QPixmap()
        self.angle = 0
        self.distance = 200
        self.object_active = False
        self.scan_points = []

        self.trail_alpha = TRAIL_ALPHA
        self.sweep_speed = 30

        self._last_angle = 0
        self._last_distance = 200

    @property
    def cx(self):
        return self.width() / 2.0

    @property
    def cy(self):
        return self.height() * 0.82

    @property
    def radio_max(self):
        return min(self.width(), self.height()) * 0.70

    def set_angle(self, a):
        self._last_angle = self.angle
        self.angle = max(0, min(180, a))

    def set_distance(self, d):
        self._last_distance = self.distance
        self.distance = max(0, min(200, d))
        self.object_active = self.distance < 200

    def add_scan_point(self, angle, distance):
        if distance < 200:
            self.scan_points.append((angle, distance))
            if len(self.scan_points) > 300:
                self.scan_points.pop(0)

    def clear_scan_points(self):
        self.scan_points.clear()

    def paintEvent(self, event):
        if self.buffer.size() != self.size():
            self.buffer = QPixmap(self.size())
            self.buffer.fill(BG_RADAR)

        p = QPainter(self.buffer)
        p.setRenderHint(QPainter.Antialiasing)

        p.setCompositionMode(QPainter.CompositionMode_SourceOver)
        p.fillRect(self.rect(), QColor(8, 14, 22, self.trail_alpha))

        self._draw_radar_grid(p)
        self._draw_scan_points(p)
        self._draw_sweep_beam(p)
        self._draw_object_line(p)

        p.end()

        screen = QPainter(self)
        screen.drawPixmap(0, 0, self.buffer)
        screen.end()

    def _draw_radar_grid(self, p):
        p.save()
        p.translate(self.cx, self.cy)

        grid_pen = QPen(QColor(0, 255, 136, 80), 1.0)
        grid_pen.setStyle(Qt.DotLine)
        p.setPen(grid_pen)
        p.setBrush(Qt.NoBrush)

        ranges = [0.25, 0.50, 0.75, 1.0]
        for r in ranges:
            d = self.radio_max * r * 2
            p.drawArc(int(-d / 2), int(-d / 2), int(d), int(d),
                      180 * 16, 180 * 16)

        solid_pen = QPen(QColor(0, 255, 136, 60), 1.0)
        p.setPen(solid_pen)
        p.drawLine(int(-self.radio_max), 0, int(self.radio_max), 0)

        angles = [30, 60, 90, 120, 150]
        for a in angles:
            rad = math.radians(a)
            x = -self.radio_max * math.cos(rad)
            y = -self.radio_max * math.sin(rad)
            p.drawLine(0, 0, int(x), int(y))

        p.restore()

        p.setPen(QColor(0, 255, 136, 100))
        font_small = QFont("Segoe UI", 11)
        p.setFont(font_small)

        range_labels = ["50cm", "100cm", "150cm", "200cm"]
        for i, r in enumerate(ranges):
            rx = self.cx + self.radio_max * r + 5
            ry = self.cy - 4
            label_width = p.fontMetrics().horizontalAdvance(range_labels[i])
            if rx + label_width > self.width() - 8:
                rx = self.width() - label_width - 8
            p.drawText(int(rx), int(ry), range_labels[i])

        deg_font = QFont("Segoe UI", 12)
        p.setFont(deg_font)
        for a in angles:
            rad = math.radians(a)
            lx = self.cx - (self.radio_max + 22) * math.cos(rad)
            ly = self.cy - (self.radio_max + 22) * math.sin(rad)
            p.save()
            p.translate(lx, ly)
            p.rotate(-(90 - a))
            p.drawText(int(-8), int(4), f"{a}°")
            p.restore()

    def _draw_sweep_beam(self, p):
        p.save()
        p.translate(self.cx, self.cy)

        rad = math.radians(self.angle)
        ex = -self.radio_max * math.cos(rad)
        ey = -self.radio_max * math.sin(rad)

        glow_pen = QPen(QColor(0, 255, 136, 18), 8)
        glow_pen.setCapStyle(Qt.RoundCap)
        p.setPen(glow_pen)
        p.drawLine(0, 0, int(ex), int(ey))

        core_pen = QPen(GREEN_BRIGHT, 2.0)
        core_pen.setCapStyle(Qt.RoundCap)
        p.setPen(core_pen)
        p.drawLine(0, 0, int(ex), int(ey))

        p.restore()

    def _draw_object_line(self, p):
        if not self.object_active:
            return

        p.save()
        p.translate(self.cx, self.cy)

        rad = math.radians(self.angle)
        dist_px = (self.distance / 200.0) * self.radio_max

        obj_x = -dist_px * math.cos(rad)
        obj_y = -dist_px * math.sin(rad)
        edge_x = -self.radio_max * math.cos(rad)
        edge_y = -self.radio_max * math.sin(rad)

        line_pen = QPen(RED_ALERT, 3)
        line_pen.setCapStyle(Qt.RoundCap)
        p.setPen(line_pen)
        p.drawLine(int(obj_x), int(obj_y), int(edge_x), int(edge_y))

        p.restore()

    def _draw_scan_points(self, p):
        if not self.scan_points:
            return

        p.save()
        p.translate(self.cx, self.cy)

        count = len(self.scan_points)
        for i, (angle, dist) in enumerate(self.scan_points):
            rad = math.radians(angle)
            dist_px = (dist / 200.0) * self.radio_max
            x = -dist_px * math.cos(rad)
            y = -dist_px * math.sin(rad)

            age_ratio = i / max(count, 1)
            alpha = max(15, int(160 * (1 - age_ratio)))
            size = 2.5 if age_ratio < 0.7 else 1.5

            dot_pen = QPen(QColor(0, 255, 136, alpha), size)
            dot_pen.setCapStyle(Qt.RoundCap)
            p.setPen(dot_pen)
            p.drawPoint(int(x), int(y))

        p.restore()


# ───────────────────────────────────────────────
# CONTROL PANEL
# ───────────────────────────────────────────────
class ControlPanel(QFrame):
    connect_requested = Signal(str, int)
    disconnect_requested = Signal()
    param_changed = Signal(str, int)
    mute_toggled = Signal(bool)
    pause_toggled = Signal(bool)

    def __init__(self):
        super().__init__()
        self.setObjectName("controlPanel")
        self.setStyleSheet("background-color: #111B28; border: none;")
        self.setFixedWidth(320)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 24, 20, 24)
        layout.setSpacing(14)

        title = QLabel("CONTROLES")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(4)
        layout.addWidget(self._divider())
        layout.addSpacing(4)

        layout.addWidget(self._section_title("PUERTO SERIE"))
        port_row = QHBoxLayout()
        port_row.setSpacing(6)

        self.port_combo = QComboBox()
        self.port_combo.setMinimumWidth(130)
        port_row.addWidget(self.port_combo)

        self.refresh_btn = QPushButton("R")
        self.refresh_btn.setObjectName("refreshBtn")
        self.refresh_btn.setToolTip("Actualizar puertos")
        self.refresh_btn.clicked.connect(self.refresh_ports)
        port_row.addWidget(self.refresh_btn)

        layout.addLayout(port_row)

        self.connect_btn = QPushButton("CONECTAR")
        self.connect_btn.setObjectName("connectBtn")
        self.connect_btn.clicked.connect(self._on_connect_click)
        layout.addWidget(self.connect_btn)

        self.status_indicator = QLabel("DESCONECTADO")
        self.status_indicator.setObjectName("statusLight")
        self.status_indicator.setAlignment(Qt.AlignCenter)
        self.status_indicator.setStyleSheet(
            "background-color: #2A0A14; color: #FF4455; "
            "border: 1px solid #FF445544; font-weight: 700; "
            "letter-spacing: 1px; font-size: 13px; padding: 6px 12px; "
            "border-radius: 3px;"
        )
        layout.addWidget(self.status_indicator)

        layout.addSpacing(8)
        layout.addWidget(self._divider())
        layout.addSpacing(4)

        layout.addWidget(self._section_title("PARÁMETROS"))

        speed_group = QVBoxLayout()
        speed_group.setSpacing(2)
        speed_label_row = QHBoxLayout()
        speed_label_row.addWidget(QLabel("Velocidad"))
        self.speed_value = QLabel("30 ms")
        self.speed_value.setObjectName("valueLabel")
        self.speed_value.setAlignment(Qt.AlignRight)
        speed_label_row.addWidget(self.speed_value)
        speed_group.addLayout(speed_label_row)

        speed_slider_row = QHBoxLayout()
        speed_slider_row.setSpacing(8)
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(SWEEP_SPEED_MIN, SWEEP_SPEED_MAX)
        self.speed_slider.setValue(30)
        self.speed_slider.valueChanged.connect(self._on_speed_change)
        speed_slider_row.addWidget(self.speed_slider)

        self.speed_spin = QSpinBox()
        self.speed_spin.setRange(SWEEP_SPEED_MIN, SWEEP_SPEED_MAX)
        self.speed_spin.setValue(30)
        self.speed_spin.setSuffix(" ms")
        self.speed_spin.setFixedWidth(82)
        self.speed_spin.valueChanged.connect(self._on_speed_spin)
        speed_slider_row.addWidget(self.speed_spin)
        speed_group.addLayout(speed_slider_row)
        layout.addLayout(speed_group)

        thresh_group = QVBoxLayout()
        thresh_group.setSpacing(2)
        thresh_label_row = QHBoxLayout()
        thresh_label_row.addWidget(QLabel("Umbral de alerta"))
        self.thresh_value = QLabel("5 cm")
        self.thresh_value.setObjectName("valueLabel")
        self.thresh_value.setAlignment(Qt.AlignRight)
        thresh_label_row.addWidget(self.thresh_value)
        thresh_group.addLayout(thresh_label_row)

        thresh_slider_row = QHBoxLayout()
        thresh_slider_row.setSpacing(8)
        self.thresh_slider = QSlider(Qt.Horizontal)
        self.thresh_slider.setRange(THRESHOLD_MIN, THRESHOLD_MAX)
        self.thresh_slider.setValue(5)
        self.thresh_slider.valueChanged.connect(self._on_thresh_change)
        thresh_slider_row.addWidget(self.thresh_slider)

        self.thresh_spin = QSpinBox()
        self.thresh_spin.setRange(THRESHOLD_MIN, THRESHOLD_MAX)
        self.thresh_spin.setValue(5)
        self.thresh_spin.setSuffix(" cm")
        self.thresh_spin.setFixedWidth(82)
        self.thresh_spin.valueChanged.connect(self._on_thresh_spin)
        thresh_slider_row.addWidget(self.thresh_spin)
        thresh_group.addLayout(thresh_slider_row)
        layout.addLayout(thresh_group)

        layout.addSpacing(4)
        layout.addWidget(self._divider())

        self.mute_check = QCheckBox("SILENCIAR BUZZER")
        self.mute_check.toggled.connect(self.mute_toggled.emit)
        layout.addWidget(self.mute_check)

        self.pause_check = QCheckBox("PAUSAR RADAR")
        self.pause_check.toggled.connect(self.pause_toggled.emit)
        layout.addWidget(self.pause_check)

        layout.addStretch()

        layout.addWidget(self._divider())
        layout.addSpacing(4)
        self.status_label = QLabel("ESTADO:  En espera")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #B2BCB7; font-size: 13px; padding: 6px 0;")
        layout.addWidget(self.status_label)

        self.refresh_ports()

    def _divider(self):
        div = QFrame()
        div.setObjectName("divider")
        return div

    def _section_title(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet(
            "color: #00FF88; font-size: 12px; font-weight: 800; "
            "letter-spacing: 1.5px; background: transparent;"
        )
        return lbl

    def _on_connect_click(self):
        if self.connect_btn.text() == "CONECTAR":
            port = self.port_combo.currentText()
            if not port or port == "No hay puertos":
                return
            self.connect_requested.emit(port, 9600)
        else:
            self.disconnect_requested.emit()

    def _on_speed_change(self, v):
        self.speed_spin.blockSignals(True)
        self.speed_spin.setValue(v)
        self.speed_spin.blockSignals(False)
        self.speed_value.setText(f"{v} ms")
        self.param_changed.emit("VEL", v)

    def _on_speed_spin(self, v):
        self.speed_slider.blockSignals(True)
        self.speed_slider.setValue(v)
        self.speed_slider.blockSignals(False)
        self.speed_value.setText(f"{v} ms")
        self.param_changed.emit("VEL", v)

    def _on_thresh_change(self, v):
        self.thresh_spin.blockSignals(True)
        self.thresh_spin.setValue(v)
        self.thresh_spin.blockSignals(False)
        self.thresh_value.setText(f"{v} cm")
        self.param_changed.emit("THR", v)

    def _on_thresh_spin(self, v):
        self.thresh_slider.blockSignals(True)
        self.thresh_slider.setValue(v)
        self.thresh_slider.blockSignals(False)
        self.thresh_value.setText(f"{v} cm")
        self.param_changed.emit("THR", v)

    def refresh_ports(self):
        self.port_combo.clear()
        ports = QSerialPortInfo.availablePorts()
        for p in ports:
            self.port_combo.addItem(p.portName(), p.systemLocation())
        if self.port_combo.count() == 0:
            self.port_combo.addItem("No hay puertos")

    def set_connected(self, connected):
        if connected:
            self.connect_btn.setText("DESCONECTAR")
            self.connect_btn.setStyleSheet(
                "QPushButton { background-color: #FFFFFF; color: #FF4455; "
                "font-weight: 800; font-size: 16px; border: 2px solid #FF4455; "
                "border-radius: 4px; padding: 12px 20px; letter-spacing: 2px; }"
                "QPushButton:hover { background-color: #FFE8EA; "
                "border: 2px solid #FF6677; }"
            )
            self.status_indicator.setText("CONECTADO")
            self.status_indicator.setStyleSheet(
                "background-color: #0A2A18; color: #00FF88; "
                "border: 1px solid #00FF8844; font-weight: 700; "
                "letter-spacing: 1px; font-size: 13px; padding: 6px 12px; "
                "border-radius: 3px;"
            )
            self.status_label.setText("ESTADO:  Activo")
            self.port_combo.setEnabled(False)
            self.refresh_btn.setEnabled(False)
        else:
            self.connect_btn.setText("CONECTAR")
            self.connect_btn.setStyleSheet("")
            self.status_indicator.setText("DESCONECTADO")
            self.status_indicator.setStyleSheet(
                "background-color: #2A0A14; color: #FF4455; "
                "border: 1px solid #FF445544; font-weight: 700; "
                "letter-spacing: 1px; font-size: 13px; padding: 6px 12px; "
                "border-radius: 3px;"
            )
            self.status_label.setText("ESTADO:  En espera")
            self.port_combo.setEnabled(True)
            self.refresh_btn.setEnabled(True)


# ───────────────────────────────────────────────
# MAIN WINDOW
# ───────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RADAR ULTRASÓNICO -- Valorant Green Edition")
        self.setMinimumSize(960, 640)
        self.resize(1280, 800)

        self.serial = QSerialPort()
        self.serial.readyRead.connect(self._on_serial_data)
        self.serial.errorOccurred.connect(self._on_serial_error)
        self._serial_connected = False

        self._setup_ui()
        self._setup_connections()

        self.render_timer = QTimer(self)
        self.render_timer.timeout.connect(self.radar.update)
        self.render_timer.start(1000 // FPS)

        self._serial_buffer = ""
        self._arduino_ready = False
        self._pending_params = []

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        radar_container = QWidget()
        radar_container.setStyleSheet("background-color: #080E16;")
        radar_layout = QVBoxLayout(radar_container)
        radar_layout.setContentsMargins(0, 0, 0, 0)
        radar_layout.setSpacing(0)

        header = QWidget()
        header.setFixedHeight(86)
        header.setStyleSheet("background-color: #111B28;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)

        title_icon = QLabel("RADAR ULTRASÓNICO")
        title_icon.setObjectName("headerTitle")
        header_layout.addWidget(title_icon)
        header_layout.addStretch()

        self.fps_label = QLabel("60 FPS")
        self.fps_label.setStyleSheet("color: #B2BCB7; font-size: 13px; background: transparent;")
        header_layout.addWidget(self.fps_label)

        radar_layout.addWidget(header)

        self.radar = RadarWidget()
        radar_layout.addWidget(self.radar)

        self.control_panel = ControlPanel()

        main_layout.addWidget(radar_container, 1)
        main_layout.addWidget(self.control_panel, 0)

    def _setup_connections(self):
        c = self.control_panel
        c.connect_requested.connect(self._on_connect)
        c.disconnect_requested.connect(self._on_disconnect)
        c.param_changed.connect(self._on_param_change)
        c.mute_toggled.connect(lambda m: self._send_cmd(f"MUTE:{1 if m else 0}"))
        c.pause_toggled.connect(lambda p: self._send_cmd(f"PAUSE:{1 if p else 0}"))

    def _on_connect(self, port, baud):
        self.serial.setPortName(port)
        self.serial.setBaudRate(baud)

        if not self.serial.open(QSerialPort.ReadWrite):
            QMessageBox.warning(self, "Error",
                                f"No se pudo abrir {port}:\n{self.serial.errorString()}")
            return

        self._serial_connected = True
        self.control_panel.set_connected(True)
        self._serial_buffer = ""
        self._arduino_ready = False

    def _on_disconnect(self):
        self._serial_buffer = ""
        self._arduino_ready = False
        if self.serial.isOpen():
            self.serial.close()
        self._serial_connected = False
        self.control_panel.set_connected(False)
        self.radar.clear_scan_points()

    def _on_serial_data(self):
        data = self.serial.readAll().data().decode("utf-8", errors="replace")
        self._serial_buffer += data

        while "\n" in self._serial_buffer:
            idx = self._serial_buffer.index("\n")
            line = self._serial_buffer[:idx].strip()
            self._serial_buffer = self._serial_buffer[idx + 1:]

            if not line:
                continue

            if line == "RADAR_READY":
                self._arduino_ready = True
                self.control_panel.status_label.setText("ESTADO:  Listo")
                self._flush_pending()
                continue

            if line.startswith("OK "):
                continue

            parts = line.split(",")
            if len(parts) == 2:
                try:
                    angle = int(parts[0])
                    dist = int(parts[1])
                    self.radar.set_angle(angle)
                    self.radar.set_distance(dist)
                    self.radar.add_scan_point(angle, dist)
                except ValueError:
                    pass

    def _on_serial_error(self, error):
        if error != QSerialPort.NoError:
            self._on_disconnect()

    def _send_cmd(self, cmd):
        if self.serial.isOpen() and self._serial_connected:
            data = (cmd + "\n").encode("utf-8")
            self.serial.write(QByteArray(data))
            return True
        return False

    def _on_param_change(self, key, value):
        if self._arduino_ready:
            self._send_cmd(f"{key}:{value}")
        else:
            self._pending_params.append((key, value))

    def _flush_pending(self):
        for key, value in self._pending_params:
            self._send_cmd(f"{key}:{value}")
        self._pending_params.clear()

    def closeEvent(self, event):
        self.render_timer.stop()
        if self.serial.isOpen():
            self.serial.close()
        super().closeEvent(event)


# ───────────────────────────────────────────────
# ENTRY POINT
# ───────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(VALORANT_QSS)

    font = QFont("Segoe UI", 11)
    font.setStyleStrategy(QFont.PreferAntialias)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
