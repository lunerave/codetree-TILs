from collections import deque

n, m = map(int, input().split())

dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]

board = []

basecamp = []
stop_by = []
visited_camp = []
visited_stop_by = []

for i in range(n):
    line = list(map(int, input().split()))
    board.append(line)
    for j in range(n):
        if line[j] == 1:
            basecamp.append((i, j))

for _ in range(m):
    x, y = map(int, input().split())
    x -= 1
    y -= 1

    board[x][y] = -1
    stop_by.append((x, y))

t = 0
in_stop_by = 0

def find_basecamp(sx, sy):
    visited = [[0]*n for _ in range(n)]
    visited[sx][sy] = 1
    q= deque()
    q.append((sx, sy))

    while q:
        x, y = q.popleft()

        if (x, y) in basecamp:
            return x, y

        for d in range(4):
            nx = x + dx[d]
            ny = y + dy[d]

            if 0 <= nx < n and 0 <= ny < n and visited[nx][ny] == 0:
                if (nx, ny) in visited_camp:
                    continue
                
                if (nx, ny) in visited_stop_by:
                    continue
                visited[nx][ny] = 1
                q.append((nx, ny))
            
moving_people = deque()


def to_stop_by(sx, sy, tx, ty):
    visited = [[0]*n for _ in range(n)]
    visited[sx][sy] = 1
    q= deque()
    q.append((sx, sy, -1, -1))

    while q:
        x, y, nsx, nsy = q.popleft()

        if x == tx and y == ty:
            return nsx, nsy

        for d in range(4):
            nx = x + dx[d]
            ny = y + dy[d]

            if 0 <= nx < n and 0 <= ny < n and visited[nx][ny] == 0:
                if (nx, ny) in visited_camp:
                    continue
                
                if (nx, ny) in visited_stop_by:
                    continue
                
                if nsx == -1 and nsy == -1:
                    nnsx, nnsy = nx, ny
                else:
                    nnsx, nnsy = nsx, nsy

                visited[nx][ny] = 1
                q.append((nx, ny, nnsx, nnsy))
            
    

while True:
    if in_stop_by == m:
        break
    t += 1

    if moving_people:
        for _ in range(len(moving_people)):
            sx, sy, tx, ty = moving_people.popleft()
            nsx, nsy = to_stop_by(sx, sy, tx, ty)
            if nsx == tx and nsy == ty:
                visited_stop_by.append((nsx, nsy))
                in_stop_by += 1
            else:
                moving_people.append((nsx, nsy, tx, ty))

    if t <= m:
        bx, by = find_basecamp(stop_by[t-1][0], stop_by[t-1][1])
        moving_people.append((bx, by, stop_by[t-1][0], stop_by[t-1][1]))
        visited_camp.append((bx, by))

print(t)