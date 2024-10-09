from collections import defaultdict
import heapq
L, Q = map(int, input().split())

query = []

entry_time = {}

position = {}

exit_time = defaultdict(int)

names = set()

p_queries = defaultdict(list)

for _ in range(Q):
    command = list(input().split(" "))

    n = -1
    x = -1
    name = -1

    if command[0] == '100':
        t, x, name = int(command[1]), int(command[2]), command[3] 
    elif command[0] == '200':
        t, x, name, n = int(command[1]), int(command[2]), command[3], int(command[4])
    elif command[0] == '300':
        t = int(command[1])

    heapq.heappush(query, (t, command[0], x, name, n))

    if command[0] == '100':
        p_queries[name].append((t, command[0], x, name, n))
    
    if command[0] == '200':
        names.add(name)
        entry_time[name] = t
        position[name] = x


for name in names:
    for t, cmd, x, p_n, n in p_queries[name]:
        time_match = 0

        if t < entry_time[name]:
            t_diff = entry_time[name] - t
            s_pos = (x + t_diff) % L
            time_match = entry_time[name]

            if position[name] > s_pos:
                add_time = position[name] - s_pos
                time_match += add_time
            elif position[name] < s_pos:
                add_time = L - (s_pos - position[name])
                time_match += add_time
        else:
            time_match = t

            if position[name] > x:
                add_time = position[name] - x
                time_match += add_time
            elif position[name] < x:
                add_time = L - (x - position[name])
                time_match += add_time
        
        exit_time[name] = max(exit_time[name], time_match)

        heapq.heappush(query, (time_match, '1', -1, name, -1))

for name in names:
    heapq.heappush(query, (exit_time[name], '2', -1, name, -1))

p_num = 0
s_num = 0

while query:
    info = heapq.heappop(query)
    cmd = info[1]

    if cmd == '100':
        s_num += 1
    elif cmd == '200':
        p_num += 1
    elif cmd == '1':
        s_num -= 1
    elif cmd == '2':
        p_num -= 1
    else:
        print(p_num, s_num)