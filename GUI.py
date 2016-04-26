# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 05:55:12 2016

@author: Austin
"""

import sys
from PySide import QtGui
from PySide import QtCore

import data_loader

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
        
        self.map = data_loader.KDMap(data_loader.loadData("business_data.txt"))
        
        self.initUI()
        
    def doQuery(self):
        self._progressbar.setValue(0)
        
        text = ""   
        
        locat = self._locationField.text()
        cats = self._queryField.toPlainText().splitlines()
        if cats[0][0] == '%':
            for c in self.map.categories:
                text += c + "\t"
        
        else:
            text += locat
            if type(locat) == type(u" ") and locat in self.map.cities:
                text += " Valid City."
            text +="\n"
            for i, cat in enumerate(cats):
                cats[i] = cat.strip()
                text += cats[i]
                if cats[i] in self.map.categories:
                    text += ": Valid Category"
                else:
                    text += " is an invalid Category.  Maybe try different caps and plurality?"
                text += "\n"
            text +="\n"
            
            self._result.setText(text)
            
            self._progressbar.setValue(25)        
            
            results = self.map.query(locat, cats)
            
            self._progressbar.setValue(75)
            
            for option in results:
                t = ""
                distance = option[1]
                stuff = option[0]
                #TODO?:Print number
                #TODO?:print the address (reverse-geocode?)
                #print the distance rating
                t += "Distance Rating: " + str(distance) + "\n"
                for cat in stuff:
                    t += "   - "
                    t += cat["name"] 
                    t += "\n        Address: \"" + cat["full_address"].replace("\n", ", ") + "\""
                    t += "\n        Stars: " + str(cat["stars"])
                    t += "\n"
                t += "\n"
                text += t
                
        self._result.setText(text)
        
        self._progressbar.setValue(100)
    
    def initUI(self):
        self._locationField = QtGui.QLineEdit(self)
        self._queryField = QtGui.QTextEdit(self)
        
        submitButton = QtGui.QPushButton("Submit")
        submitButton.setToolTip("Submit query")
        submitButton.clicked.connect(self.doQuery)
        
        self._progressbar = QtGui.QProgressBar(self)
        
        self._progressbar.setValue(0)
        
        locationLabel = QtGui.QLabel("Location")
        queryLabel = QtGui.QLabel("Query")
        resultLabel = QtGui.QLabel("Results")
        
        self._result = QtGui.QTextEdit(self)
        self._result.setReadOnly(True)
        self._locationField.setText("Las Vegas")
        self._queryField.setText("Shopping\nParks\nFood")
        self._result.setText("Remember to capitolize the starting letters of each word.")
        #self._result.setText("1) Clyde Street\n    - Baker's Dozen\n    - Low Green\n    - Thompson's" +
        #    "\n2) Tomez Street\n    - Oak n' Spoon\n    - High Green\n    - Barrowfield Bakery" )
        
        topGrid = QtGui.QGridLayout()
        topGrid.setSpacing(10)
        
        topGrid.addWidget(locationLabel, 1, 0, QtCore.Qt.AlignTop)
        topGrid.addWidget(self._locationField, 1, 1)
        topGrid.addWidget(queryLabel, 2, 0, QtCore.Qt.AlignTop)
        topGrid.addWidget(self._queryField, 2, 1)
        
        topGrid.addWidget(submitButton, 3, 0)
        topGrid.addWidget(self._progressbar, 3, 1)
        
        topGrid.addWidget(resultLabel, 4, 0, QtCore.Qt.AlignTop)
        topGrid.addWidget(self._result, 4, 1)
        
        mainH = QtGui.QHBoxLayout()
        mainH.addLayout(topGrid)
        
        protoMap = QtGui.QPixmap("images\old_map_of_glasgow.jpg")
        mapArea = QtGui.QLabel(self)
        mapArea.setPixmap(protoMap)     
        scrollArea = QtGui.QScrollArea()
        scrollArea.setWidget(mapArea) 
        scrollArea.setWidgetResizable(True)
        #TEMPORARILY COMMENTED OUT SCROLLAREA
        #mainH.addWidget(scrollArea)
        
        
        self.setWindowTitle("Area Finder") 
        self.setWindowIcon(QtGui.QIcon("images\Avosoft-Warm-Toolbar-World.Ico"))
        
        self.setLayout(mainH)
        self.setGeometry(300,300,250,150)
        self.show()

    
        
ex = SelectPage()

sys.exit(app.exec_())
