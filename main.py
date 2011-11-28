# coding: utf-8
from PySide import QtGui
import sys
from forms.MainForm import Dialog

__author__ = "Alexander Soulimov (alexander.soulimov@gmail.com)"
__copyright__ = "Copyright (c) 2011 A.Soulimov"
__license__ = "Python"



def main(argv):
	"""

	"""
	app = QtGui.QApplication(sys.argv)
	dialog = Dialog()
	sys.exit(dialog.exec_())


if __name__ == "__main__":
	main(sys.argv[1:])