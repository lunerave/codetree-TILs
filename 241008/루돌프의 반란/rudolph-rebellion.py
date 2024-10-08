def cal_dist(r1, c1, r2, c2):
    return abs(r1 - r2) ** 2 + abs(c1 - c2) ** 2


def in_range(x, y):
    return 0 <= x < n and 0 <= y < n

dx=[-1,-1,0,1,1, 1, 0,-1]
dy=[0 ,1 ,1,1,0,-1,-1,-1]
def roodolf_move(rounds):
    # 가장가까운 산타를 향해 1칸 돌진.
    # 산타가 둘이상이면 r좌표큰, 동일하면 c좌표큰
    # 상하좌우,대각선 포함해서 8방향.
    global rr,rc
    min_dist = 100000
    mr,mc = 10000,10000
    mnum= -1
    #산타 값 전부조회
    for num in range(1,p+1):
        sr,sc = s_where[num]
        if sr == -100 : continue
        dist = cal_dist(sr,sc,rr,rc)
        if (min_dist,-mr,-mc) >= (dist,-sr,-sc) : # 여기서 오류나면 그냥 for문으로 2차원배열 탐색으로 하기
            min_dist = dist 
            mr,mc = sr,sc
            mnum = num
    #print(mr,mc,mnum)

    r_dist = cal_dist(mr,mc,rr,rc)

    for dnum in range(8):
        nx,ny = rr+dx[dnum],rc+dy[dnum]
        n_dist = cal_dist(mr,mc,nx,ny)
        if in_range(nx,ny) and r_dist > n_dist :
            r_dist = n_dist
            nr,nc = nx,ny
            r_num = dnum

    #맵 갱신
    r_map[rr][rc] = 0
    r_map[nr][nc] = 1
    rr,rc = nr,nc
    # 박치기 충돌 구현해야함

    if s_map[rr][rc] != 0 :
        #누군가있다면
        santa = s_map[rr][rc]
        sx,sy = rr,rc
        #기절구현 주의
        break_santa[santa] = rounds + 2
        #점수구현
        s_point[santa] += c
        s_map[rr][rc] = 0
        #밀려나기 구현
        nnx,nny = sx+c*dx[r_num],sy+c*dy[r_num]
        if in_range(nnx,nny): # 밖으로 안 나갈때
            #만약에 밀려난곳에 산타가 있나 체크해야함
            s_where[santa] = nnx,nny
            mnumber = santa
            while True :
                if no_santa(nnx,nny) : break
                nnx,nny,mnumber = push(nnx,nny,mnumber,r_num)
            # 빠져나오고난다음 mnx,mny 에 자리 넣어줘야함.
            if in_range(nnx,nny): # 안쪽이면 반영해주기
                s_map[nnx][nny] = mnumber
                s_where[mnumber] = nnx,nny
            else : #밀려서 밖으로 나가면 우주로 ㅂㅂ
                s_where[mnumber] = -100,-100
        else :
            s_map[sx][sy] = 0
            s_where[santa] = -100, -100
            return

    return

def one_san_move(santa,rounds):
    if not break_santa[santa] <= rounds : return
    sx,sy = s_where[santa]
    if sx == -100 : return
    #루돌프에게 가까워지는 방향으로 1칸
    # 다른산타, 게임판밖 x
    # 움직못하면 그냥 가만히
    # 가까워지지 못하면 그냥 가만히
    s_dist = cal_dist(sx,sy,rr,rc)
    mx,my = sx,sy
    for num in range(0,8,2):
        nx,ny = sx+dx[num],sy+dy[num]
        n_dist = cal_dist(nx,ny,rr,rc)
        if in_range(nx,ny) and s_map[nx][ny] == 0 and  s_dist > n_dist : #상우하좌
            s_dist = n_dist
            mx,my = nx,ny
            mnum = num

    # 갱신 및 그림 업데이트
    s_map[sx][sy] = 0
    s_where[santa] = mx,my
    s_map[mx][my] = santa
    # 루돌프와 부딫힘 체크
    if rr == mx and rc == my: #밀려나야함
        # 점수얻기
        # d 거리만큼 튕겨나가기
        s_map[mx][my] = 0
        r_num = (mnum+4)%8
        #기절처리 주의
        break_santa[santa] = rounds + 2
        #포인트 처리
        s_point[santa] += d
        mnx,mny = mx+d*dx[r_num],my+d*dy[r_num]
        if in_range(mnx,mny): # 밖으로 나갈때
            #만약에 밀려난곳에 산타가 있나 체크해야함
            s_where[santa] = mnx,mny
            mnumber = santa
            while True :
                if no_santa(mnx,mny) : break
                mnx,mny,mnumber = push(mnx,mny,mnumber,r_num)
            # 빠져나오고난다음 mnx,mny 에 자리 넣어줘야함.
            if in_range(mnx,mny): # 안쪽이면 반영해주기
                #print(mnx,mny,mnumber)
                s_map[mnx][mny] = mnumber
                s_where[mnumber] = mnx,mny
            else : #밀려서 밖으로 나가면 우주로 ㅂㅂ
                s_where[mnumber] = -100,-100
        else :
            s_map[mx][my] = 0
            s_where[santa] = -100, -100
            return

    return

def push(x,y,num,r_num):

    mnumber = s_map[x][y]
    s_where[num] = x,y
    s_map[x][y] = num
    mx,my = x+dx[r_num],y+dy[r_num]
    return mx,my,mnumber


def no_santa(mnx,mny):
    if not in_range(mnx,mny) : return True
    if s_map[mnx][mny] == 0 :
        return True
    return False

def santa_move(rounds):

    for santa in range(1,p+1):
        one_san_move(santa,rounds)
    return


n,m,p,c,d = map(int,input().split())
s_point = [0 for _ in range((1+p))]
s_where = [(-1,-1) for _ in range((1+p))]
rr,rc = map(int,input().split())
rr-=1
rc-=1
r_map = [ [ 0 for _ in range(n)] for _ in range(n)]
s_map = [ [ 0 for _ in range(n)] for _ in range(n)]
r_map[rr][rc] = 1
break_santa = [0 for _ in range((1+p))]
for pn in range(p):
    snum,sr,sc = map(int,input().split())
    s_where[snum] = (sr-1,sc-1)
    s_map[sr-1][sc-1] = snum

def look_maps():
    print('산타')
    for k in s_map:
        print(*k)
    print('루돌')
    for k1 in r_map:
        print(*k1)
    return

def output_santa_point():
    for num in range(1,p+1):
        print(s_point[num],end=' ')
    return


def santa_dead_check():
    count = 0
    for santa in range(1,p+1):
        sx,sy = s_where[santa]
        if sx == -100 :
            count += 1

    return count == p
def santa_point_up():

    for num in range(1,p+1):
        sx,sy = s_where[num]
        if sx == -100 : continue
        s_point[num] += 1
    return
for rounds in range(m):
    roodolf_move(rounds)
    #look_maps()
    if santa_dead_check(): break
    santa_move(rounds)
    #look_maps()
    if santa_dead_check(): break
    santa_point_up()

output_santa_point()