from tree_builder import node
from tree_builder import branch

class Tree:
    def __init__(self, stack, pot):
        ''' Generates a tree
        '''

        # List of nodes and branches in the tree
        self.nodes = []

        # self.x and self.y will be used for mapping the nodes and branches in the tree.
        self.x = 0
        self.y = 0

        # Stack from the parameters
        self.stack = float(stack)

        # Pot taken from the parameters
        self.pot = float(pot)

        self.build_tree()

    def build_tree(self):

        # First the root node: OOP, BB
        root_node = node.Node(parent=None,
                                moves=None,
                                tree=self)

        bet_sizes = self.get_bet_sizes(root_node)

        root_node.moves = [(3, bet_size) for bet_size in bet_sizes]
        root_node.moves = root_node.moves + [(1, 0)]

        self.branch_out(root_node)

        self.get_node_coords(root_node)

    def branch_out(self, node_inst):
        ''' Recursive function to create the nodes '''

        # If it comes from the root node
        if not node_inst.parent:

            # root node bets
            bet_amm = self.get_bet_sizes(node_inst)

            for i in bet_amm:
                # root node OOP bets
                branch2 = branch.Branch(parent=node_inst, move=(3, i))
                self.branch_out(branch2)

            # root_node checks
            branch1 = branch.Branch(parent=node_inst, move=(1, 0))

            self.branch_out(branch1)

        else:
            # New street
            if (node_inst.street < 3 and node_inst.node_branch == 1 and node_inst.street_end and node_inst.stack_f > 0):

                node7 = node.Node(parent=node_inst,
                                    moves=None)

                bet_sizes = self.get_bet_sizes(node7)
                node7.moves = [(3, bet_size) for bet_size in bet_sizes]
                node7.moves = node7.moves + [(1, 0)]

                for i in node7.moves:
                    branch2 = branch.Branch(parent=node7, move=i)
                    self.branch_out(branch2)

            # It comes checked from OOP
            elif node_inst.node_branch == 1 and node_inst.move[0] == 1 and node_inst.player == 0:

                node2 = node.Node(parent=node_inst,
                                    moves=None)

                bet_sizes = self.get_bet_sizes(node2)
                node2.moves = [(3, bet_size) for bet_size in bet_sizes]
                node2.moves = node2.moves + [(1, 0)]

                for i in node2.moves:
                    #  IP
                    branch2 = branch.Branch(parent=node2, move=i)
                    if not (branch2.street == 3 and branch2.move == (1, 0)):
                        self.branch_out(branch2)

            # Hand comes betted
            elif node_inst.node_branch == 1 and node_inst.move[0] == 3:
                node3 = node.Node(parent=node_inst,
                                    moves=None)

                if node_inst.move[1] < node3.stack_o:
                    node3.moves = [(4, self.get_raise_size(node3)), (2, node_inst.move[1]), (0, 0)]
                else:
                    node3.moves = [(2, node_inst.move[1]), (0, 0)]

                for i in node3.moves:
                    branch2 = branch.Branch(parent=node3, move=i)
                    self.branch_out(branch2)

            # Hand comes raised
            elif node_inst.node_branch == 1 and node_inst.move[0] == 4:
                node8 = node.Node(parent=node_inst,
                                    moves=None)

                if node_inst.move[1] < node8.stack_o:
                    node8.moves = [(4, self.get_raise_size(node8)), (2, node_inst.move[1]), (0, 0)]
                else:
                    node8.moves = [(2, node_inst.move[1]), (0, 0)]

                for i in node8.moves:
                    branch9 = branch.Branch(parent=node8, move=i)
                    self.branch_out(branch9)

    def get_node_coords(self, node_inst):
        ''' Gets the coordinates of a node or branch for mapping it on the screen
        The tree is already built.
        '''

        # Always +1 in the x coordinate respect the parent
        if node_inst.parent:
            self.x = node_inst.parent.coords[0] + 2

        # Set the coordinates of the node in the map
        node_inst.coords = (self.x, self.y)

        # If it is a terminal node
        if node_inst.leaf:
            self.y += 1

        self.nodes.append(node_inst)
        node_inst.ind = len(self.nodes) - 1

        # Recursion
        for i in node_inst.children:
            self.get_node_coords(i)

    def get_bet_sizes(self, node_inst):

        if node_inst.stack_o > 0:

            spr = node_inst.stack_o / node_inst.pot_o
            ammounts = []
            if spr < 2:
                ammounts.append(node_inst.stack_o)
            if spr >= 2 and self.pot < 3:
                ammounts.append(0.5 * node_inst.pot_o)
            if spr >= 2 and self.pot >= 3:
                ammounts.append(0.3333 * node_inst.pot_o)
            if spr >= 3 and self.pot >= 3:
                ammounts.append(0.5 * node_inst.pot_o)
            if spr >= 4 and self.pot >= 3:
                ammounts.append(0.8 * node_inst.pot_o)
            if spr >= 4 and self.pot >= 3:
                ammounts.append(1.5 * node_inst.pot_o)

            return(ammounts)

    def get_raise_size(self, node_inst):
        ''' Determines the raise size given the effective stack and pot in that situation '''

        # Size of the villain's bet
        bet = node_inst.parent.move[1]

        # If there is space for a raise
        if bet < node_inst.stack_o:

            # Raise all in
            # What is higher the pot or the bet x 3
            b2 = max(node_inst.parent.pot_o, bet * 3)

            # Pot after raise - call
            p2 = b2 * 2 + node_inst.parent.pot_o
            # Stack after raise - call
            s2 = node_inst.parent.stack_o - b2

            # SPR after raise call = s2 / p2
            if s2 / p2 < 0.75:
                raise_ = node_inst.stack_o

            else:

                # At least we will raise to the pot size
                if bet * 3 < node_inst.parent.pot_o:
                    raise_ = node_inst.parent.pot_o

                # bet x 3 >= pot
                else:

                    # OOP
                    if node_inst.player == 0:

                        # We are OOP we raise x 4 if result spr >= 0.75
                        # Pot after raise - call
                        # pot 2 stack 9 p2 = 2 + 1 * 4 = 6
                        p2 = node_inst.parent.pot_o + 2 * bet * 4
                        # Stack después del raise - call
                        # pot 2 stack 9 s2 = 9 - 1 * 4 = 5
                        s2 = node_inst.parent.stack_o - bet * 4

                        if s2 / p2 >= 0.75:

                            raise_ = bet * 4

                        # We are OOP we raise x 3 if x 4 spr result < 0.75 but x 3 spr result >= 0.75
                        else:

                            raise_ = bet * 3

                    # We are IP we raise x 3 if result spr >= 0.75
                    else:
                        raise_ = bet * 3

            return(raise_ - bet)
