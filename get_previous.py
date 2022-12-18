def get_previous_own_node_or_branch(node_inst):
    ''' Returns the previous last own node or branch in the sequence that leads to this node instance '''

    tmp_node = node_inst.parent
    while tmp_node.player != node_inst.player:
        tmp_node = tmp_node.parent

    return(tmp_node)
