class NodeManager:
    """The class to manage the node"""

    def __init__(self):
        self.Nodes = []

    def add_node(self, node):
        self.Nodes.append(node)

    def get_node(self, index):
        return self.Nodes[index]

    def num_nodes(self):
        return len(self.Nodes)

    def cal_node_distance(self, from_index, to_index):
        node_from = self.get_node(from_index)
        node_to = self.get_node(to_index)
        return node_from.distance_to(node_to)
