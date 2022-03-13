from tree_builder.gui import get_codes

def but_show(node_inst):

    if node_inst.node_branch == 0:

        t = get_codes.get_code_street(node_inst)[0] + ' ' + get_codes.get_code_player(node_inst) + '\n' + 'Stack: ' + str(node_inst.stack_o) + '\n'
        t += 'Pot: ' + str(round(node_inst.pot_o - node_inst.to_call, 2))
        if node_inst.to_call > 0:
            t += '\n' + ' + ' + str(round(node_inst.to_call, 2))
        return(t)

    elif node_inst.node_branch == 1:
        t = get_codes.get_code_street(node_inst)[0] + ' ' + get_codes.get_code_player(node_inst) + '\n' + get_codes.get_code_move(node_inst)
        return(t)
