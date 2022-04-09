# Handles the navigation and transitions of the Ui

from PyQt5 import QtWidgets, QtGui, QtCore
import cv2
from AgePredictorUI.MainUI import Ui_MainWindow
import os
from AgePredictor.Camera import Camera
from AgePredictor.predictor import create_model, predict


class UiFunctions(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Handles the transitions of the Ui
    Dev: setupUi and use self as parent
    Final: use parent to use it in other modules
    """

    def __init__(self, parent=None, model_name=None, weights_path=None):
        super().__init__(parent)  # Class construction

        # Use parent wisely according to the purpose
        # self.parent = self  # initialise the parent -- dev purpose
        self.parent = parent  # initialise the parent -- Final case

        self.model = create_model(model_name, weights_path)  # Create model
        self.camera = Camera(self.model)

        # State
        self.camOff = False
        self.img_path = None
        self.frameCount = 0

        # Signal-slot all the buttons
        # 1. Home Page
        self.parent.NavigationHome2.clicked.connect(lambda x: self.parent.stackedWidget.setCurrentIndex(0))
        self.parent.NavigationUploadImage2.clicked.connect(lambda x: self.parent.stackedWidget.setCurrentIndex(1))
        self.parent.NavigationLiveCam2.clicked.connect(lambda x: self.parent.stackedWidget.setCurrentIndex(2))

        self.parent.UploadImageTile.clicked.connect(lambda x: self.parent.stackedWidget.setCurrentIndex(1))
        self.parent.LiveCamTile.clicked.connect(lambda x: self.parent.stackedWidget.setCurrentIndex(2))

        # 2. Upload Image Page
        self.parent.NavigationHome3.clicked.connect(lambda x: self.parent.stackedWidget.setCurrentIndex(0))
        self.parent.NavigationUploadImage3.clicked.connect(lambda x: self.parent.stackedWidget.setCurrentIndex(1))
        self.parent.NavigationLiveCam3.clicked.connect(lambda x: self.parent.stackedWidget.setCurrentIndex(2))

        self.parent.UploadImageButton.clicked.connect(self.uploadImage)
        self.parent.PredictButton.clicked.connect(self.predictFromImage)

        # 3. Live Cam Page
        self.parent.NavigationHome4.clicked.connect(lambda x: self.parent.stackedWidget.setCurrentIndex(0))
        self.parent.NavigationUploadImage4.clicked.connect(lambda x: self.parent.stackedWidget.setCurrentIndex(1))
        self.parent.NavigationLiveCam4.clicked.connect(lambda x: self.parent.stackedWidget.setCurrentIndex(2))

        self.parent.CamSwitchButton.clicked.connect(self.webCam)

        # Event Loop
        self.readFrame = QtCore.QTimer()
        self.readFrame.setInterval(1000 // 30)
        self.readFrame.timeout.connect(self.startCam)

    def uploadImage(self):
        self.img_path = QtWidgets.QFileDialog.getOpenFileName(self.parent, caption="Open...", directory=os.getcwd(),
                                                              filter="Image files "
                                                                     "(*.png *.jpg *.jpeg)")
        if self.img_path:
            pixmap = QtGui.QPixmap(self.img_path[0])
            self.parent.ImageViewer.setPixmap(pixmap)
            self.parent.ImageViewer.setScaledContents(True)
        else:
            pass

    def predictFromImage(self):
        face, _, _ = self.camera.detect_face_new(cv2.imread(self.img_path[0]))
        group, confidence = predict(face, self.model)
        self.parent.ResultLabel.setText("Predicted Age: " + str(group) + "( " + str(confidence * 100)[:4] + " %)")

    def webCam(self):
        if self.camOff:
            self.readFrame.stop()
            self.camera.stopCamera()
            self.parent.CamSwitchButton.setText("On")
            self.camOff = False
        else:
            self.camera.vid = cv2.VideoCapture(0)
            self.readFrame.start()
            self.parent.CamSwitchButton.setText("Off")
            self.camOff = True

    def startCam(self):
        self.camera.read(self.parent.CamView, self.frameCount)
        self.frameCount += 1
