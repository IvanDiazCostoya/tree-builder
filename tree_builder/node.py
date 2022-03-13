from tree_builder.tree_tools import get_previous
from tree_builder.gui import get_codes

class Node:
    def __init__(self, parent, moves, tree=None):
        ''' Builds a node '''

        # 0 is node, 1 is branch
        self.node_branch = 0

        # Parent node
        self.parent = parent

        # We need to attach the tree to the node to pass global information
        if not self.parent:
            # We only have to specify the tree of the root node
            self.tree = tree
        else:
            self.tree = self.parent.tree

        # Index in the list
        # Used for printing the tree in the scroll area
        self.ind = None

        # When it's creadted a node is always a leaf, when another leaf is
        # attached, it stops being a leaf
        # Used for printing the tree in the scroll area
        self.leaf = True

        if self.parent:
            self.parent.leaf = False
            self.parent.children.append(self)

        # Children nodes
        self.children = []

        # Coords in the map
        self.coords = None

        # Player
        if not self.parent or self.parent.street_end:
            self.player = 0
        else:
            self.player = not self.parent.player

        # Stack
        # If it's the root node or the first IP node the stack is the initial one
        if not self.parent or (self.parent.parent and not self.parent.parent.parent and self.player == 1):
            self.stack_o = self.tree.stack
            self.stack_f = self.stack_o

        # If it's not the root node or the first IP node the stack
        # is taken from final stack in the last node or branch of the same player
        # Nodes don't change the stack, only the branches, so final stack is the same as initial stack always in nodes
        else:
            prev_own_node_or_branch = get_previous.get_previous_own_node_or_branch(self)

            self.stack_o = prev_own_node_or_branch.stack_f
            self.stack_f = self.stack_o

        # Pot of root node is the initial pot of the tree
        if not self.parent:
            self.pot_o = self.tree.pot
            self.pot_f = self.pot_o
        # if its is not the root node the initial is taken from
        # final stack in the last node of the same player
        else:
            self.pot_o = parent.pot_f
            self.pot_f = self.pot_o

        # Street
        # The root node starts always in flop
        if not self.parent:
            self.street = 1
        # If las branch was street end we add one street, unless it's already river
        elif self.parent.street_end and self.parent.street_end < 3:
            self.street = self.parent.street + 1
        # Otherwise it is the same street as last branch
        else:
            self.street = self.parent.street

        # Ammount to call
        if self.parent and self.street == self.parent.street:
            self.to_call = self.parent.move[1]
        else:
            self.to_call = 0

        self.moves = []

    def __repr__(self):
        t = 'Node number: ' + str(self.ind) + '\nPlayer: ' + get_codes.get_code_player(self) + '\n'
        t += 'Street: ' + get_codes.get_code_street(self) + '\n'
        t += 'Stack: ' + str(round(self.stack_o, 2)) + '\n'
        t += 'Pot: ' + str(round(self.pot_o - self.to_call, 2))
        if self.to_call > 0:
            t += ' + ' + str(round(self.to_call, 2))
        t += '\n'
        t += 'To call: ' + str(round(self.to_call, 2)) + '\n'
        tmp = [get_codes.get_code_move(a) for a in self.children]
        tmp = '\n'.join(tmp)
        t += 'Moves: '
        t += tmp
        t += '\n'

        return(t)
