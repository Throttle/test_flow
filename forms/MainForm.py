# coding: utf-8

__author__ = "Alexander Soulimov (alexander.soulimov@gmail.com)"
__copyright__ = "Copyright (c) 2011 A.Soulimov"
__license__ = "Python"

from PySide import QtGui


class Dialog(QtGui.QDialog):

	def __init__(self):
		super(Dialog, self).__init__()

		# create menu
		self.createMenu()

		# create control panel
		self.createHorizontalGroupBox()

		# create parameter edits
		self.createGridGroupBox()

		self.viewParams = QtGui.QGroupBox(u"Выберите файл с данными: ")
		layout = QtGui.QHBoxLayout()
		self.fileNameEdit = QtGui.QLineEdit("")
		self.fileNameEdit.setReadOnly(True)
		self.openFileNameButton = QtGui.QPushButton(u"...")
		self.openFileNameButton.clicked.connect(self.open_file)
		layout.addWidget(self.fileNameEdit)
		layout.addWidget(self.openFileNameButton)
		self.viewParams.setLayout(layout)

		self.logParams = QtGui.QGroupBox(u"Данные для построения дерева: ")
		self.logText = QtGui.QTextEdit()
		self.logText.setFontFamily("Consolas")
		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.logText)
		self.logParams.setLayout(layout)

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setMenuBar(self.menuBar)
		mainLayout.addWidget(self.viewParams)
		mainLayout.addWidget(self.logParams)
		mainLayout.addWidget(self.gridGroupBox)
		mainLayout.addWidget(self.horizontalGroupBox)
		self.setLayout(mainLayout)
		self.setWindowTitle(u"ЛР №3. Метод классификации. Построение дерева принятия решения ID3.")


	def createMenu(self):
		self.menuBar = QtGui.QMenuBar()
		self.fileMenu = QtGui.QMenu(u"&Файл", self)
		self.exitAction = self.fileMenu.addAction(u"&Выход")
		self.menuBar.addMenu(self.fileMenu)
		self.exitAction.triggered.connect(self.accept)

	def createHorizontalGroupBox(self):
		self.horizontalGroupBox = QtGui.QGroupBox(u"Управление: ")
		layout = QtGui.QHBoxLayout()

		button = QtGui.QPushButton(u"Построить дерево")
		button.clicked.connect(self.create_evaluation_tree)
		layout.addWidget(button)

		button = QtGui.QPushButton(u"Показать дерево")
		button.clicked.connect(self.show_tree)
		layout.addWidget(button)

		button = QtGui.QPushButton(u"Классифицировать")
		button.clicked.connect(self.classify)
		layout.addWidget(button)
		self.horizontalGroupBox.setLayout(layout)

	def createGridGroupBox(self):
		self.gridGroupBox = QtGui.QGroupBox(u"Классифицируемый объект: ")
		layout = QtGui.QHBoxLayout()
		self.classifiedObjEdit = QtGui.QLineEdit()
		layout.addWidget(self.classifiedObjEdit)
		self.gridGroupBox.setLayout(layout)


	def create_evaluation_tree(self):
		pass

	def show_tree(self):
		pass

	def classify(self):
		pass

	def open_file(self):
		fileName, filtr = QtGui.QFileDialog.getOpenFileName()
		if fileName:
			self.fileNameEdit.setText(fileName)
			f = open(fileName)
			lines = f.readlines()
			self.logText.setText(reduce(lambda x,y: x + y, lines))




if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	dialog = Dialog()
	sys.exit(dialog.exec_())