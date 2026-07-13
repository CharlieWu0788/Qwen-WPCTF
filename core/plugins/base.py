class BasePlugin:
    name = None
    category = None
    capability = []

    def run(self, context):
        raise NotImplementedError