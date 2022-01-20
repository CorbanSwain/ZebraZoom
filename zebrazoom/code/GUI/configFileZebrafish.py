from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QRadioButton, QButtonGroup


def apply_style(widget, **kwargs):
    if (font := kwargs.pop('font', None)) is not None:
        widget.setFont(font)
    widget.setStyleSheet(';'.join('%s: %s' % (prop.replace('_', '-'), val)  for prop, val in kwargs.items()))
    return widget


class HeadEmbeded(QWidget):
  def __init__(self, controller):
    super().__init__(controller.window)
    self.controller = controller

    layout = QVBoxLayout()
    layout.addWidget(apply_style(QLabel("Prepare Config File", self), font=controller.title_font), alignment=Qt.AlignmentFlag.AlignCenter)

    layout.addWidget(apply_style(QLabel("Choose only one of the options below:", self), font=QFont("Helvetica", 12)), alignment=Qt.AlignmentFlag.AlignCenter)
    btnGroup1 = QButtonGroup(self)
    blackBackRadioButton = QRadioButton("Black background, white zebrafish.", self)
    btnGroup1.addButton(blackBackRadioButton)
    blackBackRadioButton.setChecked(True)
    layout.addWidget(blackBackRadioButton, alignment=Qt.AlignmentFlag.AlignCenter)
    whiteBackRadioButton = QRadioButton("White background, black zebrafish.", self)
    btnGroup1.addButton(whiteBackRadioButton)
    layout.addWidget(whiteBackRadioButton, alignment=Qt.AlignmentFlag.AlignCenter)

    layout.addWidget(apply_style(QLabel("Do you want ZebraZoom to detect bouts of movement?", self), font=QFont("Helvetica", 12)), alignment=Qt.AlignmentFlag.AlignCenter)
    btnGroup2 = QButtonGroup(self)
    noBoutDetectRadioButton = QRadioButton("No. I want the tracking data for all frames of the videos.", self)
    btnGroup2.addButton(noBoutDetectRadioButton)
    noBoutDetectRadioButton.setChecked(True)
    layout.addWidget(noBoutDetectRadioButton, alignment=Qt.AlignmentFlag.AlignCenter)
    boutDetectionRadioButton = QRadioButton("Yes. I want the tracking data only when the fish is moving.", self)
    btnGroup2.addButton(boutDetectionRadioButton)
    layout.addWidget(boutDetectionRadioButton, alignment=Qt.AlignmentFlag.AlignCenter)

    layout.addWidget(apply_style(QLabel("Do you want to try to tweak tracking parameters further?", self), font=QFont("Helvetica", 12)), alignment=Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(QLabel("Warning: further tweaking tracking parameters could make tracking results worse; please try without this option first.", self), alignment=Qt.AlignmentFlag.AlignCenter)
    btnGroup3 = QButtonGroup(self)
    tweakTrackingParamsYesRadioButton = QRadioButton("Yes", self)
    btnGroup3.addButton(tweakTrackingParamsYesRadioButton)
    tweakTrackingParamsYesRadioButton.setChecked(True)
    layout.addWidget(tweakTrackingParamsYesRadioButton, alignment=Qt.AlignmentFlag.AlignCenter)
    tweakTrackingParamsNoRadioButton = QRadioButton("No", self)
    btnGroup3.addButton(tweakTrackingParamsNoRadioButton)
    layout.addWidget(tweakTrackingParamsNoRadioButton, alignment=Qt.AlignmentFlag.AlignCenter)

    nextBtn = QPushButton("Next", self)
    nextBtn.clicked.connect(lambda: controller.headEmbededGUI(controller, blackBackRadioButton.isChecked(), whiteBackRadioButton.isChecked(), noBoutDetectRadioButton.isChecked(), boutDetectionRadioButton.isChecked(), tweakTrackingParamsYesRadioButton.isChecked(), tweakTrackingParamsNoRadioButton.isChecked()))
    layout.addWidget(nextBtn, alignment=Qt.AlignmentFlag.AlignCenter)
    startPageBtn = QPushButton("Go to the start page", self)
    startPageBtn.clicked.connect(lambda: controller.show_frame("StartPage"))
    layout.addWidget(startPageBtn, alignment=Qt.AlignmentFlag.AlignCenter)

    self.setLayout(layout)
