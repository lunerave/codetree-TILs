from collections import defaultdict
import heapq

Q = int(input())

def dijkstra(start):
    distance = defaultdict(lambda: 1e9)
    distance[start] = 0
    q = [(0, start)]  # (distance, node)

    while q:
        c, node = heapq.heappop(q)

        if c > distance[node]:
            continue  # 이미 최단 거리로 갱신된 경우

        for nnode, w in nodes[node]:
            if c + w < distance[nnode]:
                distance[nnode] = c + w
                heapq.heappush(q, (c + w, nnode))
    
    return distance

heap = []
start = 0
possible, impossible = [], []
possible_set, impossible_set = set(), set()
ban = set()

for _ in range(Q):
    command = list(map(int, input().split()))

    if command[0] == 100:
        n, m = command[1], command[2]
        nodes = [[] for _ in range(n)]

        for i in range(3, len(command), 3):
            s = command[i]
            e = command[i + 1]
            w = command[i + 2]
            nodes[s].append((e, w))
            if s != e:
                nodes[e].append((s, w))
    
        distances = dijkstra(start)

    if command[0] == 200:
        id, least, dest = command[1], command[2], command[3]
        
        # 만약 dest에 대한 거리 계산이 이미 존재한다면 캐시에서 사용
        distance = distances[dest]
        benefit = least - distance
        if benefit >= 0:
            heapq.heappush(possible, (-benefit, id, least, dest))
            possible_set.add(id)
        else:
            heapq.heappush(impossible, (-benefit, id, least, dest))
            impossible_set.add(id)

    if command[0] == 300:
        target = command[1]
        if target in possible_set or impossible_set:
            ban.add(target)
        impossible_set.discard(target)
        possible_set.discard(target)
        
    if command[0] == 400:
        temp = []
        while possible:
            profit, id, least, dest = heapq.heappop(possible)
            if id in ban:
                continue
            if id in possible_set:
                print(id)
                possible_set.discard(id)
                ban.add(id)
                break
            else:
                temp.append((profit, id, least, dest))
        else:
            print(-1)
        
        for t in temp:
            heapq.heappush(possible, t)

    if command[0] == 500:
        start = command[1]
        distances = dijkstra(start)
        temp = [] 
        temp_impossible = []
        possible_set, impossible_set = set(), set()
        for sales in (possible, impossible):
            for _, id, least, dest in sales:
                if id in ban:
                    continue
                profit = least - distances[dest]
                if profit >= 0:
                    heapq.heappush(temp, (-profit, id, least, dest))
                    possible_set.add(id)
                else:
                    temp_impossible.append((-profit, id, least, dest))
                    impossible_set.add(id)
        
        possible = temp
        impossible = temp_impossible