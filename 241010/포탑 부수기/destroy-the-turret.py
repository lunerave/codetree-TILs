from collections import defaultdict, deque

dx = [0, 1, 0, -1, -1, 1, -1, 1]
dy = [1, 0, -1, 0, -1, 1, 1, -1]

n, m, k = map(int, input().split())

towers = []

attacked = defaultdict(int)

for _ in range(n):
    towers.append(list(map(int, input().split())))

def laser(sx, sy, tx, ty):
    q = deque()
    q.append((sx, sy, []))

    visited = [[0]*m for _ in range(n)]

    visited[sx][sy] = 1

    while q:
        x, y, route = q.popleft()

        if x == tx and y == ty:
            return route

        for d in range(4):
            nx = x + dx[d]
            ny = y + dy[d]

            if nx < 0:
                nx = n-1
            if ny < 0:
                ny = m-1
            if nx == n:
                nx = 0
            if ny == m:
                ny = 0
            
            if visited[nx][ny] == 0 and towers[nx][ny] != 0:
                nroute = route[:]
                nroute.append((nx, ny))
                visited[nx][ny] = 1
                q.append((nx, ny, nroute))
    
    return []


for turn in range(k):

    min_tower = 2**31
    max_tower = -1
    
    for i in range(n):
        for j in range(n):
            if towers[i][j] <= 0:
                continue

            if min_tower > towers[i][j]:
                min_tower = towers[i][j]
                min_towers = []
                min_towers.append((i, j, i+j, attacked[(i, j)]))
            elif min_tower == towers[i][j]:
                min_towers.append((i, j, i+j, attacked[(i, j)]))
            elif max_tower < towers[i][j]:
                max_tower = towers[i][j]
                max_towers = []
                max_towers.append((i, j, i+j, attacked[(i, j)]))
            elif max_tower == towers[i][j]:
                max_towers.append((i, j, i+j, attacked[(i, j)]))
    
    min_towers.sort(key = lambda x:[-x[3], -x[2], -x[1]])
    max_towers.sort(key = lambda x: [x[3], x[2], x[1]])
    
    min_x, min_y = min_towers[0][0], min_towers[0][1]
    max_x, max_y = max_towers[0][0], max_towers[0][1]

    towers[min_x][min_y] += n+m

    target_dmg = towers[min_x][min_y]
    route_dmg = target_dmg // 2

    attacked[(min_x, min_y)] = turn
    
    res = laser(min_x, min_y, max_x, max_y)
    
    if res:
        for i in range(len(res)):
            tx, ty = res[i]
            if i == len(res)-1:
                towers[tx][ty] -= target_dmg
            else:
                towers[tx][ty] -= route_dmg
    else:
        towers[max_x][max_y] -= target_dmg
        for d in range(8):
            nx = max_x + dx[d]
            ny = max_y + dy[d]

            if nx < 0:
                nx = n-1
            if ny < 0:
                ny = m-1
            if nx == n:
                nx = 0
            if ny == m:
                ny = 0
            
            towers[nx][ny] = max(0, towers[nx][ny] - route_dmg)
    
    for i in range(n):
        for j in range(m):
            if (i, j) not in res and towers[i][j] != 0:
                towers[i][j] += 1

answer = 0

for i in range(n):
    for j in range(m):
        if towers[i][j] > answer:
            answer = towers[i][j]

print(answer)