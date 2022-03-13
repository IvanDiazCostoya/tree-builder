from tree_builder.gui import get_codes

class Branch:
    def __init__(self, parent, move):

        # 0 is node, 1 is branch
        self.node_branch = 1

        # Index in the list of nodes
        self.ind = None

        # Parent node
        self.parent = parent

        # We need to attach the tree to the node to pass global information
        self.tree = self.parent.tree

        # Always same street as parent
        self.street = self.parent.street

        # When it's created a node is always a leaf, when another leaf is
        # attached, it stops being a leaf
        self.leaf = True
        if self.parent:
            self.parent.leaf = False
            self.parent.children.append(self)

        # Children nodes
        self.children = []

        # Coords in the mapping
        self.coords = None

        # Player
        self.player = self.parent.player

        # Move
        self.move = move

        # Initial stack
        self.stack_o = self.parent.stack_o

        # Final stack
        if self.parent.parent and self.parent.parent.move[0] >= 3 and self.move[0] == 4:
            self.stack_f = self.stack_o - move[1] - self.parent.to_call
        else:
            self.stack_f = self.stack_o - move[1]

        # Initial pot
        self.pot_o = self.parent.pot_f

        # Final pot
        if self.parent.parent and self.parent.parent.move[0] >= 3 and self.move[0] == 4:
            self.pot_f = self.parent.pot_f + move[1] + self.parent.to_call
        else:
            self.pot_f = self.parent.pot_f + move[1]

        # Street
        self.street = self.parent.street

        # Street is finished or not
        if (self.parent.parent and self.parent.parent.street == self.street) \
        and (self.move[0] == 2 or \
        (self.move[0] == 1 and self.parent.parent.move[0] == 1)):
            self.street_end = True
        else:
            self.street_end = False

    def __repr__(self):
        t = 'Branch number: ' + str(self.ind) + '\nPlayer: ' + get_codes.get_code_player(self) + '\n'
        t += 'Street: ' + get_codes.get_code_street(self) + '\n'
        t += 'Initial stack: ' + str(round(self.stack_o, 2)) + '\n'
        t += 'Final stack: ' + str(round(self.stack_f, 2)) + '\n'
        t += 'Initial pot: ' + str(round(self.pot_o, 2)) + '\n'
        t += 'Final pot: ' + str(round(self.pot_f, 2)) + '\n'
        t += 'Move: '
        t += get_codes.get_code_move(self)
        t += '\n'

        return(t)
