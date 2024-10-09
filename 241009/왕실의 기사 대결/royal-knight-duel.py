from collections import deque

l, n, q = map(int, input().split())

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

traps_and_walls = []

traps = set()
walls = set()

nights = [[0]*l for _ in range(l)]

nights_health = dict()

answer = 0

origin_hp = [0] * (n+1)


for i in range(l):
    line = list(map(int, input().split()))
    traps_and_walls.append(line)
    for j in range(l):
        if line[j] == 1:
            traps.add((i, j))
        if line[j] == 2:
            walls.add((i, j))

for i in range(1, n+1):
    x, y, h, w, hp = map(int, input().split())
    nights_health[i] = hp
    origin_hp[i] = hp
    x -= 1
    y -= 1
    for nx in range(x, x+h):
        for ny in range(y, y+w):
            nights[nx][ny] = i


def bfs(sx, sy):
    temp = []
    temp.append((sx, sy))
    q = deque()
    q.append((sx, sy))
    visited = [[0]*l for _ in range(l)]
    visited[sx][sy] = 1

    while q:
        x, y = q.popleft()

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            if 0 <= nx < l and 0 <= ny < l and visited[nx][ny] == 0 and nights[nx][ny] == nights[x][y]:
                temp.append((nx, ny))
                visited[nx][ny] = 1
                q.append((nx, ny))
    
    return temp

def walls_check(x, y):
    if traps_and_walls[x][y] == 2:
        return False
    
    return True


def move_possible(bodies, direction):
    global save

    for x, y in bodies:
        nx = x + dx[direction]
        ny = y + dy[direction]

        if 0 <= nx < l and 0 <= ny < l:
            if nights[nx][ny] == 0 or nights[nx][ny] == nights[x][y]:
                if not walls_check(nx, ny):
                    return False
            else:
                if nights[nx][ny] in save:
                    continue
                save.append((nights[nx][ny]))    
                next_bodies = bfs(nx, ny)
                res = move_possible(next_bodies, direction)
                if not res:
                    return False
        else:
            return False
    
    return True

def remove_night(night):
    for i in range(l):
        for j in range(l):
            if nights[i][j] == night:
                bodies = bfs(i, j)
    
    for x, y in bodies:
        nights[x][y] = 0


        
for _ in range(q):
    night_num, direction = map(int, input().split())

    origin_bodies = []

    for i in range(l):
        for j in range(l):
            if nights[i][j] == night_num:
                origin_bodies = bfs(i, j)
                break
        if origin_bodies:
            break

    if not origin_bodies:
        continue
    
    save = []

    res = move_possible(origin_bodies, direction)
    
    if not res:
        continue

    for s in save:
        bodies = []
        for i in range(l):
            for j in range(l):
                if nights[i][j] == s:
                    bodies = bfs(i, j)
                    break
            if bodies:
                break
        
        for x, y in bodies:
            nights[x][y] = 0

        for x, y in bodies:
            nx = x + dx[direction]
            ny = y + dy[direction]

            nights[nx][ny] = s
            if traps_and_walls[nx][ny] == 1:
                nights_health[s] -= 1
        if nights_health[s] <= 0:
            remove_night(s)

    for x, y in origin_bodies:
        nights[x][y] = 0

    for x, y in origin_bodies:
        nx = x + dx[direction]
        ny = y + dy[direction]

        nights[nx][ny] = night_num


for i in range(1, n+1):
    if nights_health[i] > 0:
        answer += origin_hp[i] -nights_health[i]

print(answer)