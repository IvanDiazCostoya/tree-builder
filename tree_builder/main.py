from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap
import sys
import os

from tree_builder.gui import print_node_info
from tree_builder.gui import print_button_text
from tree_builder import tree

class UI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load ui file from PyQt5 designer
        gui_dir = os.path.dirname(os.path.realpath(__file__))
        gui_file = os.path.join(gui_dir, 'gui/gui.ui')
        uic.loadUi(gui_file, self)

        # Move to the left upper corner
        self.move(0, 0)

        # Connect button build tree to function print tree
        self.ButtonBuildTree.clicked.connect(self.build_tree_clicked)

        # List of buttons in the tree.
        # We need the list to change their properties when clicked
        self.buttons = []

        # Index of button clicked in the buttons list.
        self.clicked = None

    def build_tree_clicked(self):
        ''' Button with text 'Build tree' in the Tree info square is clicked '''

        # Delete tree from the scroll area, and other fields
        self.delete()

        self.NodeInfoResultsText.setText('')

        # Build new tree
        a = str(self.InputEffStack.text())
        b = str(self.InputPot.text())

        self.t = tree.Tree(stack=a, pot=b)

        # Print tree in the scroll area
        self.print_tree()

    def delete(self):
        ''' Delete all the tree in the scroll area'''

        # No button is clicked
        self.clicked = 0

        # Erase previous list of buttons
        self.buttons = []

        # When we set a widget parent to None, it is deleted
        for i in reversed(range(self.treeMap_gridLayout.count())):
            self.treeMap_gridLayout.itemAt(i).widget().setParent(None)

    def print_tree(self):
        ''' Print the tree in the scroll area'''

        # Coordinates of first button (360, 20, 71, 71)
        # x advances (80, 0, 0, 0)
        # y advances (0, 80, 0, 0)

        directory = os.path.dirname(os.path.realpath(__file__))
        img1 = os.path.join(directory, 'gui/img/arrow_1.jpg')
        img2 = os.path.join(directory, 'gui/img/arrow_2.jpg')
        img3 = os.path.join(directory, 'gui/img/arrow_3.jpg')
        img4 = os.path.join(directory, 'gui/img/arrow_4.jpg')
        img5 = os.path.join(directory, 'gui/img/arrow_5.jpg')

        for h, node in enumerate(self.t.nodes):

            # Coordinates of the node
            x = node.coords[0]
            y = node.coords[1]

            # New button for a node or branch
            self.testButton = QPushButton()

            # Info showed on the button
            self.testButton.setText(print_button_text.but_show(node))

            # If clicked shows branch/node info
            self.testButton.clicked.connect(lambda ch, node=node: print_node_info.print_node_info(self, node))

            # fixed size for the scroll area behaviour
            self.testButton.setFixedSize(QtCore.QSize(71, 71))

            # Add the button to the button list
            self.buttons.append(self.testButton)

            # Add label that will hold the arrow
            self.arrowLabel = QLabel()

            # Not sure this line is necesary. Check with bigger trees
            self.arrowLabel.setAlignment(QtCore.Qt.AlignLeft)

            # fixed size for the scroll area behaviour
            self.arrowLabel.setFixedSize(QtCore.QSize(71, 71))

            # Add this button to the scroll layout in coordinates y and x
            self.treeMap_gridLayout.addWidget(self.testButton, y , x)

            # If it has children
            if not node.leaf:
                # One children means --> arrow
                if len(node.children) == 1:
                    pixmap = QPixmap(img1)

                # More than one children means --||--> arrow
                elif len(node.children) > 1:
                    pixmap = QPixmap(img2)

                    for p in range(len(node.children) - 1):

                        # Coordinate y of one children
                        y1 = node.children[p].coords[1]

                        # Coordinate y of next children
                        y2 = node.children[p+1].coords[1]

                        # Height difference between two children
                        dif = y2 - y1

                        if dif > 1:
                            for p in range(dif - 1):

                                self.arrowLabel3 = QLabel()
                                self.arrowLabel3.setAlignment(QtCore.Qt.AlignLeft)
                                self.arrowLabel3.setFixedSize(QtCore.QSize(71, 71))
                                self.treeMap_gridLayout.addWidget(self.arrowLabel3, y1 + 1 + p , x + 1)

                                # Image |
                                pixmap3 = QPixmap(img5)
                                self.arrowLabel3.setPixmap(pixmap3)

                self.treeMap_gridLayout.addWidget(self.arrowLabel, y , x + 1)

                self.arrowLabel.setPixmap(pixmap)

            last_node_y = self.t.nodes[h-1].coords[1]

            if y > last_node_y:
                self.arrowLabel2 = QLabel()
                self.arrowLabel2.setAlignment(QtCore.Qt.AlignLeft)
                self.arrowLabel2.setFixedSize(QtCore.QSize(71, 71))
                self.treeMap_gridLayout.addWidget(self.arrowLabel2, y , x - 1)
                list_children = node.parent.children
                my_index = list_children.index(node)

                # First index
                if my_index == 0:
                    pixmap2 = QPixmap(img2)

                # Middle index
                if my_index > 0 and my_index < len(list_children) - 1:
                    pixmap2 = QPixmap(img4)

                # Last index
                if my_index == len(list_children) - 1:
                    pixmap2 = QPixmap(img3)

                self.arrowLabel2.setPixmap(pixmap2)

if __name__ == '__main__':

    # Initialize the App
    app = QApplication(sys.argv)
    UIWindow = UI()
    # Show the App
    UIWindow.show()
    sys.exit(app.exec())
