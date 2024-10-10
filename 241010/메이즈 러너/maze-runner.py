import copy

n, m, k = map(int, input().split())

dx = [-1, 1, 0, 0]
dy = [0, 0, 1, -1]

board = []

people_num = set()

for _ in range(n):
    board.append(list(map(int, input().split())))

for _ in range(m):
    x, y = map(int ,input().split())
    x -= 1
    y -= 1

    people_num.add((x, y))
    board[x][y] = -1

ex, ey = map(int, input().split())

ex -= 1
ey -= 1

board[ex][ey] = -2

def move(people, ex, ey):
    removed = []
    moved = []
    for x, y in people:
        distance = abs(ex-x) + abs(ey-y)
        for d in range(4):
            nx = x + dx[d]
            ny = y + dy[d]

            if 0 <= nx < n and 0 <= ny < n and not board[nx][ny] > 0:
                if (abs(ex-nx) + abs(ey-ny)) < distance:
                    removed.append((x, y))
                    moved.append((nx, ny))
                    break
    return removed, moved

def find_square():
    for length in range(2, n+1):
        for i in range(n-length+1):
            for j in range(n-length+1):
                last_x, last_y = i+length, j+length

                traveler = False

                if i <= ex < last_x and j <= ey < last_y:

                    for tx in range(i, last_x):
                        for ty in range(j, last_y):
                            if board[tx][ty] == -1:
                                traveler = True
                                break
                        
                        if traveler:
                            break
                
                if traveler:
                    return i, j, length
    
def rotate(x, y, length):

    temp_board = copy.deepcopy(board)

    for i in range(x, x+length):
        for j in range(y, y+length):
            ox = i - x
            oy = j - y

            temp_board[oy+x][length-ox+y-1] = board[i][j]
    
    for i in range(x, x+length):
        for j in range(y, y+length):
            board[i][j] = temp_board[i][j]

answer = 0

for k in range(k):

    is_people = 0

    people = []

    for i in range(n):
        for j in range(n):
            if board[i][j] == -1:
                people.append((i, j))
    
    removed, moved = move(people, ex, ey)

    answer += len(moved)

    for x, y in removed:
        board[x][y] = 0

    for x, y in moved:
        if board[x][y] == -2:
            continue
        else:
            board[x][y] = -1
    
    for i in range(n):
        for j in range(n):
            if board[i][j] == -1:
                is_people = 1
                break
        if is_people:
            break
    
    if not is_people:
        break

    tx, ty, length = find_square()

    rotate(tx, ty, length)

    for i in range(tx, tx+length):
        for j in range(ty, ty+length):
            if board[i][j] == -2:
                ex, ey = i, j
            if board[i][j] > 0:
                board[i][j] -= 1
    

print(answer)
print(ex+1, ey+1)