'''
Transforms numerical data into text to print in human readable format
'''

def get_code_move(node):
    if node.move == (0, 0):
        return('Fold')
    if node.move == (1, 0):
        return('Check')
    if node.move[0] == 2:
        return('Call ' + str(round(node.move[1], 2)))
    if node.move[0] == 3:
        return('Bet ' + str(round(node.move[1], 2)))
    if node.move[0] == 4:
        return('Raise ' + str(round(node.parent.to_call, 2)) + '\n' + ' + ' + str(round(node.move[1], 2)))

def get_code_player(node):
    if node.player == 0:
        return('OOP')
    elif node.player == 1:
        return('IP')

def get_code_street(node):
    if node.street == 0:
        return('PreFlop')
    elif node.street == 1:
        return('Flop')
    elif node.street == 2:
        return('Turn')
    elif node.street == 3:
        return('River')
