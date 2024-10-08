from collections import deque
import copy
dx = [-1, 1, 0, 0]
dy = [0, 0, 1, -1]

k, m = map(int, input().split())

maps = []

for _ in range(5):
    maps.append(list(map(int, input().split())))

saved_pieces = deque(list(map(int, input().split())))

def rotate90(sx, sy, length):
    sx -= 1
    sy -= 1
    
    temp_maps = copy.deepcopy(maps)

    for x in range(sx, sx + length):
        for y in range(sy, sy + length):
            ox, oy = x - sx, y - sy
            temp_maps[sx+oy][sy+length-ox-1] = maps[x][y]
    
    return temp_maps

def oprotate90(sx, sy, length):
    sx -= 1
    sy -= 1

    temp_maps = copy.deepcopy(maps)

    for x in range(sx, sx + length):
        for y in range(sy, sy + length):
            ox = x - sx
            oy = y - sy
            temp_maps[length - oy - 1 + sx][ox + sy] = maps[x][y]
    
    return temp_maps

def rotate180(sx, sy, length):
    sx -= 1
    sy -= 1

    temp_maps = copy.deepcopy(maps)

    for x in range(sx, sx + length):
        for y in range(sy, sy + length):
            ox = x - sx
            oy = y - sy

            temp_maps[length-ox-1+sx][length-oy-1+sy] = maps[x][y]
    
    return temp_maps

def bfs(rotated):
    temp = 0
    visited = [[0]*5 for _ in range(5)]
    for i in range(5):
        for j in range(5):
            if rotated[i][j] > 0 and visited[i][j] == 0:
                num = rotated[i][j]
                visited[i][j] = 1
                q = deque()
                q.append((i, j))
                count = 1

                while q:
                    x, y = q.popleft()

                    for d in range(4):
                        nx = x + dx[d]
                        ny = y + dy[d]

                        if 0 <= nx < 5 and 0 <= ny < 5 and visited[nx][ny] == 0 and rotated[nx][ny] == num:
                            visited[nx][ny] = 1
                            count += 1
                            q.append((nx, ny))
                
                if count >= 3:
                    temp += count
    return temp

def bfs_and_break():
    global rotated
    temp = 0
    lst = []
    visited = [[0]*5 for _ in range(5)]
    for i in range(5):
        for j in range(5):
            if rotated[i][j] > 0 and visited[i][j] == 0:
                num = rotated[i][j]
                visited[i][j] = 1
                q = deque()
                q.append((i, j))
                count = 1
                save_index = [(i, j)]

                while q:
                    x, y = q.popleft()

                    for d in range(4):
                        nx = x + dx[d]
                        ny = y + dy[d]

                        if 0 <= nx < 5 and 0 <= ny < 5 and visited[nx][ny] == 0 and rotated[nx][ny] == num:
                            visited[nx][ny] = 1
                            count += 1
                            q.append((nx, ny))
                            save_index.append((nx, ny))
                
                if count >= 3:
                    temp += count
                    for tx, ty in save_index:
                        rotated[tx][ty] = 0
    return temp

answer_list = []
for _ in range(k):     
    answers = []

    for i in range(1, 4):
        for j in range(1, 4):
            rotated = rotate90(i, j, 3)
            rotated_result = bfs(rotated)
            answers.append([rotated_result, 90, i, j])

            rotated = rotate180(i, j, 3)
            rotated_result = bfs(rotated)
            answers.append([rotated_result, 180, i, j])
            
            rotated = oprotate90(i, j, 3)
            rotated_result = bfs(rotated)
            answers.append([rotated_result, 270, i, j])

    answers.sort(key=lambda x: (-x[0], x[1], x[3], x[2]))

    answer = 0
    index = answers[0][2], answers[0][3]
    angle = answers[0][1]
    flag = 0

    if angle == 90:
        rotated = rotate90(index[0], index[1], 3)
        answer += bfs_and_break()
        while True:
            for i in range(5):
                for j in range(4, -1, -1):
                    if saved_pieces and rotated[j][i] == 0:
                        rotated[j][i] = saved_pieces.popleft()
                    if not saved_pieces:
                        flag = 1
            
            temp = bfs_and_break()
            answer += temp
            if temp == 0 or flag == 1:
                break
    elif angle == 180:
        rotated = rotate180(index[0], index[1], 3)
        answer += bfs_and_break()
        while True:
            for i in range(5):
                for j in range(4, -1, -1):
                    if saved_pieces and rotated[j][i] == 0:
                        rotated[j][i] = saved_pieces.popleft()
                    if not saved_pieces:
                        flag = 1
            
            temp = bfs_and_break()
            answer += temp
            if temp == 0 or flag == 1:
                break
    elif angle == 270:
        rotated = oprotate90(index[0], index[1], 3)
        answer += bfs_and_break()
        while True:
            for i in range(5):
                for j in range(4, -1, -1):
                    if saved_pieces and rotated[j][i] == 0:
                        rotated[j][i] = saved_pieces.popleft()
                    if not saved_pieces:
                        flag = 1
            
            temp = bfs_and_break()
            answer += temp
            if temp == 0 or flag == 1:
                break
    
    maps = copy.deepcopy(rotated)

    if(answer != 0):
        answer_list.append(answer)

print(*answer_list)