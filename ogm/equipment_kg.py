from ogm import Graph, models
from database.session import execute


class EquipmentGraph(Graph):
    _match_graph_stmt = """MATCH (u:User {name: "admin"})-->(g:Graph {gid: -1})-->"""
    _match_equipment_nodes = execute(_match_graph_stmt + """(k:Equipment) RETURN k""")
    _match_country_nodes = execute(_match_graph_stmt + """(k:COUNTRY) RETURN k""")
    _match_manufacturer_nodes = execute(_match_graph_stmt + """(k:MANUFACTURER) RETURN k""")
    _match_research_nodes = execute(_match_graph_stmt + """(k:RESEARCH) RETURN k""")
    _match_category_nodes = execute(_match_graph_stmt + """(k:CATEGORY) RETURN k""")

    def __init__(self, graph):
        super().__init__(graph)

    @staticmethod
    def records2nodes(records):
        k_nodes = [r["k"] for r in records]
        k_nodes = [models.KNode(node.labels, dict(node.items())) for node in k_nodes]
        return k_nodes

    @property
    def equipment_nodes(self):
        records = EquipmentGraph._match_equipment_nodes({})
        return EquipmentGraph.records2nodes(records)

    @property
    def country_nodes(self):
        records = EquipmentGraph._match_country_nodes({})
        return EquipmentGraph.records2nodes(records)

    @property
    def manufacturer_nodes(self):
        records = EquipmentGraph._match_manufacturer_nodes({})
        return EquipmentGraph.records2nodes(records)

    @property
    def research_nodes(self):
        records = EquipmentGraph._match_research_nodes({})
        return EquipmentGraph.records2nodes(records)

    @property
    def category_nodes(self):
        records = EquipmentGraph._match_category_nodes({})
        return EquipmentGraph.records2nodes(records)

