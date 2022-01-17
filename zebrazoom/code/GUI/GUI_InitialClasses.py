import json
import math
import os
import webbrowser
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout, QCheckBox, QSpinBox

from zebrazoom.code.readValidationVideo import readValidationVideo


LARGE_FONT= QFont("Verdana", 12)
LIGHT_YELLOW = '#FFFFE0'
LIGHT_CYAN = '#E0FFFF'
LIGHT_GREEN = '#90ee90'
GOLD = '#FFD700'
SPINBOX_STYLESHEET = '''
QSpinBox::down-button  {
  subcontrol-origin: border;
  subcontrol-position: center left;
  height: 20;
  width: 20;
}

QSpinBox::up-button  {
  subcontrol-origin: border;
  subcontrol-position: center right;
  height: 20;
  width: 20;
}'''


def apply_style(widget, **kwargs):
    if (font := kwargs.pop('font', None)) is not None:
        widget.setFont(font)
    widget.setStyleSheet(';'.join('%s: %s' % (prop.replace('_', '-'), val)  for prop, val in kwargs.items()))
    return widget


class StartPage(QWidget):
    def __init__(self, controller):
        super().__init__(controller.window)
        self.controller = controller

        layout = QGridLayout()
        # Add widgets to the layout
        layout.addWidget(apply_style(QLabel("Welcome to ZebraZoom!", self), font=controller.title_font, color='purple'), 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(apply_style(QLabel("1 - Create a Configuration File:", self), color='blue', font_size='16px'), 1, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(apply_style(QLabel("You first need to create a configuration file for each 'type' of video you want to track.", self), color='green'), 3, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(apply_style(QLabel("Access the folder where configuration files are saved with the button above.", self), color='green'), 5, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("", self), 6, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(apply_style(QLabel("2 - Run the Tracking:", self), color='blue', font_size='16px'), 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(apply_style(QLabel("Once you have a configuration file, use it to track a video.", self), color='green'), 3, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(apply_style(QLabel("Or run the tracking on all videos inside a folder.", self), color='green'), 5, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(apply_style(QLabel("3 - Verify tracking results:", self), color='blue', font_size='16px'), 7, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(apply_style(QLabel("Visualize/Verify/Explore the tracking results with the button above.", self), color='green'), 9, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(apply_style(QLabel("Tips on how to correct/enhance ZebraZoom's output when necessary.", self), color='green'), 11, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(apply_style(QLabel("4 - Analyze behavior:", self), color='blue', font_size='16px'), 7, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(apply_style(QLabel("Compare populations based on either kinematic parameters or clustering of bouts.", self), color='green'), 9, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(apply_style(QLabel("Access the folder where the tracking results are saved with the button above.", self), color='green'), 11, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("", self), 12, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(apply_style(QLabel("Regularly update your version of ZebraZoom with: 'pip install zebrazoom --upgrade'!", self), background_color=GOLD), 15, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        open_config_folder_btn = apply_style(QPushButton("Open configuration file folder", self), background_color=LIGHT_YELLOW)
        open_config_folder_btn.clicked.connect(lambda: controller.openConfigurationFileFolder(controller.homeDirectory))
        layout.addWidget(open_config_folder_btn, 4, 0, Qt.AlignmentFlag.AlignCenter)
        run_tracking_on_video_btn = apply_style(QPushButton("Run ZebraZoom's Tracking on a video", self), background_color=LIGHT_YELLOW)
        run_tracking_on_video_btn.clicked.connect(lambda: controller.show_frame("VideoToAnalyze"))
        layout.addWidget(run_tracking_on_video_btn, 2, 1, Qt.AlignmentFlag.AlignCenter)
        run_tracking_on_videos_btn = apply_style(QPushButton("Run ZebraZoom's Tracking on several videos", self), background_color=LIGHT_YELLOW)
        run_tracking_on_videos_btn.clicked.connect(lambda: controller.show_frame("SeveralVideos"))
        layout.addWidget(run_tracking_on_videos_btn, 4, 1, Qt.AlignmentFlag.AlignCenter)
        visualize_output_btn = apply_style(QPushButton("Visualize ZebraZoom's output", self), background_color=LIGHT_YELLOW)
        visualize_output_btn.clicked.connect(lambda: controller.showResultsVisualization())
        layout.addWidget(visualize_output_btn, 8, 0, Qt.AlignmentFlag.AlignCenter)
        enhance_output_btn = apply_style(QPushButton("Enhance ZebraZoom's output", self), background_color=LIGHT_YELLOW)
        enhance_output_btn.clicked.connect(lambda: controller.show_frame("EnhanceZZOutput"))
        layout.addWidget(enhance_output_btn, 10, 0, Qt.AlignmentFlag.AlignCenter)
        analyze_output_btn = apply_style(QPushButton("Analyze ZebraZoom's outputs", self), background_color=LIGHT_YELLOW)
        analyze_output_btn.clicked.connect(lambda: controller.show_frame("CreateExperimentOrganizationExcel"))
        layout.addWidget(analyze_output_btn, 8, 1, Qt.AlignmentFlag.AlignCenter)
        open_output_folder_btn = apply_style(QPushButton("Open ZebraZoom's output folder: Access raw data", self), background_color=LIGHT_YELLOW)
        open_output_folder_btn.clicked.connect(lambda: controller.openZZOutputFolder(controller.homeDirectory))
        layout.addWidget(open_output_folder_btn, 10, 1, Qt.AlignmentFlag.AlignCenter)
        toubleshoot_btn = apply_style(QPushButton("Troubleshoot", self), background_color=LIGHT_CYAN)
        toubleshoot_btn.clicked.connect(lambda: controller.show_frame("ChooseVideoToTroubleshootSplitVideo"))
        layout.addWidget(toubleshoot_btn, 13, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        video_documentation_btn = apply_style(QPushButton("Video online documentation", self), background_color=LIGHT_CYAN)
        video_documentation_btn.clicked.connect(lambda: webbrowser.open_new("https://github.com/oliviermirat/ZebraZoom#tableofcontent"))
        layout.addWidget(video_documentation_btn, 14, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        hbox = QHBoxLayout()
        prepare_initial_config_btn = apply_style(QPushButton("Prepare initial configuration file for tracking", self), background_color=LIGHT_YELLOW)
        prepare_initial_config_btn.clicked.connect(lambda: controller.show_frame("ChooseVideoToCreateConfigFileFor"))
        hbox.addWidget(prepare_initial_config_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        optimize_config_file_btn = apply_style(QPushButton("Optimize a previously created configuration file", self), background_color=LIGHT_YELLOW)
        optimize_config_file_btn.clicked.connect(lambda: controller.show_frame("OptimizeConfigFile"))
        hbox.addWidget(optimize_config_file_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(hbox, 2, 0, Qt.AlignmentFlag.AlignCenter)
        # Set the layout on the application's window
        self.setLayout(layout)


class SeveralVideos(QWidget):
    def __init__(self, controller):
        super().__init__(controller.window)
        self.controller = controller

        layout = QVBoxLayout()
        layout.addWidget(apply_style(QLabel("Run ZebraZoom on several videos", self), font=controller.title_font), alignment=Qt.AlignmentFlag.AlignCenter)

        button1 = apply_style(QPushButton("Run ZebraZoom on an entire folder", self), background_color=LIGHT_YELLOW)
        button1.clicked.connect(lambda: controller.show_frame("FolderToAnalyze"))
        layout.addWidget(button1, alignment=Qt.AlignmentFlag.AlignCenter)

        sublayout1 = QVBoxLayout()
        button2 = apply_style(QPushButton("Manual first frame tail extremity for head embedded", self), background_color=LIGHT_YELLOW)
        button2.clicked.connect(lambda: controller.show_frame("TailExtremityHE"))
        sublayout1.addWidget(button2, alignment=Qt.AlignmentFlag.AlignCenter)
        sublayout1.addWidget(QLabel("This button allows you to only manually select the tail extremities,", self), alignment=Qt.AlignmentFlag.AlignCenter)
        sublayout1.addWidget(QLabel("you will be able to run the tracking on multiple videos without interruptions with the 'Run ZebraZoom on an entire folder' button above afterwards.", self), alignment=Qt.AlignmentFlag.AlignCenter)
        sublayout1.addWidget(apply_style(QLabel("", self), font=controller.title_font), alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(sublayout1)

        sublayout2 = QVBoxLayout()
        button3 = apply_style(QPushButton("Only select the regions of interest", self), background_color=LIGHT_YELLOW)
        button3.clicked.connect(lambda: controller.show_frame("FolderMultipleROIInitialSelect"))
        sublayout2.addWidget(button3, alignment=Qt.AlignmentFlag.AlignCenter)
        sublayout2.addWidget(QLabel("This is for the 'Multiple rectangular regions of interest chosen at runtime' option.", self), alignment=Qt.AlignmentFlag.AlignCenter)
        sublayout2.addWidget(QLabel("This button allows you to only select the ROIs,", self), alignment=Qt.AlignmentFlag.AlignCenter)
        sublayout2.addWidget(QLabel("you will be able to run the tracking on multiple videos without interruptions with the 'Run ZebraZoom on an entire folder' button above afterwards.", self), alignment=Qt.AlignmentFlag.AlignCenter)
        sublayout2.addWidget(apply_style(QLabel("", self), font=controller.title_font), alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(sublayout2)

        sublayout3 = QVBoxLayout()
        button4 = apply_style(QPushButton("'Group of multiple same size and shape equally spaced wells' coordinates pre-selection", self), background_color=LIGHT_YELLOW)
        button4.clicked.connect(lambda: controller.show_frame("FolderMultipleROIInitialSelect"))
        sublayout3.addWidget(button4, alignment=Qt.AlignmentFlag.AlignCenter)
        sublayout3.addWidget(QLabel("This button allows you to only select the coordinates,", self), alignment=Qt.AlignmentFlag.AlignCenter)
        sublayout3.addWidget(QLabel("you will be able to run the tracking on multiple videos without interruptions with the 'Run ZebraZoom on an entire folder' button above afterwards.", self), alignment=Qt.AlignmentFlag.AlignCenter)
        sublayout3.addWidget(apply_style(QLabel("", self), font=controller.title_font), alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(sublayout3)

        start_page_btn = apply_style(QPushButton("Go to the start page", self), background_color=LIGHT_CYAN)
        start_page_btn.clicked.connect(lambda: controller.show_frame("StartPage"))
        layout.addWidget(start_page_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)


class VideoToAnalyze(QWidget):
    def __init__(self, controller):
        super().__init__(controller.window)
        self.controller = controller

        layout = QVBoxLayout()
        layout.addWidget(apply_style(QLabel("Choose video.", self), font=controller.title_font), alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Look for the video you want to analyze.", self), alignment=Qt.AlignmentFlag.AlignCenter)
        button = apply_style(QPushButton("Choose file", self), background_color=LIGHT_YELLOW)
        button.clicked.connect(lambda: controller.chooseVideoToAnalyze(just_extract_checkbox.isChecked(), no_validation_checkbox.isChecked(), debug_checkbox.isChecked()))
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("", self), alignment=Qt.AlignmentFlag.AlignCenter)

        debug_sublayout = QVBoxLayout()
        debug_checkbox = apply_style(QCheckBox("Run in debug mode.", self), background_color='red')
        debug_sublayout.addWidget(debug_checkbox, alignment=Qt.AlignmentFlag.AlignCenter)
        debug_sublayout.addWidget(QLabel("", self), alignment=Qt.AlignmentFlag.AlignCenter)
        debug_sublayout.addWidget(apply_style(QLabel("This option can be useful to test a new configuration file.", self), background_color='red'), alignment=Qt.AlignmentFlag.AlignCenter)
        debug_sublayout.addWidget(apply_style(QLabel("In this mode you will need to click on any key on each visualization windows.", self), background_color='red'), alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(debug_sublayout)
        layout.addWidget(QLabel("", self), alignment=Qt.AlignmentFlag.AlignCenter)

        text_sublayout = QVBoxLayout()
        text_sublayout.addWidget(QLabel("Alternatively, to test a new configuration file, you can temporarily manually add the parameter:", self), alignment=Qt.AlignmentFlag.AlignCenter)
        text_sublayout.addWidget(QLabel("'lastFrame': someSmallValue(for example 100)", self), alignment=Qt.AlignmentFlag.AlignCenter)
        text_sublayout.addWidget(QLabel("as well as the parameter:", self), alignment=Qt.AlignmentFlag.AlignCenter)
        text_sublayout.addWidget(QLabel("'backgroundExtractionForceUseAllVideoFrames': 1", self), alignment=Qt.AlignmentFlag.AlignCenter)
        text_sublayout.addWidget(QLabel("inside your configuration file to run the tracking on a small portion of the video in order to test the tracking.", self), alignment=Qt.AlignmentFlag.AlignCenter)
        text_sublayout.addWidget(QLabel("(if necessary, you can also add the parameter 'firstFrame' in your configuration file)", self), alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(text_sublayout)
        layout.addWidget(QLabel("", self), alignment=Qt.AlignmentFlag.AlignCenter)

        button = apply_style(QPushButton("Click here if you prefer to run the tracking from the command line", self), background_color='green')
        button.clicked.connect(lambda: webbrowser.open_new("https://github.com/oliviermirat/ZebraZoom#commandlinezebrazoom"))
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

        just_extract_checkbox = apply_style(QCheckBox("I ran the tracking already, I only want to redo the extraction of parameters.", self), color='purple')
        layout.addWidget(just_extract_checkbox, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("", self), alignment=Qt.AlignmentFlag.AlignCenter)
        no_validation_checkbox = apply_style(QCheckBox("Don't (re)generate a validation video (for speed efficiency).", self), color='purple')
        layout.addWidget(no_validation_checkbox, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("", self), alignment=Qt.AlignmentFlag.AlignCenter)

        start_page_btn = apply_style(QPushButton("Go to the start page", self), background_color=LIGHT_CYAN)
        start_page_btn.clicked.connect(lambda: controller.show_frame("StartPage"))
        layout.addWidget(start_page_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)


class FolderToAnalyze(QWidget):
    def __init__(self, controller):
        super().__init__(controller.window)
        self.controller = controller

        layout = QVBoxLayout()
        layout.addWidget(apply_style(QLabel("Choose folder.", self), font=controller.title_font), alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Look for the folder you want to analyze.", self), alignment=Qt.AlignmentFlag.AlignCenter)
        button = apply_style(QPushButton("Choose folder", self), background_color=LIGHT_YELLOW)
        button.clicked.connect(lambda: controller.chooseFolderToAnalyze(just_extract_checkbox.isChecked(), no_validation_checkbox.isChecked(), expert_checkbox.isChecked()))
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("", self), alignment=Qt.AlignmentFlag.AlignCenter)

        just_extract_checkbox = QCheckBox("I ran the tracking already, I only want to redo the extraction of parameters.", self)
        layout.addWidget(just_extract_checkbox, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("", self), alignment=Qt.AlignmentFlag.AlignCenter)
        no_validation_checkbox = QCheckBox("Don't (re)generate a validation video (for speed efficiency).", self)
        layout.addWidget(no_validation_checkbox, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("", self), alignment=Qt.AlignmentFlag.AlignCenter)
        expert_checkbox = QCheckBox("Expert use (don't click here unless you know what you're doing): Only generate a script to launch all videos in parallel with sbatch.", self)
        layout.addWidget(expert_checkbox, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("", self), alignment=Qt.AlignmentFlag.AlignCenter)

        start_page_btn = apply_style(QPushButton("Go to the start page", self), background_color=LIGHT_CYAN)
        start_page_btn.clicked.connect(lambda: controller.show_frame("StartPage"))
        layout.addWidget(start_page_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)


class TailExtremityHE(QWidget):
    def __init__(self, controller):
        super().__init__(controller.window)
        self.controller = controller

        layout = QVBoxLayout()
        layout.addWidget(apply_style(QLabel("Choose folder.", self), font=controller.title_font), alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Look for the folder of videos where you want to manually label tail extremities.", self), alignment=Qt.AlignmentFlag.AlignCenter)
        button = apply_style(QPushButton("Choose folder", self), background_color=LIGHT_YELLOW)
        button.clicked.connect(controller.chooseFolderForTailExtremityHE)
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

        start_page_btn = apply_style(QPushButton("Go to the start page", self), background_color=LIGHT_CYAN)
        start_page_btn.clicked.connect(lambda: controller.show_frame("StartPage"))
        layout.addWidget(start_page_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)


class FolderMultipleROIInitialSelect(QWidget):
    def __init__(self, controller):
        super().__init__(controller.window)
        self.controller = controller

        layout = QVBoxLayout()
        layout.addWidget(apply_style(QLabel("Choose folder.", self), font=controller.title_font), alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Select the folder of videos for which you want to define the regions of interest.", self), alignment=Qt.AlignmentFlag.AlignCenter)
        button = apply_style(QPushButton("Choose folder", self), background_color=LIGHT_YELLOW)
        button.clicked.connect(controller.chooseFolderForMultipleROIs)
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

        start_page_btn = apply_style(QPushButton("Go to the start page", self), background_color=LIGHT_CYAN)
        start_page_btn.clicked.connect(lambda: controller.show_frame("StartPage"))
        layout.addWidget(start_page_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)


class ConfigFilePromp(QWidget):
    def __init__(self, controller):
        super().__init__(controller.window)
        self.controller = controller

        layout = QVBoxLayout()
        layout.addWidget(apply_style(QLabel("Choose configuration file.", self), font=controller.title_font), alignment=Qt.AlignmentFlag.AlignCenter)
        button = apply_style(QPushButton("Choose file", self), background_color=LIGHT_YELLOW)
        button.clicked.connect(lambda: controller.chooseConfigFile())
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
        start_page_btn = apply_style(QPushButton("Go to the start page", self), background_color=LIGHT_CYAN)
        start_page_btn.clicked.connect(lambda: controller.show_frame("StartPage"))
        layout.addWidget(start_page_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)


class Patience(QWidget):
    def __init__(self, controller):
        super().__init__(controller.window)
        self.controller = controller

        layout = QVBoxLayout()
        button = apply_style(QPushButton("Launch ZebraZoom on your video(s)", self), background_color=LIGHT_YELLOW)
        button.clicked.connect(lambda: controller.launchZebraZoom())
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("After clicking on the button above, please wait for ZebraZoom to run, you can look at the console outside of the GUI to check on the progress of ZebraZoom.", self), alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)


class ZZoutro(QWidget):
    def __init__(self, controller):
        super().__init__(controller.window)
        self.controller = controller

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Finished.", self), alignment=Qt.AlignmentFlag.AlignCenter)
        button = apply_style(QPushButton("Go to the start page", self), background_color=LIGHT_YELLOW)
        button.clicked.connect(lambda: controller.show_frame("StartPage"))
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)


class ResultsVisualization(QWidget):
    def __init__(self, controller):
        super().__init__(controller.window)
        self.controller = controller
        self.setLayout(QGridLayout())

    def refresh(self):
        nbLines = 15
        curLine = 1
        curCol  = 0

        layout = self.layout()
        for idx in reversed(range(layout.count())):
            layout.itemAt(idx).widget().setParent(None)

        layout.addWidget(apply_style(QLabel("Choose the results you'd like to visualize", self), font=self.controller.title_font), 0, 0, Qt.AlignmentFlag.AlignCenter)

        reference = self.controller.ZZoutputLocation

        if not(os.path.exists(reference)):
          os.mkdir(reference)

        os.walk(reference)
        for x in sorted(next(os.walk(reference))[1]):
          button = QPushButton(x, self)
          button.clicked.connect(lambda _, currentResultFolder=x: self.controller.showViewParameters(currentResultFolder))
          layout.addWidget(button, curLine, curCol, Qt.AlignmentFlag.AlignCenter)
          if (curLine > nbLines):
            curLine = 1
            curCol = curCol + 1
          else:
            curLine = curLine + 1

        button = apply_style(QPushButton("Go to the start page", self), background_color=LIGHT_YELLOW)
        button.clicked.connect(lambda: self.controller.show_frame("StartPage"))
        layout.addWidget(button, curLine, curCol, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)


class ViewParameters(QWidget):
    def __init__(self, controller):
        super().__init__(controller.window)
        self.controller = controller

        layout = QGridLayout()
        layout.addWidget(apply_style(QLabel("    ", self), font=LARGE_FONT), 1, 6, Qt.AlignmentFlag.AlignCenter)
        button = QPushButton("View video for all wells together", self)
        button.clicked.connect(lambda: self.showValidationVideo(-1, self.numPoiss(), 0, -1))
        layout.addWidget(button, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.view_btn = QPushButton("", self)
        self.view_btn.clicked.connect(lambda: self.showGraphForAllBoutsCombined(self.numWell(), self.numPoiss(), self.dataRef, self.visualization, self.graphScaling))
        layout.addWidget(self.view_btn, 1, 2, 1, 5, Qt.AlignmentFlag.AlignCenter)

        self.title_label = apply_style(QLabel('', self), font_size='16px')
        layout.addWidget(self.title_label, 0, 0, 1, 8, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Well number:", self), 2, 1, Qt.AlignmentFlag.AlignCenter)
        self.spinbox1 = QSpinBox(self)
        self.spinbox1.setStyleSheet(SPINBOX_STYLESHEET)
        self.spinbox1.setMinimumWidth(70)
        self.spinbox1.valueChanged.connect(self._wellChanged)
        self.numWell = self.spinbox1.value
        layout.addWidget(self.spinbox1, 2, 2, Qt.AlignmentFlag.AlignCenter)

        self.zoomed_video_btn = QPushButton("", self)
        self.zoomed_video_btn.clicked.connect(lambda: self.showValidationVideo(self.numWell(), self.numPoiss(), 1, -1))
        layout.addWidget(self.zoomed_video_btn, 3, 2, Qt.AlignmentFlag.AlignCenter)
        link1 = apply_style(QPushButton("Video viewing tips", self), background_color='red')
        link1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        link1.clicked.connect(lambda: webbrowser.open_new("https://zebrazoom.org/validationVideoReading.html"))
        layout.addWidget(link1, 3, 4, Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(QLabel("Fish number:", self), 4, 1, Qt.AlignmentFlag.AlignCenter)
        self.spinbox2 = QSpinBox(self)
        self.spinbox2.setStyleSheet(SPINBOX_STYLESHEET)
        self.spinbox2.setMinimumWidth(70)
        self.spinbox2.valueChanged.connect(self._poissChanged)
        self.numPoiss = self.spinbox2.value
        layout.addWidget(self.spinbox2, 4, 2, Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(QLabel("Bout number:", self), 5, 1, Qt.AlignmentFlag.AlignCenter)
        self.spinbox3 = QSpinBox(self)
        self.spinbox3.setStyleSheet(SPINBOX_STYLESHEET)
        self.spinbox3.setMinimumWidth(70)
        self.spinbox3.valueChanged.connect(self._mouvChanged)
        self.numMouv = self.spinbox3.value
        layout.addWidget(self.spinbox3, 5, 2, Qt.AlignmentFlag.AlignCenter)

        button1 = QPushButton("View bout's angle", self)
        button1.clicked.connect(lambda: self.printSomeResults())
        layout.addWidget(button1, 6, 2, Qt.AlignmentFlag.AlignCenter)

        self.flag_movement_btn = QPushButton("", self)
        self.flag_movement_btn.clicked.connect(self.flagMove)
        layout.addWidget(self.flag_movement_btn, 6, 4, Qt.AlignmentFlag.AlignCenter)

        self.prev_btn = QPushButton("Previous Bout", self)
        self.prev_btn.clicked.connect(self.printPreviousResults)
        layout.addWidget(self.prev_btn, 7, 1, Qt.AlignmentFlag.AlignCenter)
        self.next_btn = QPushButton("Next Bout", self)
        self.next_btn.clicked.connect(self.printNextResults)
        layout.addWidget(self.next_btn, 7, 2, Qt.AlignmentFlag.AlignCenter)

        back_btn = QPushButton("Go to the previous page", self)
        back_btn.clicked.connect(lambda: controller.show_frame("ResultsVisualization"))
        layout.addWidget(back_btn, 8, 1, Qt.AlignmentFlag.AlignCenter)
        change_btn = apply_style(QPushButton("Change Right Side Plot", self), background_color=LIGHT_GREEN)
        change_btn.clicked.connect(lambda: self.printSomeResults(True))
        layout.addWidget(change_btn, 8, 2, 1, 2, Qt.AlignmentFlag.AlignCenter)

        self.zoom_btn = apply_style(QPushButton("", self), background_color=LIGHT_GREEN)
        self.zoom_btn.clicked.connect(lambda: self.printSomeResults(False, True))
        layout.addWidget(self.zoom_btn, 8, 3, 1, 2, Qt.AlignmentFlag.AlignCenter)

        self.well_video_btn = QPushButton("", self)
        self.well_video_btn.clicked.connect(lambda: self.showValidationVideo(self.numWell(), self.numPoiss(), 0, self.begMove))
        layout.addWidget(self.well_video_btn, 3, 1, Qt.AlignmentFlag.AlignCenter)
        self.bout_video_btn = QPushButton("View bout's video" , self)
        self.bout_video_btn.clicked.connect(lambda: self.showValidationVideo(self.numWell(), self.numPoiss(), 1, self.begMove))
        layout.addWidget(self.bout_video_btn, 6, 1, Qt.AlignmentFlag.AlignCenter)
        self.graph_title_label = apply_style(QLabel('', font=LARGE_FONT))
        layout.addWidget(self.graph_title_label, 1, 7, Qt.AlignmentFlag.AlignCenter)

        self.superstruct_btn = apply_style(QPushButton("Save SuperStruct" , self), background_color='orange')
        self.superstruct_btn.clicked.connect(self.saveSuperStruct)
        layout.addWidget(self.superstruct_btn, 7, 4, Qt.AlignmentFlag.AlignCenter)

        f = Figure(figsize=(5,5), dpi=100)
        self.a = f.add_subplot(111)
        self.canvas = FigureCanvas(f)
        layout.addWidget(self.canvas, 2, 7, 7, 1, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def setFolder(self, name):
        self.title_label.setText(name)
        self.currentResultFolder = name
        reference = os.path.join(self.controller.ZZoutputLocation, os.path.join(name, 'results_' + name + '.txt'))
        if not(os.path.exists(reference)):
          mypath = os.path.join(self.controller.ZZoutputLocation, name)
          onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
          resultFile = ''
          for fileName in onlyfiles:
            if 'results_' in fileName:
              resultFile = fileName
          reference = os.path.join(self.controller.ZZoutputLocation, os.path.join(name, resultFile))

        with open(reference) as ff:
            self.dataRef = json.load(ff)

        self.spinbox1.setValue(0)
        self.spinbox2.setValue(0)
        self.spinbox3.setValue(0)
        self.nbWells = len(self.dataRef["wellPoissMouv"])
        self.nbPoiss = len(self.dataRef["wellPoissMouv"][self.numWell()])
        self.nbMouv = len(self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()])
        self.visualization = 2
        self.graphScaling = True
        self.spinbox1.setRange(0, self.nbWells - 1)
        self.spinbox2.setRange(0, self.nbPoiss - 1)
        self.spinbox3.setRange(0, self.nbMouv - 1)
        self.superstruct_btn.hide()
        self.printSomeResults()

    def _updateGraph(self):
        self.a.clear()
        if self.nbMouv > 0:
            self.begMove = self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()][self.numMouv()]["BoutStart"]
            endMove = self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()][self.numMouv()]["BoutEnd"]

            if self.visualization == 0 and not("TailAngle_smoothed" in self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()][self.numMouv()]):
                self.visualization = 1

            if self.visualization == 1 and not("TailAngle_Raw" in self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()][self.numMouv()]):
                self.visualization = 2

            # if self.visualization == 2 and not((len(np.unique(self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()][self.numMouv()]["HeadX"])) > 1) and (len(np.unique(self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()][self.numMouv()]["HeadY"])) > 1)):
                # self.visualization = 0

            if self.visualization == 0:

              tailAngleSmoothed = self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()][self.numMouv()]["TailAngle_smoothed"].copy()

              for ind,val in enumerate(tailAngleSmoothed):
                tailAngleSmoothed[ind]=tailAngleSmoothed[ind]*(180/(math.pi))

              if "Bend_Timing" in self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()][self.numMouv()]:
                freqX = self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()][self.numMouv()]["Bend_Timing"]
                freqY = self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()][self.numMouv()]["Bend_Amplitude"]
              else:
                freqX = []
                freqY = []
              if type(freqY)==int or type(freqY)==float:
                freqY = freqY * (180/(math.pi))
              else:
                if "Bend_Timing" in self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()][self.numMouv()]:
                  freqX = self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()][self.numMouv()]["Bend_Timing"].copy()
                  freqY = self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()][self.numMouv()]["Bend_Amplitude"].copy()
                else:
                  freqX = []
                  freqY = []
                for ind,val in enumerate(freqY):
                  freqY[ind]=freqY[ind]*(180/(math.pi))
              fx = [self.begMove]
              fy = [0]
              if (type(freqX) is int) or (type(freqX) is float):
                freqX = [freqX]
                freqY = [freqY]
              for idx,x in enumerate(freqX):
                idx2 = idx - 1
                fx.append(freqX[idx2] - 1 + self.begMove)
                fx.append(freqX[idx2] - 1 + self.begMove)
                fx.append(freqX[idx2] - 1 + self.begMove)
                fy.append(0)
                fy.append(freqY[idx2])
                fy.append(0)

              if not(self.graphScaling):
                self.a.set_ylim(-140, 140)

              if len(tailAngleSmoothed):
                self.a.plot([i for i in range(self.begMove,endMove+1)],tailAngleSmoothed)
                self.a.plot(fx,fy)
                self.a.plot([i for i in range(self.begMove,endMove+1)],[0 for i in range(0,len(tailAngleSmoothed))])

            elif self.visualization == 1:

              tailAngleSmoothed = self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()][self.numMouv()]["TailAngle_Raw"].copy()
              for ind,val in enumerate(tailAngleSmoothed):
                tailAngleSmoothed[ind]=tailAngleSmoothed[ind]*(180/(math.pi))

              if not(self.graphScaling):
                self.a.set_ylim(-140, 140)

              self.a.plot([i for i in range(self.begMove,endMove+1)],tailAngleSmoothed)
              self.a.plot([i for i in range(self.begMove,endMove+1)],[0 for i in range(0,len(tailAngleSmoothed))])

            else:
              headX = self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()][self.numMouv()]["HeadX"].copy()
              headY = self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()][self.numMouv()]["HeadY"].copy()


              if not(self.graphScaling):
                lengthX  = self.dataRef["wellPositions"][self.numWell()]["lengthX"]
                lengthY  = self.dataRef["wellPositions"][self.numWell()]["lengthY"]
                self.a.set_xlim(0, lengthX)
                self.a.set_ylim(0, lengthY)

              self.a.plot(headX, headY)
        else:
            tailAngleSmoothed = [i for i in range(0,1)]
            self.a.plot([i for i in range(0,len(tailAngleSmoothed))],tailAngleSmoothed)
            self.a.text(0.5, 0.5, 'No bout detected for well %d' % self.numWell(), horizontalalignment='center', verticalalignment='center', transform=self.a.transAxes)
        self.canvas.draw()

    def _updateWidgets(self):
        self.zoomed_video_btn.setText("View zoomed video for well %d" % self.numWell())
        self.next_btn.setEnabled(self.numMouv() < self.nbMouv - 1 or self.numPoiss() < self.nbPoiss - 1 or self.numWell() < self.nbWells - 1)
        self.prev_btn.setEnabled(self.numMouv() or self.numPoiss() or self.numWell())
        if self.nbMouv:
          if self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()][self.numMouv()].get("flag"):
            apply_style(self.flag_movement_btn, background_color='red').setText("UnFlag Movement")
          else:
            apply_style(self.flag_movement_btn).setText("Flag Movement")
          self.flag_movement_btn.show()
          self.well_video_btn.setText("View video for well %d" % self.numWell())
          self.well_video_btn.show()
          self.bout_video_btn.show()
          if self.visualization == 0:
            text = "Tail Angle Smoothed and amplitudes for well %d, fish %d, bout %d"
          elif self.visualization == 1:
            text = "Tail Angle Raw for well %d, fish %d, bout %d"
          else:
            text = "Body Coordinates for well %d, fish %d, bout %d"
          self.graph_title_label.setText(text % (self.numWell() , self.numPoiss(), self.numMouv()))
          self.graph_title_label.show()
        else:
          self.flag_movement_btn.hide()
          self.well_video_btn.hide()
          self.bout_video_btn.hide()
          self.graph_title_label.hide()

    def flagMove(self):
        self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()][self.numMouv()]["flag"] = int(not self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()][self.numMouv()].get("flag", False));
        if self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()][self.numMouv()]["flag"]:
            apply_style(self.flag_movement_btn, background_color='red').setText("UnFlag Movement")
        else:
            apply_style(self.flag_movement_btn).setText("Flag Movement")
        self.superstruct_btn.show()

    def printSomeResults(self, changeVisualization=False, changeScaling=False):
        if changeVisualization:
            self.visualization = int(self.visualization + 1) % 3
        if changeScaling:
            self.graphScaling = not self.graphScaling
        buttonLabel = "View "
        if self.graphScaling:
          buttonLabel = buttonLabel + "Zoomed In "
        else:
          buttonLabel = buttonLabel + "Zoomed Out "
        if self.visualization == 0:
          buttonLabel = buttonLabel + "tail angle smoothed"
        elif self.visualization == 1:
          buttonLabel = buttonLabel + "tail angle raw"
        else:
          buttonLabel = buttonLabel + "body coordinates"
        self.view_btn.setText(buttonLabel + " for all bouts combined")
        self.zoom_btn.setText("Zoom out Graph" if self.graphScaling else "Zoom in Graph")
        self._updateGraph()
        self._updateWidgets()

    def showValidationVideo(self, numWell, numAnimal, zoom, deb):
        cur_dir_path = os.path.dirname(os.path.realpath(__file__))
        path = Path(cur_dir_path)
        path = path.parent.parent
        filepath = os.path.join(path, os.path.join('ZZoutput', os.path.join(self.currentResultFolder, 'pathToVideo.txt')))

        if os.path.exists(filepath):
            with open(filepath) as fp:
               videoPath = fp.readline()
            videoPath = videoPath[:len(videoPath)-1]
        else:
            videoPath = ""

        readValidationVideo(videoPath, self.currentResultFolder, '.txt', numWell, numAnimal, zoom, deb, ZZoutputLocation=self.controller.ZZoutputLocation)

    def showGraphForAllBoutsCombined(self, numWell, numPoiss, dataRef, visualization, graphScaling):

      plt.ion()
      if (visualization == 0) or (visualization == 1):

        tailAngleFinal = []
        xaxisFinal = []
        if "firstFrame" in dataRef and "lastFrame" in dataRef:
          begMove = 0
          endMove = dataRef["wellPoissMouv"][numWell][numPoiss][0]["BoutStart"]
          xaxis     = [i for i in range(begMove, endMove)]
          tailAngle = [0 for i in range(begMove, endMove)]
          tailAngleFinal = tailAngleFinal + tailAngle
          xaxisFinal = xaxisFinal + xaxis
        for numMouv in range(0, len(dataRef["wellPoissMouv"][numWell][numPoiss])):
          if (visualization == 0):
            tailAngle = dataRef["wellPoissMouv"][numWell][numPoiss][numMouv]["TailAngle_smoothed"].copy()
          else:
            tailAngle = dataRef["wellPoissMouv"][numWell][numPoiss][numMouv]["TailAngle_Raw"].copy()
          for ind,val in enumerate(tailAngle):
            tailAngle[ind]=tailAngle[ind]*(180/(math.pi))
          begMove = dataRef["wellPoissMouv"][numWell][numPoiss][numMouv]["BoutStart"]
          endMove = begMove + len(tailAngle)
          xaxis = [i for i in range(begMove-1,endMove+1)]
          tailAngle.append(0)
          tailAngle.insert(0, 0)
          tailAngleFinal = tailAngleFinal + tailAngle
          xaxisFinal = xaxisFinal + xaxis
        if "firstFrame" in dataRef and "lastFrame" in dataRef:
          begMove = endMove
          endMove = dataRef["lastFrame"] - 1
          xaxis     = [i for i in range(begMove, endMove)]
          tailAngle = [0 for i in range(begMove, endMove)]
          tailAngleFinal = tailAngleFinal + tailAngle
          xaxisFinal = xaxisFinal + xaxis
        if "fps" in dataRef:
          plt.plot([xaxisFinalVal / dataRef["fps"] for xaxisFinalVal in xaxisFinal], tailAngleFinal)
        else:
          plt.plot(xaxisFinal, tailAngleFinal)
        if not(graphScaling):
          plt.ylim(-140, 140)
        if "firstFrame" in dataRef and "lastFrame" in dataRef:
          if "fps" in dataRef:
            plt.xlim(dataRef["firstFrame"] / dataRef["fps"], dataRef["lastFrame"] / dataRef["fps"])
          else:
            plt.xlim(dataRef["firstFrame"], dataRef["lastFrame"])
        plt.show()

      else:

        headXFinal = []
        headYFinal = []
        for numMouv in range(0, len(dataRef["wellPoissMouv"][numWell][numPoiss])):
          headXFinal = headXFinal + dataRef["wellPoissMouv"][numWell][numPoiss][numMouv]["HeadX"].copy()
          headYFinal = headYFinal + dataRef["wellPoissMouv"][numWell][numPoiss][numMouv]["HeadY"].copy()
        plt.plot(headXFinal, headYFinal)
        if not(graphScaling):
          plt.xlim(0, dataRef["wellPositions"][numWell]["lengthX"])
          plt.ylim(0, dataRef["wellPositions"][numWell]["lengthY"])
        plt.show()

    def printNextResults(self):
        if self.numMouv() + 1 < self.nbMouv:
            self.spinbox3.setValue(self.numMouv() + 1)
        elif self.numPoiss() + 1 < self.nbPoiss:
            self.spinbox2.setValue(self.numPoiss() + 1)
            self.spinbox3.setValue(0)
        else:
            self.spinbox1.setValue(self.numWell() + 1)
            self.spinbox2.setValue(0)
            self.spinbox3.setValue(0)

    def printPreviousResults(self):
        if self.numMouv() - 1 >= 0:
            self.spinbox3.setValue(self.numMouv() - 1)
        elif self.numPoiss() - 1 >= 0:
            self.spinbox2.setValue(self.numPoiss() - 1)
            self.spinbox3.setValue(self.nbMouv - 1)
        else:
            self.spinbox1.setValue(self.numWell() - 1)
            self.spinbox2.setValue(self.nbPoiss - 1)
            self.spinbox3.setValue(self.nbMouv - 1)

    def saveSuperStruct(self):
        name = self.currentResultFolder

        cur_dir_path = os.path.dirname(os.path.realpath(__file__))
        path = Path(cur_dir_path).parent.parent
        reference = os.path.join(self.controller.ZZoutputLocation, os.path.join(name, 'results_' + name + '.txt'))
        print("reference:", reference)

        with open(reference,'w') as out:
           json.dump(self.dataRef, out)

        self.superstruct_btn.hide()

    def _wellChanged(self):
        self.nbPoiss = len(self.dataRef["wellPoissMouv"][self.numWell()])
        self.spinbox2.setRange(0, self.nbPoiss - 1)
        self.nbMouv = len(self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()])
        self.spinbox3.setRange(0, self.nbMouv - 1)
        self._updateGraph()
        self._updateWidgets()

    def _poissChanged(self):
        self.nbMouv = len(self.dataRef["wellPoissMouv"][self.numWell()][self.numPoiss()])
        self.spinbox3.setRange(0, self.nbMouv - 1)
        self._updateGraph()
        self._updateWidgets()

    def _mouvChanged(self):
        self._updateGraph()
        self._updateWidgets()
