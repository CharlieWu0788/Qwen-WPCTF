class AttackNode:
    def __init__(self, node_id: str, node_type: str, target: str):
        self.node_id = node_id
        self.node_type = node_type
        self.target = target
        self.attributes = {}

    def add_attribute(self, key, value):
        self.attributes[key] = value

    def to_dict(self):
        return {
            "id": self.node_id,
            "type": self.node_type,
            "target": self.target,
            "attributes": self.attributes
        }