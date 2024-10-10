MAX_N = 100001
MAX_D = 21

a, p, val = [0] * MAX_N, [0] * MAX_N, [0] * MAX_N
noti = [False] * MAX_N
nx = [[0] * MAX_D for _ in range(MAX_N)]

n, q = map(int, input().split())

def init(info):
    global a, p, val, nx

    for i in range(1, n+1):
        p[i] = info[i]
    
    for i in range(1, n+1):
        a[i] = info[i+n]

        if a[i] > 20:
            a[i] = 20
    
    for i in range(1, n+1):
        now = i
        x = a[i]
        nx[now][x] += 1

        while p[now] and x:
            now = p[now]
            x -= 1
            if x:
                nx[now][x] += 1
            val[now] += 1

def toggle_noti(chat):
    now = p[chat]
    num = 1
    while now:
        for i in range(num, 21):
            val[now] += nx[chat][i] if noti[chat] else -nx[chat][i]
            if i > num:
                nx[now][i-num] += nx[chat][i] if noti[chat] else -nx[chat][i]
        
        if noti[now]:
            break
        
        now = p[now]
        num += 1
    noti[chat] = not noti[chat]

def change_power(chat, power):
    bef_power = a[chat]
    power = min(power, 20)
    a[chat] = power

    nx[chat][bef_power] -= 1
    if not noti[chat]:
        now = p[chat]
        num = 1

        while now:
            if bef_power >= num:
                val[now] -= 1
            if bef_power > num:
                nx[now][bef_power - num] -= 1
            if noti[now]:
                break
            
            now = p[now]
            num += 1
    
    nx[chat][power] += 1
    if not noti[chat]:
        now = p[chat]
        num = 1

        while now:
            if power >= num:
                val[now] += 1
            if power > num:
                nx[now][power - num] += 1
            if noti[now]:
                break
            
            now = p[now]
            num += 1

def change_parent(chat1, chat2):
    bef_noti1 = noti[chat1]
    bef_noti2 = noti[chat2]

    if not noti[chat1]:
        toggle_noti(chat1)
    if not noti[chat2]:
        toggle_noti(chat2)
    
    p[chat1], p[chat2] = p[chat2], p[chat1]

    if not bef_noti1:
        toggle_noti(chat1)
    if not bef_noti2:
        toggle_noti(chat2)

def print_res(chat):
    print(val[chat])



for _ in range(q):
    info = list(map(int, input().split()))

    command = info[0]

    if command == 100:
        init(info)
    elif command == 200:
        chat = info[1]
        toggle_noti(chat)
    elif command == 300:
        chat, power = info[1], info[2]
        change_power(chat, power)
    elif command == 400:
        chat1, chat2 = info[1], info[2]
        change_parent(chat1, chat2)
    else:
        chat = info[1]
        print_res(chat)