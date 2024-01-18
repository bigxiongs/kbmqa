import json
from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher

from database.session import execute
# 初始化设置
data_path = 'military.json'
# 打开数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "00000000"))
graph.run('match (n) detach delete n')

initialize_database = execute("MATCH (n) DETACH DELETE n")


# util
# 建立一个节点
def create_node(graph, label, attrs):
    n = "_.name=" + "\"" + attrs["name"] + "\""

    matcher = NodeMatcher(graph)
    # 查询是否已经存在，若存在则返回节点，否则返回None
    value = matcher.match(label).where(n).first()
    # 如果要创建的节点不存在则创建
    if value is None:
        node = Node(*label, **attrs)
        n = graph.create(node)
        return n
    return None


# label1 = ("Stock","kk")
# attrs1 = {"name": "招商银行", "code": "600036"}
# create_node(graph, label1, attrs1)

# 建立两个节点之间的关系
def create_relationship(graph, label1, attrs1, label2, attrs2, r_name):
    value1 = match_node(graph, label1, attrs1)
    value2 = match_node(graph, label2, attrs2)
    if value1 is None or value2 is None:
        return False
    r = Relationship(value1, r_name, value2)
    graph.create(r)


# 查询节点
def match_node(graph, label, attrs):
    n = "_.name=" + "\"" + attrs["name"] + "\""
    matcher = NodeMatcher(graph)
    return matcher.match(label).where(n).first()

# r = "证券交易所"
# create_relationship(graph, label1, attrs1, label2, attrs2, r)

"""创建国家、生产研发单位节点"""

## 生成国家、生产研发单位列表
country_label = []
manufacturer_label = []

for data in open(data_path, encoding='utf-8'):
    data_json = json.loads(data)
    # print(type(data_json))
    # print(data_json)

    node_properties = {}
    for i in data_json.items():
        # 加载所有国家
        if i[0] == '产国':
            if i[1] not in country_label:
                country_label.append(i[1])

        # 加载所有厂商
        if i[0] == '制造厂' or i[0] == '生产单位' or i[0] == '研发单位' or i[0] == '研发厂商' or i[0] == '制造商':
            if i[1] not in manufacturer_label:
                manufacturer_label.append(i[1])

# print(country_label)
# print(manufacturer_label)

## 生成国家、生产研发单位实体数据
country_node = []
manufacturer_node = []

for i in country_label:
    country_node.append([['国家'],i])
# print(country_node)

for i in manufacturer_label:
    manufacturer_node.append([['生产研发厂商'],i])
# print(manufacturer_node)
# print(len(manufacturer_node))

## 创建国家、生产研发单位节点
for i in country_node:
    create_node(graph, tuple(i[0]), {"name": i[1]})
    # break

for i in manufacturer_node:
    create_node(graph, tuple(i[0]), {"name": i[1]})
    # print(tuple(i[0]), {"name": i[1]}, i[0])
    # break

print('创建国家、生产研发单位节点完成！')

# import json
# data_path = r'C:\Users\Administrator.DESKTOP-O4V8L0N\Desktop\事务\毕业设计\代码\test\military.json'
big = ['飞行器', '舰船舰艇', '枪械与单兵', '坦克装甲车辆', '火炮', '导弹武器', '太空装备', '爆炸物']
small = ['战斗机', '攻击机', '轰炸机', '教练机', '预警机', '侦察机', '反潜机', '电子战机', '无人机', '运输机', '飞艇',
         '试验机', '加油机', '通用飞机', '干线', '支线', '运输直升机', '武装直升机', '多用途直升机', '航空母舰',
         '战列舰', '巡洋舰', '驱逐舰', '护卫舰', '两栖作战舰艇', '核潜艇', '常规潜艇', '水雷战舰艇', '导弹艇',
         '巡逻舰/艇', '保障辅助舰艇', '气垫艇/气垫船', '其他', '非自动步枪', '自动步枪', '冲锋枪', '狙击枪', '手枪',
         '机枪', '霰弹枪', '火箭筒', '榴弹发射器', '附件', '刀具', '迷彩服', '步兵战车', '主战坦克', '特种坦克',
         '装甲运兵车', '装甲侦察车', '装甲指挥车', '救护车', '工程抢修车', '布/扫雷车', '越野车', '其他特种装甲车辆',
         '榴弹炮', '加农炮', '加农榴弹炮', '迫击炮', '火箭炮', '高射炮', '坦克炮', '反坦克炮', '无后坐炮', '装甲车载炮',
         '舰炮', '航空炮', '自行火炮', '弹炮结合系统', '反弹道导弹', '地地导弹', '舰地（潜地）导弹', '地空导弹',
         '舰空导弹', '空空导弹', '空地导弹', '潜舰导弹', '空舰导弹', '岸舰导弹', '舰舰导弹', '航天机构', '运载火箭',
         '航天基地', '技术试验卫星', '军事卫星', '科学卫星', '应用卫星', '空间探测器', '航天飞机', '宇宙飞船', '地雷',
         '水雷', '手榴弹', '炸弹', '鱼雷', '火箭弹', '原子弹', '氢弹', '中子弹']
combine = big + small

## 生成武装装备实体
arms = []
arms_node = []
for data in open(data_path, encoding='utf-8'):
    data_json = json.loads(data)
    # print(data_json)
    node_properties = {}
    for i in data_json.items():
        # 加载所有武器实体（label：大类 小类）
        node_properties[i[0]] = i[1]

    # 对不规则名称进行处理
    puncation = '＂＃＄％＆＇（）＊＋，／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿‘’‛“”„‟…‧﹏﹑﹔·！？｡。!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'
    for i in puncation:
        node_properties['名称'] = node_properties['名称'].replace(i, "")

    # print(node_properties['_id']['$oid'])
    # break

    node_properties['_id'] = node_properties['_id']['oid']

    node_properties['name'] = node_properties['名称']
    # for j in combine:
    #     if node_properties['类型'] == j:
    #         label = j
    # node_properties['label'] = label
    arms.append(node_properties)
    # print(arms)
    # break
# print(arms)

# ## 创建武器装备实体
for i in arms:
    try:
        create_node(graph, (i['大类'], i['类型']), i)
    except Exception as e:
        continue
    # print(i['大类'])
    # break
print('创建武器装备实体完成！')

pro_list = []
for i in arms:
    for key, item in i.items():
        if key not in pro_list:
            pro_list.append(key)
# pro_list.remove('_id').remove('name')
print(len(pro_list))
print(pro_list)

manufacturer_type = ['制造厂', '生产单位', '研发单位', '研发厂商', '制造商']
count = 0
for data in arms:
    # data_json = json.loads(data)
    # print(data_json)
    # create_relationship(graph, 'manufacturer', {"name": data['研发单位']}, 'country', {"name": data['产国']}, '属于')
    for key, value in data.items():
        if key in manufacturer_type:
            create_relationship(graph, '生产研发厂商', {"name": data[key]}, '国家', {"name": data['产国']}, '属于')
            create_relationship(graph, '生产研发厂商', {"name": data[key]}, data['类型'], {"name": data['名称']}, '生产研发')
            create_relationship(graph, data['类型'], {"name": data['名称']}, '国家', {"name": data['产国']}, '产国')
    # break
    # count += 1
    # if count == 10:
    #     break
print('创建关系完成')