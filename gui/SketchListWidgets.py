# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

import gui.widgets

from gui.icons import Ico 
from gui.icons import Icon 

"""
Displays the directories for sketches
Currently two modes, broswse USER sketches, or Examples

TODO - maybe these need to be split up
"""
class SketchesBrowser(QtGui.QSplitter):
	def __init__(self,  parent, main):
		QtGui.QDockWidget.__init__(self, parent)

		self.main = main

		sketchesWidget = SketchListWidget("Sketches", self, self.main)
		self.addWidget(sketchesWidget)
		self.connect(sketchesWidget, QtCore.SIGNAL("open_sketch"), self.on_open_sketch)

		examplesWidget = SketchListWidget("Examples", self, self.main)
		self.addWidget(examplesWidget)
		self.connect(examplesWidget, QtCore.SIGNAL("open_sketch"), self.on_open_sketch)
		
	def on_open_sketch(self, file_path):
		print "BROWSER", file_path
		self.emit(QtCore.SIGNAL("open_sketch"), file_path)


##UNUSED
class UNUSED_SketchListDockWidget(QtGui.QDockWidget):

	MODE_USER = 0
	MODE_EXAMPES = 1
	
	def __init__(self, title, parent, main):
		QtGui.QDockWidget.__init__(self, title, parent)

		self.main = main
		
		containerWidget = QtGui.QWidget()
		self.setWidget(containerWidget)

		self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)


class SketchListWidget(QtGui.QWidget):
	
	def __init__(self, title, parent, main):
		QtGui.QWidget.__init__(self, parent)

		self.main = main
		if title == "Examples":
			self.dir_to_browse = self.main.settings.examples_path()
		else:
			self.dir_to_browse = self.main.settings.sketches_path()

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0,0,0,0)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)

		headLabel = gui.widgets.HeaderLabel(self, self.main, icon=Ico.Sketches, title=title, color="black", wash_to="#456D91")
		mainLayout.addWidget(headLabel)



		## redundant listings
		if 1 == 0:
			self.treePlaces = QtGui.QTreeWidget()
			mainLayout.addWidget(self.treePlaces, 1)
			self.treePlaces.headerItem().setText(0, "Location")
			self.treePlaces.headerItem().setText(1, "Path")
			self.treePlaces.header().hide()
			self.treePlaces.setColumnHidden(1, True)
			self.treePlaces.setRootIsDecorated(False)
			self.treePlaces.setAlternatingRowColors(True)
			self.connect(self.treePlaces, QtCore.SIGNAL("itemClicked (QTreeWidgetItem *,int)"), self.on_tree_place_clicked)
			for foo in [["Examples", self.main.settings.examples_path()],["Sketches", self.main.settings.sketchbooks_path()]]:
				item = QtGui.QTreeWidgetItem()
				self.treePlaces.addTopLevelItem(item)
				item.setText(0, foo[0])
				font = item.font(0)
				font.setBold(True)
				item.setFont(0, font)
				item.setIcon(0, Icon(Ico.Folder))
				if foo[1]:
					item.setText(1, foo[1])

			self.dir_to_browse = None


		toolbar = QtGui.QToolBar(self)
		toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		#toolbar.setHeight(0)
		mainLayout.addWidget( toolbar )
		
		self.toolButtonGroup = QtGui.QButtonGroup(self)
		self.toolButtonGroup.setExclusive(True)
		self.connect(self.toolButtonGroup, QtCore.SIGNAL("buttonClicked(QAbstractButton *)"), self.on_view_selected)

		listButton = QtGui.QToolButton()
		listButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		listButton.setText("List")
		listButton.setIcon(Icon(Ico.Yellow))
		listButton.setStyleSheet("padding: 0px; margin: 0px;")
		listButton.setCheckable(True)
		listButton.setChecked(True)
		toolbar.addWidget(listButton)
		self.toolButtonGroup.addButton(listButton, 0)

		listButton = QtGui.QToolButton()
		listButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		listButton.setText("Tree")
		listButton.setIcon(Icon(Ico.Black))
		listButton.setStyleSheet("padding: 0px; margin: 0px;")
		listButton.setCheckable(True)
		toolbar.addWidget(listButton)
		self.toolButtonGroup.addButton(listButton, 1)

		#######################################
		## Tree
		#######################################
		self.tree = QtGui.QTreeWidget()
		mainLayout.addWidget(self.tree, 10)
		
		self.tree.setSortingEnabled(True)
		self.tree.setRootIsDecorated(True)
		self.tree.setAlternatingRowColors(False)
		self.tree.headerItem().setText(0, "Files")
		self.connect(self.tree, QtCore.SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"), self.on_tree_double_clicked)
		self.connect(self.tree, QtCore.SIGNAL("itemClicked (QTreeWidgetItem *,int)"), self.on_tree_clicked)

		self.load_list()

	def on_tree_place_clicked(self, item, col):
		self.dir_to_browse = item.text(1)
		self.load_list()
		

	def on_view_selected(self, button):
		for bitt in self.toolButtonGroup.buttons():
			if bitt.isChecked():
				bitt.setIcon(Icon(Ico.Yellow))
			else:
				bitt.setIcon(Icon(Ico.Black))
		self.load_list()
	#################################################################
	## Tree Events
	#################################################################
	def on_tree_clicked(self, item, col):
		return
		#print "on_tree_clicked", item, col
		data = item.data(0, QtCore.Qt.UserRole)
		print data
		if not data.isNull():
			#if data.toString() == "pde":
			print "YES", data.toString()
		

	def on_tree_double_clicked(self, item, col):
		#print "on_tree_double_clicked", item, col
		#print "on_tree_clicked", item, col
		data = item.data(0, QtCore.Qt.UserRole)
		print "oepn", data.toString()
		if not data.isNull():
			#if data.toString() == "pde":
			#print "YES", data.toString()
			self.emit(QtCore.SIGNAL("open_sketch"), data.toString())
			#pdeFile = QtCore.QFile(data.toString())
			#if not pdeFile.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
			#	print "oops"
			#	return
			#all_file = pdeFile.readAll()
			#all_file_string = QtCore.QString(all_file)
			

		#progFile = QtCore.QFile(prog_file)
		#if not progFile.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
			#print "oops"
			#return
		
		#while not progFile.atEnd():
			#line = progFile.readLine();
	#################################################################
	## Load Files
	#################################################################
	def load_list(self):
		#print "ROOO = ", self.dir_to_browse
		self.tree.model().removeRows(0, self.tree.model().rowCount())
		if not self.dir_to_browse:
			return
		fileInfo = QtCore.QFileInfo(self.dir_to_browse)
		#print self.dir_to_browse
		if not fileInfo.exists():
			QtGui.QMessageBox.information(self, "OOps", " the dir %s was not found" % self.dir_to_browse)
			return
		#rootNode = self.tree.invisibleRootItem()
		self.walk_dir(fileInfo.filePath(),  self.tree.invisibleRootItem())
		self.tree.sortItems(0, QtCore.Qt.AscendingOrder)

	def walk_dir(self, dir_path, parentNode):
		dir_path = QtCore.QDir(dir_path)
		#print dir_path
		info_list = dir_path.entryInfoList(QtCore.QDir.AllEntries | QtCore.QDir.NoDotAndDotDot)
		#print info_list

		
		isList =  self.toolButtonGroup.checkedId() == 0

		
		for fileInfo in info_list:
			if fileInfo.isDir():
	
				if isList:
					self.walk_dir(fileInfo.filePath(), parentNode)
				else:
					treeItem = QtGui.QTreeWidgetItem(parentNode)
					treeItem.setText(0, fileInfo.fileName() ) ## hack to remove .html
					treeItem.setIcon(0, Icon(Ico.Folder))
					self.walk_dir(fileInfo.filePath(), treeItem)
			#self.tree.addTopLevelItem(treeItem)
			#self.tree.setItemExpanded(treeItem, True)
			#return
			else:
				#print "pde" , fileInfo.filePath()
				if fileInfo.suffix() == 'pde':
					treeItem = QtGui.QTreeWidgetItem(parentNode)
					treeItem.setText(0, fileInfo.fileName() ) ## hack to remove .html
					treeItem.setData(0, QtCore.Qt.UserRole, fileInfo.filePath() )
					treeItem.setIcon(0, Icon(Ico.Sketch))
					#self.tree.addTopLevelItem(treeItem)
					#self.tree.setItemExpanded(treeItem, True)