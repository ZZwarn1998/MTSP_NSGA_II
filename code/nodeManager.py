class nodeManager:
    Nodes = []

    @classmethod
    def addNode(cls, node):
        cls.Nodes.append(node)

    @classmethod
    def getNode(cls, index):
        return cls.Nodes[index]

    @classmethod
    def numberOfNodes(cls):
        return len(cls.Nodes)