import json
from functools import reduce

from rapidfuzz import fuzz
import requests

from kg.build_equipment_kg import GRAPH

DATA_PATH = "./searching/equipment_keywords.json"
FASTGPT_API = "fastgpt-Vg1WnaXIyW7RpTneyqp0ITYbC"
BASE_URL = "https://api.fastgpt.in/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {FASTGPT_API}",
    "Content-Type": "application/json"
}

with open(DATA_PATH, encoding='utf-8') as f:
    EQUIPMENT_KEYWORDS = json.loads(f.read())


def payload(question) -> dict:
    return {
        "stream": False,
        "detail": False,
        "variables": {
            "uid": "",
            "name": ""
        },
        "messages": [
            {
                "content": question,
                "role": "user"
            }
        ]
    }


def search(_question: str):
    _answer = answer(_question)

    equipments = {e: r for e in EQUIPMENT_KEYWORDS["Equipment"]
                  if (r := max(fuzz.ratio(e, _question), fuzz.ratio(e, _answer))) > 60}
    countries = {c for c in EQUIPMENT_KEYWORDS["COUNTRY"] if c in _question or c in _answer}
    manufacturers = {m for m in EQUIPMENT_KEYWORDS["MANUFACTURER"] if m in _question or m in _answer}
    researches = {r for r in EQUIPMENT_KEYWORDS["RESEARCH"] if r in _question or r in _answer}
    category_l = {c for c in EQUIPMENT_KEYWORDS["CATEGORY"] if c in _question or c in _answer}
    category_s = {cs for cs in (cl for cl in EQUIPMENT_KEYWORDS["CATEGORY"]) if cs in _question or cs in _answer}
    label2name = {"Equipment": equipments, "COUNTRY": countries, "MANUFACTURER": manufacturers, "RESEARCH": researches,
                  "CATEGORY": category_s | category_l}

    related_nodes = reduce(lambda a, b: a + [GRAPH.find_node([b], c) for c in label2name[b]], label2name, [])
    kids = {n.properties["kid"] for n in related_nodes}
    related_edges = [r for r in GRAPH.knowledge_relationships if r.start_node in kids and r.end_node in kids]

    return _answer, related_nodes, related_edges


def answer(question: str) -> str:
    response = requests.post(BASE_URL, json=payload(question), headers=HEADERS)
    try:
        return json.loads(response.text)["choices"][0]["message"]["content"]
    except Exception:
        return ""
