import heapq

Q = int(input())

def dijk(start, n, dest): 
    distance = [2**31]*n 

    # distance[start] = 0

    q = []

    heapq.heappush(q, (0, start))

    while q:
        c, node = heapq.heappop(q)

        for nnode, w in nodes[node]:
            if c + w < distance[nnode]:
                distance[nnode] = c + w
                heapq.heappush(q, (c+w, nnode)) 
    
    return distance[dest]

heap = []
start = 0


for _ in range(Q):
    command = list(map(int, input().split()))

    if command[0] == 100:
        n, m = command[1], command[2]
        nodes = [[] for _ in range(n)]

        for i in range(3, len(command), 3):
            s = command[i]
            e = command[i+1]
            w = command[i+2]
            nodes[s].append((e, w))
            if s != e:
                nodes[e].append((s, w))
    
    if command[0] == 200:
        id, least, dest = command[1], command[2], command[3]

        # if start == dest:
        #     for d, w in nodes[start]:
        #         if d == start:
        #             heapq.heappush(heap, [-(least-w), id, least, dest])
        # else:
        heapq.heappush(heap, [-(least-dijk(start, n, dest)), id, least, dest])
    
    if command[0] == 300:
        target = command[1]
        for idx, h in enumerate(heap):
            if h[1] == target:
                heap.remove(heap[idx])
    
    if command[0] == 400:
        if heap:
            info = heap[0]
            value = -info[0]
            id = info[1]
            if value < 0:
                print(-1)
            else:
                print(id)
                heapq.heappop(heap)
        else:
            print(-1)
    if command[0] == 500:
        new_start = command[1]
        temp = []
        while heap:
            info = heapq.heappop(heap)
            id, least, dest = info[1], info[2], info[3]
            temp.append([-(least-dijk(new_start, n, dest)), id, least, dest])
        start = new_start
        heap = []
        for t in temp:
            heapq.heappush(heap, t)