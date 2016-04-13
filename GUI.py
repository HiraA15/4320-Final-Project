# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 05:55:12 2016

@author: Austin
"""

import sys
from PySide import QtGui
from PySide import QtCore

app = QtGui.QApplication(sys.argv)

'''
wid = QtGui.QWidget()
wid.resize(250, 150)
wid.setWindowTitle('Simple')
wid.show()
'''
def testFunc():
    print 'test'

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        btn = QtGui.QPushButton('Button', self)
        btn.setToolTip('Test Button')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)        
        
        btn.clicked.connect(testFunc)
                
        self.setGeometry(300,300,250,150)
        self.setWindowTitle('Example')
        #self.setWindowIcon(QtGui.QIcon('web.png'))
        
        self.show()

#class SearchTermManager(QtGui.QWidget):
    
#class ResultPage(QtGui.QWidget):
    
#class MapPage(QtGui.QWidget):
    
#TODO!  QStackedLayout
    
#TODO: Business Widget
        
class SelectPage(QtGui.QWidget):
    def __init__(self):
        super(SelectPage, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        self._locationField = QtGui.QLineEdit(self)
        self._queryField = QtGui.QTextEdit(self)
        
        submitButton = QtGui.QPushButton("Submit")
        submitButton.setToolTip("Submit query")
        
        self._progressbar = QtGui.QProgressBar(self)
        
        self._progressbar.setValue(30)
        
        locationLabel = QtGui.QLabel("Location")
        queryLabel = QtGui.QLabel("Query")
        resultLabel = QtGui.QLabel("Results")
        
        protoResult = QtGui.QTextEdit(self)
        protoResult.setReadOnly(True)
        self._locationField.setText("Glasglow")
        self._queryField.setText("Bakery\npark\nbar")
        protoResult.setText("1) Clyde Street\n    - Baker's Dozen\n    - Low Green\n    - Thompson's" +
            "\n2) Tomez Street\n    - Oak n' Spoon\n    - High Green\n    - Barrowfield Bakery" )
        
        topGrid = QtGui.QGridLayout()
        topGrid.setSpacing(10)
        
        topGrid.addWidget(locationLabel, 1, 0, QtCore.Qt.AlignTop)
        topGrid.addWidget(self._locationField, 1, 1)
        topGrid.addWidget(queryLabel, 2, 0, QtCore.Qt.AlignTop)
        topGrid.addWidget(self._queryField, 2, 1)
        
        topGrid.addWidget(submitButton, 3, 0)
        topGrid.addWidget(self._progressbar, 3, 1)
        
        topGrid.addWidget(resultLabel, 4, 0, QtCore.Qt.AlignTop)
        topGrid.addWidget(protoResult, 4, 1)
        
        mainH = QtGui.QHBoxLayout()
        mainH.addLayout(topGrid)
        
        protoMap = QtGui.QPixmap("images\old_map_of_glasgow.jpg")
        mapArea = QtGui.QLabel(self)
        mapArea.setPixmap(protoMap)     
        scrollArea = QtGui.QScrollArea()
        scrollArea.setWidget(mapArea) 
        scrollArea.setWidgetResizable(True)
        mainH.addWidget(scrollArea)
        
        
        self.setWindowTitle("Area Finder") 
        self.setWindowIcon(QtGui.QIcon("images\Avosoft-Warm-Toolbar-World.Ico"))
        
        self.setLayout(mainH)
        self.setGeometry(300,300,250,150)
        self.show()

    
        
ex = SelectPage()

sys.exit(app.exec_())
