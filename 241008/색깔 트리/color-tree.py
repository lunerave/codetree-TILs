from collections import defaultdict, deque
import sys
input = sys.stdin.readline
class Node:
    def __init__(self, m_id, p_id, color, max_depth):
        self.m_id = m_id
        self.p_id = p_id
        self.color = color
        self.max_depth = max_depth
        self.parent_node = None
        self.color_value_list = [False] * 5
        self.child_node_list = []

    def check_parent_node(self, p_id, depth_count=2):
        if p_id == -1:
            return True
        if id_node_check_list[p_id].max_depth < depth_count:
            return False
        else:
            next_node = id_node_check_list[p_id]
            return next_node.check_parent_node(next_node.p_id, depth_count + 1)
    
    def add_parent_node(self, p_id):
        if self.check_parent_node(p_id):
            self.p_id = p_id
            self.parent_node = id_node_check_list[p_id]
            self.parent_node.child_node_list.append(self)
            return True
            

    def reset_color_value_list(self):
        self.color_value_list = [False] * 5


def dfs_color_update(node):
    """DFS로 서브트리 내의 색상 정보를 갱신"""
    node.color_value_list = [False] * 5
    node.color_value_list[node.color - 1] = True

    for child in node.child_node_list:
        child_colors = dfs_color_update(child)
        for i in range(5):
            if child_colors[i]:
                node.color_value_list[i] = True
    
    return node.color_value_list


def calculate_score():
    """서브트리 내의 색상을 계산하고 점수를 구하는 함수"""
    total_sum = 0
    
    # 트리의 루트 노드들부터 시작해서 DFS로 색상 정보 갱신
    for node in id_node_check_list.values():
        if node.p_id == -1:  # 루트 노드에서만 시작
            dfs_color_update(node)

    # 각 노드별로 서브트리의 색상 수를 세고 점수를 계산
    for node in id_node_check_list.values():
        unique_colors = sum(node.color_value_list)
        total_sum += unique_colors * unique_colors
    
    print(total_sum)


n = int(input())
id_node_check_list = defaultdict(Node)

for _ in range(n):
    command, *args = map(int, input().split())
    
    if command == 100:
        m_id, p_id, color, max_depth = args
        node = Node(m_id, p_id, color, max_depth)
        
        if p_id == -1:
            id_node_check_list[m_id] = node
        else:
            if node.add_parent_node(p_id):
                id_node_check_list[m_id] = node
    
    elif command == 200:
        m_id, new_color = args
        node = id_node_check_list[m_id]
        q = deque([node])
        
        while q:
            current_node = q.popleft()
            current_node.color = new_color
            for child in current_node.child_node_list:
                q.append(child)
    
    elif command == 300:
        m_id = args[0]
        print(id_node_check_list[m_id].color)
    
    elif command == 400:
        calculate_score()