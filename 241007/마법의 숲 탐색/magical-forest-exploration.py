from collections import deque

r, c, k = map(int, input().split())

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

answer = 0

maps = [[0]*c for _ in range(r)]

visited_num = 1

def getExit(x, y, d):
    if d == 0:
        return [x-1, y]
    elif d == 1:
        return [x, y+1]
    elif d == 2:
        return [x+1, y]
    else:
        return [x, y-1]

def in_board(x, y):
    if 0 <= x < r and 0 <= y < c:
        return True
    else:
        return False

def check(x, y):
    if not in_board(x, y):
        if x < r and 0 <= y < c:
            return True
    else:
        if maps[x][y] == 0:
            return True

    return False



def move(sy, sd, visited_num):
    global maps

    x, y = -2, sy

    while True:
        if check(x+2, y) and check(x+1, y+1) and check(x+1, y-1):
            x += 1
        elif check(x+1, y-1) and check(x-1, y-1) and check(x, y-2) and check(x+1, y-2) and check(x+2, y-1):
            x += 1
            y -= 1
            sd = (sd-1)%4
        elif check(x+1, y+1) and check(x-1, y+1) and check(x, y+2) and check(x+1, y+2) and check(x+2, y+1):
            x += 1
            y += 1
            sd = (sd+1)%4
        else:
            break
    
    if not in_board(x, y) or not in_board(x+1, y) or not in_board(x-1, y) or not in_board(x, y-1) or not in_board(x, y+1):
        return [False, -1, -1]
    else:
        maps[x][y] = maps[x+1][y] = maps[x-1][y] = maps[x][y-1] = maps[x][y+1] = visited_num
        ex, ey = getExit(x, y, sd)
        maps[ex][ey] = -visited_num
        return [True, x, y]

def bfs(sx, sy, visited_num):
    visited = [[0]*c for _ in range(r)]

    golem = -1

    visited[sx][sy] = 1

    q = deque()

    q.append((sx, sy))

    while q:
        x, y = q.popleft()

        for d in range(4):
            nx = x + dx[d]
            ny = y + dy[d]

            if in_board(nx, ny) and visited[nx][ny] == 0 and maps[nx][ny] != 0:
                if abs(maps[x][y]) == abs(maps[nx][ny]) or (maps[x][y] < 0):
                    q.append((nx, ny))
                    visited[nx][ny] = 1
                    golem = max(golem, nx)
    
    return golem+1


for _ in range(k):
    sy, sd = map(int, input().split())
    sy -= 1

    info = move(sy, sd, visited_num)
    is_in, x, y = info

    if is_in:
        answer += bfs(x, y, visited_num)
    else:
        maps = [[0]*c for _ in range(r)]

    visited_num += 1

print(answer)