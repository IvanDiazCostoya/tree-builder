def print_node_info(gui, node_inst):
    ''' Text in NodeInfoResultsText. Not a table
    It's the square of text right underneath the build tree button
    '''

    # The button previously clicked goes back to default background color
    gui.buttons[gui.clicked].setStyleSheet('background-color: light gray')

    # New clicked index
    gui.clicked = node_inst.ind

    # New clicked button changes background color
    gui.buttons[node_inst.ind].setStyleSheet('background-color: rgb(58, 190, 255)')

    # Display node/branch info
    gui.NodeInfoResultsText.setText(str(node_inst))
