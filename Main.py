# Main file that executes the program

from PyQt5 import QtWidgets
from AgePredictorUI.UI_Functions import UiFunctions
from AgePredictorUI.MainUI import Ui_MainWindow


class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Acts similar to the main file
    dev purpose
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        transitions = UiFunctions(self, model_name="inception", weights_path=r"C:\Users\aniru\PycharmProjects\Age Predictor 2.0\venv2\AgePredictor\InceptionWeights\tmp\checkpoint")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())