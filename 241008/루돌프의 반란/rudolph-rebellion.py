n, m, p, c, d = map(int, input().split())

maps = [[0]*n for _ in range(n)]

rudolfx, rudolfy = map(int, input().split())

rudolfx -= 1
rudolfy -= 1

maps[rudolfx][rudolfy] = -1

santa = [[] for _ in range(31)]
santas = []
santa_out = []
santa_stunned = {}

dx = [-1, 0, 1, 0, -1, -1, 1, 1]
dy = [0, 1, 0, -1, -1, 1, 1, -1]

for _ in range(p):
    santa_num, x, y = map(int, input().split())
    maps[x-1][y-1] = santa_num
    santas.append([santa_num, x-1, y-1, 0])

santas.sort(key = lambda x:x[0])

def move_to_close_santa(sx, sy, tx, ty):
    if sx == tx:
        return (sx, sy+1, 1) if sy < ty else (sx, sy-1, 3)
    elif sy == ty:
        return (sx+1, sy, 2) if sx < tx else (sx-1, sy, 0)
    elif sx < tx and sy < ty:
        return (sx+1, sy+1, 6)
    elif sx < tx and sy > ty:
        return (sx+1, sy-1, 7)
    elif sx > tx and sy < ty:
        return (sx-1, sy+1, 5)
    elif sx < tx and sy > ty:
        return (sx-1, sy-1, 4)

def find_close_santa(x, y):
    res = []
    for santa in santas:
        if santa[0] in santa_out:
            continue
        temp_res = abs(santa[1]-x)**2 + abs(santa[2]-y)**2
        res.append([temp_res, santa[1], santa[2]])
    
    res.sort(key = lambda x: [x[0], -x[1], -x[2]])

    return res[0][1], res[0][2]

def santa_move(sx, sy, rx, ry):
    res = []
    for i in range(4):
        nx = sx + dx[i]
        ny = sy + dy[i]

        if 0 <= nx < n and 0 <= ny < n and (maps[nx][ny] == 0 or maps[nx][ny] == -1):
            if maps[nx][ny] == 0:
                res.append([(abs(nx-rx)**2 + abs(ny-ry)**2), d, nx, ny])
            else:
                return nx, ny, i
    if not res:
        return sx, sy
    
    res.sort(key=lambda x: [x[0], x[1]])

    return res[0][2], res[0][3]

for a in range(m):
    santa_x, santa_y = find_close_santa(rudolfx, rudolfy)
    # 루돌프 산타로 이동
    maps[rudolfx][rudolfy] = 0
    rudolf = move_to_close_santa(rudolfx, rudolfy, santa_x, santa_y)
    rudolfx = rudolf[0]
    rudolfy = rudolf[1]

    if maps[rudolfx][rudolfy] > 0:
        santa_stunned[maps[rudolfx][rudolfy]] = a + 1
        for s in range(p):
            if santas[s][0] == maps[rudolfx][rudolfy]:
                santas[s][3] += c
        direct = rudolf[2]
        nsx = rudolfx + dx[direct]*c
        nsy = rudolfy + dy[direct]*c
        if 0 <= nsx < n and 0 <= nsy < n:
            if maps[nsx][nsy] == 0:
                maps[nsx][nsy] = maps[rudolfx][rudolfy]
                for s in range(p):
                    if santas[s][0] == maps[nsx][nsy]:
                        santas[s][1] = nsx
                        santas[s][2] = nsy
                        break
                maps[rudolfx][rudolfy] = -1
            else:
                temp_x, temp_y = nsx + dx[direct], nsy + dy[direct]
                out_flag = 0
                while True:
                    if 0 <= temp_x < n and 0 <= temp_y < n: 
                        if maps[temp_x][temp_y] > 0:
                            temp_x += dx[direct]
                            temp_y += dy[direct]
                        else:
                            break
                    else:
                        out_flag = 1
                        break
                
                if out_flag == 1:
                    sad_santa = maps[temp_x - dx[direct]][temp_y - dy[direct]]
                    santa_out.append(sad_santa)
                
                while True:
                    next_x = temp_x - dx[direct]
                    next_y = temp_y - dy[direct]
                    for s in range(p):
                        if santas[s][0] == maps[next_x][next_y]:
                            santas[s][1] = temp_x
                            santas[s][2] = temp_y
                            break

                    maps[temp_x][temp_y] = maps[next_x][next_y]
                    temp_x = next_x
                    temp_y = next_y
                    if temp_x == nsx and temp_y == nsy:
                        maps[next_x][next_y] = maps[rudolfx][rudolfy]
                        for s in range(p):
                            if santas[s][0] == maps[next_x][next_y]:
                                santas[s][1] = next_x
                                santas[s][2] = next_y
                                break
                        break
        else:
            santa_out.append(maps[rudolfx][rudolfy])
            maps[rudolfx][rudolfy] = -1
    else:
        maps[rudolfx][rudolfy] = -1
            
    
    # 산타 이동
    for i in range(p):
        # 산타가 이동할 공간
        santa = santas[i]
        if santa[0] in santa_out:
            continue
        if santa[0] in santa_stunned:
            if santa_stunned[santa[0]] >= a:
                continue
            
        santa_loc = santa_move(santa[1], santa[2], rudolfx, rudolfy)
        nsx = santa_loc[0]
        nsy = santa_loc[1]
        # 같으면 이동할 공간이 없음
        if nsx == santa[1] and nsy == santa[2]:
            continue
        if len(santa_loc) == 3:
            santa_stunned[santa[0]] = a + 1
            direct = santa_loc[2]
            santas[i][3] += d
            maps[santa[1]][santa[2]] = 0
            nsx = nsx - dx[direct]*d
            nsy = nsy - dy[direct]*d
            if 0 <= nsx < n and 0 <= nsy < n:
                if maps[nsx][nsy] == 0:
                    maps[nsx][nsy] = santa[0]
                else: # 튕겨서 산타를 만났을 경우
                    temp_x, temp_y = nsx - dx[direct], nsy - dy[direct]
                    out_flag = 0
                    while True:
                        if 0 <= temp_x < n and 0 <= temp_y < n: 
                            if maps[temp_x][temp_y] > 0:
                                temp_x -= dx[direct]
                                temp_y -= dy[direct]
                            else:
                                break
                        else:
                            out_flag = 1
                            break
                    
                    if out_flag == 1:
                        sad_santa = maps[temp_x + dx[direct]][temp_y + dy[direct]]
                        santa_out.append(sad_santa)
                    
                    while True:
                        next_x = temp_x + dx[direct]
                        next_y = temp_y + dy[direct]
                        for s in range(p):
                            if santas[s][0] == maps[next_x][next_y]:
                                santas[s][1] = temp_x
                                santas[s][2] = temp_y
                                break

                        maps[temp_x][temp_y] = maps[next_x][next_y]
                        temp_x = next_x
                        temp_y = next_y
                        if temp_x == nsx and temp_y == nsy:
                            maps[next_x][next_y] = santa[0]
                            santas[i][1] = next_x
                            santas[i][2] = next_y
                            break
            else: # 튕겨서 마을 밖으로 나감
                santa_out.append(santa[0])
            continue

        maps[santa[1]][santa[2]] = 0
        maps[nsx][nsy] = santa[0]
        santas[i][1] = nsx
        santas[i][2] = nsy

    for s in range(p):
        if santas[s][0] not in santa_out:
            santas[s][3] += 1

answer = []

for santa in santas:
    answer.append(santa[3])

print(*answer)