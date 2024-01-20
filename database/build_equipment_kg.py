import copy
import json
from datetime import datetime

from ogm import User, models

DATA_PATH = "military.json"
CREATOR = "admin"
GID = -1
COUNTRY_LABEL = "产国"
MANUFACTURER_LABEL = "生产单位"
RESEARCH_LABEL = "研发单位"
CATEGORY_LARGE = "大类"
CATEGORY_SMALL = "类型"
NAME_LABEL = "name"
EQUIPMENT_LABEL = "Equipment"
ADMIN = User(models.User(CREATOR, "", "", "", "", datetime.now()))


def initialize_kg():
    ADMIN.detach_graph(GID)
    try:
        ADMIN.draw_graph("Equipment Knowledge Graph", datetime.now(), datetime.now(), GID)
    except AssertionError:
        ...
    return [g for g in ADMIN.graphs if g.gid == GID][0]


def load_data():
    with open(DATA_PATH, encoding='utf-8') as f:
        lines = f.readlines()

    return [json.loads(line) for line in lines]


def create_countries_manufacturers_researches_nodes(graph, dataset):
    """create country, manufacturer and research nodes"""
    countries = {c for c in map(lambda equipment: equipment.get(COUNTRY_LABEL, None), dataset) if c is not None}
    manufacturers = {m for m in map(lambda equipment: equipment.get(MANUFACTURER_LABEL, None), dataset) if
                     m is not None}
    researches = {r for r in map(lambda equipment: equipment.get(RESEARCH_LABEL, None), dataset) if r is not None}

    def nodes():
        yield from map(lambda c: models.KNode(["COUNTRY"], {"name": c}), countries)
        yield from map(lambda c: models.KNode(["MANUFACTURER"], {"name": c}), manufacturers)
        yield from map(lambda c: models.KNode(["RESEARCH"], {"name": c}), researches)

    for c in nodes():
        graph.draw_node(c)

    print('create_countries_manufacturers_researches_nodes success')


def create_category_nodes(graph, dataset):
    categories_l = {c for c in map(lambda equipment: equipment.get(CATEGORY_LARGE, None), dataset) if c is not None}
    categories_s = {c for c in map(lambda equipment: equipment.get(CATEGORY_SMALL, None), dataset) if c is not None}

    def nodes():
        yield from map(lambda c: models.KNode(["CATEGORY"], {"name": c, "type": "l"}), categories_l)
        yield from map(lambda c: models.KNode(["CATEGORY"], {"name": c, "type": "s"}), categories_s)

    for c in nodes():
        graph.draw_node(c)

    print('create_category_nodes success')


def create_category_relationships(graph, dataset):
    categories = {c for c in map(lambda e: (e.get(CATEGORY_SMALL, None), e.get(CATEGORY_LARGE, None)), dataset)}

    def relationships():
        yield from map(lambda rel: models.KRelationship("BELONG", {},
                                                        graph.find_node(["CATEGORY"], rel[0]).properties["kid"],
                                                        graph.find_node(["CATEGORY"], rel[1]).properties["kid"]),
                       categories)

    for r in relationships():
        graph.draw_relationship(r)

    print("create_category_relationships success")


def create_equipment_nodes(graph, dataset):
    def _reduce_equipment(equipment: dict):
        equipment = copy.deepcopy(equipment)
        equipment[NAME_LABEL] = equipment["名称"]
        equipment["_id"] = equipment["_id"]["oid"]
        for label in (COUNTRY_LABEL, MANUFACTURER_LABEL, RESEARCH_LABEL, CATEGORY_LARGE, CATEGORY_SMALL, "名称"):
            equipment.pop(label, None)
        return equipment

    def _to_model(equipment):
        return models.KNode([EQUIPMENT_LABEL], equipment)

    equipments = map(lambda equipment: _to_model(_reduce_equipment(equipment)), dataset)

    for e in equipments:
        graph.draw_node(e)

    print("create_equipment_nodes success")


def create_equipment_relationships(graph, dataset):
    def _r(label_in_db, label_in_json):
        return [(graph.find_node([EQUIPMENT_LABEL], rel[0]).properties["kid"],
                 graph.find_node([label_in_db], rel[1]).properties["kid"]) for rel in
                map(lambda e: (e.get("名称"), e.get(label_in_json, None)), dataset) if rel[1] is not None]

    country_r = _r("COUNTRY", COUNTRY_LABEL)
    manufacturer_r = _r("MANUFACTURER", MANUFACTURER_LABEL)
    research_r = _r("RESEARCH", RESEARCH_LABEL)
    category_r = _r("CATEGORY", CATEGORY_SMALL)

    for r in country_r:
        relationship = models.KRelationship("LOCATE", {}, r[0], r[1])
        graph.draw_relationship(relationship)

    for r in manufacturer_r:
        relationship = models.KRelationship("PRODUCE", {}, r[1], r[0])
        graph.draw_relationship(relationship)

    for r in research_r:
        relationship = models.KRelationship("STUDY", {}, r[1], r[0])
        graph.draw_relationship(relationship)

    for r in category_r:
        relationship = models.KRelationship("BELONG", {}, r[0], r[1])
        graph.draw_relationship(relationship)

    print("create_equipment_relationships success")


def initialize_equipment_kg():
    graph = initialize_kg()
    dataset = load_data()
    create_countries_manufacturers_researches_nodes(graph, dataset)
    create_category_nodes(graph, dataset)
    create_category_relationships(graph, dataset)
    create_equipment_nodes(graph, dataset)
    create_equipment_relationships(graph, dataset)


if __name__ == "__main__":
    initialize_equipment_kg()
