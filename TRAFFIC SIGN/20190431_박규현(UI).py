from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication, QPushButton
import cv2
from PIL import Image
from keras.models import load_model
import numpy as np

class Ui_Dialog(QWidget):
    def __init__(self):
        super().__init__()
        self.image_file = 0
        self.setupUi()
        self.Load_model()
        self.pushButton.clicked.connect(self.Button_click)
        self.model

    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(328, 409)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(210, 260, 91, 41))
        self.pushButton.setStyleSheet("font: 9pt \"나눔고딕\";\n"
"background-color: rgb(255, 228, 255);")
        self.pushButton.setAutoDefault(True)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(20, 20, 291, 291))
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(20, 330, 291, 61))
        self.label_2.setStyleSheet("font: 10pt \"Ink Free\";\n"
"background-color: rgb(255, 246, 210);")
        self.label_2.setText("")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label.raise_()
        self.pushButton.raise_()
        self.label_2.raise_()

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "표지판을 알려줘"))
        self.pushButton.setText(_translate("Dialog", "불러오기"))

    def Button_click(self):
        self.image_file, _ = QFileDialog.getOpenFileNames(self)
        self.label.setPixmap(QtGui.QPixmap(self.image_file[0]).scaled(271, 281))
        self.Image_Data(self.image_file[0])

    def Load_model(self):
        self.model = load_model('C:/Users/GyuHyeon/Documents/4-1/컴퓨터비전/기말 과제/traffic_model.h5')
        print("sucess load model")

    def Image_Data(self, file_name):
        image_data = []

        image = cv2.imread(file_name)
        image_fromarray = Image.fromarray(image, 'RGB')
        resize_image = image_fromarray.resize((30, 30))
        image_data.append(np.array(resize_image))

        # Changing the list to numpy array
        image_data = np.array(image_data)
        self.Predic(image_data)

    def Predic(self, image):
        classes = { 0:'Speed limit (20km/h)',
            1:'Speed limit (30km/h)', 
            2:'Speed limit (50km/h)', 
            3:'Speed limit (60km/h)', 
            4:'Speed limit (70km/h)', 
            5:'Speed limit (80km/h)', 
            6:'End of speed limit (80km/h)', 
            7:'Speed limit (100km/h)', 
            8:'Speed limit (120km/h)', 
            9:'No passing', 
            10:'No passing veh over 3.5 tons', 
            11:'Right-of-way at intersection', 
            12:'Priority road', 
            13:'Yield', 
            14:'Stop', 
            15:'No vehicles', 
            16:'Veh > 3.5 tons prohibited', 
            17:'No entry', 
            18:'General caution', 
            19:'Dangerous curve left', 
            20:'Dangerous curve right', 
            21:'Double curve', 
            22:'Bumpy road', 
            23:'Slippery road', 
            24:'Road narrows on the right', 
            25:'Road work', 
            26:'Traffic signals', 
            27:'Pedestrians', 
            28:'Children crossing', 
            29:'Bicycles crossing', 
            30:'Beware of ice/snow',
            31:'Wild animals crossing', 
            32:'End speed + passing limits', 
            33:'Turn right ahead', 
            34:'Turn left ahead', 
            35:'Ahead only', 
            36:'Go straight or right', 
            37:'Go straight or left', 
            38:'Keep right', 
            39:'Keep left', 
            40:'Roundabout mandatory', 
            41:'End of no passing', 
            42:'End no passing veh > 3.5 tons' }

        pred = self.model.predict(image)
        for i in range(len(pred[0])):
            if pred[0][i] == 1.0:
                self.label_2.setText(classes[i])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.show()
    sys.exit(app.exec_())

