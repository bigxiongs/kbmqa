class Statement:
    def __init__(self, label: str):
        self.label = label
        self.alias = label[:1].lower()
        self.parameters = {}
        self.match_clause = ""
        self.where_clause = ""
        self.set_clause = ""
        self.create_clause = ""
        self.delete_clause = ""

    @classmethod
    def match(cls, node):
        label = node.__name__
        return cls(label)

    def where(self, parameters: dict):
        if not self.where_clause:
            self.where_clause = "WHERE"
        for k, v in parameters.items():
            self.where_clause += " %s.%s = $%s" % (self.alias, k, k)
            self.parameters[k] = v




