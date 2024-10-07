from collections import deque

n, q = map(int, input().split())

dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

bingbing = []

len_bingbing = 2**n

for _ in range(len_bingbing):
    bingbing.append(list(map(int, input().split())))

levels = list(map(int, input().split()))

def melt():
    global bingbing

    save_melted = []

    for i in range(len_bingbing):
        for j in range(len_bingbing):
            if bingbing[i][j] > 0:
                count = 0

                for d in range(4):
                    nx = i + dx[d]
                    ny = j + dy[d]

                    if 0 <= nx < len_bingbing and 0 <= ny < len_bingbing and bingbing[nx][ny] > 0:
                        count += 1
                
                if count < 3:
                    save_melted.append((i, j))
    
    for x, y in save_melted:
        bingbing[x][y] -= 1


def rotate():
    global bingbing



    for level in levels:
        if level == 0:
            melt()
            continue
        
        bing_size = 2**level
        bing_fraction_size = 2**(level-1)
        
        temp_maps = [[0]*(len_bingbing) for _ in range(len_bingbing)]

        for x in range(0, len_bingbing, bing_size):
            for y in range(0, len_bingbing, bing_size):
                if level == 1:
                    for i in range(bing_fraction_size+1):
                        for j in range(bing_fraction_size+1):
                            temp_maps[j+x][bing_fraction_size-i+y] = bingbing[i+x][j+y]
                else:
                    for i in range(0, bing_size, bing_fraction_size):
                        for j in range(0, bing_size, bing_fraction_size):
                            for q in range(bing_fraction_size):
                                for p in range(bing_fraction_size):
                                    temp_maps[j+x+q][bing_fraction_size-i+y+p] = bingbing[i+x+q][j+y+p]
        
        for i in range(len_bingbing):
            for j in range(len_bingbing):
                bingbing[i][j] = temp_maps[i][j]
        
        melt()

def cal_all_bing():
    results = 0

    for i in range(len_bingbing):
        for j in range(len_bingbing):
            results += bingbing[i][j]
    
    return results

def cal_big_bing():
    visited = [[0] * len_bingbing for _ in range(len_bingbing)]
    results = 0

    for i in range(len_bingbing):
        for j in range(len_bingbing):
            if bingbing[i][j] > 0 and visited[i][j] == 0:
                q = deque()
                q.append((i, j))
                big_ice = 1
                visited[i][j] = 1

                while q:
                    x, y = q.popleft()

                    for d in range(4):
                        nx = x + dx[d]
                        ny = y + dy[d]

                        if 0 <= nx < len_bingbing and 0 <= ny < len_bingbing and visited[nx][ny] == 0 and bingbing[nx][ny] > 0:
                            visited[nx][ny] = 1
                            big_ice += 1
                            q.append((nx, ny))
                
                results = max(results, big_ice)
    
    return results

rotate()

print(cal_all_bing())
print(cal_big_bing())