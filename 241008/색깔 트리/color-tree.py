MAX_ID = 100001
MAX_DEPTH = 101
COLOR_MAX = 5

isRoot = [False] * MAX_ID

class Node:
    def __init__(self):
        self.id = 0
        self.color = 0
        self.lastUpdate = 0
        self.maxDepth = 0
        self.parentId = 0
        self.childIds = []

class ColorCount:
    def __init__(self):
        self.cnt = [0] * (COLOR_MAX + 1)
    
    def __add__(self, obj):
        res = ColorCount()
        for i in range(1, COLOR_MAX + 1):
            res.cnt[i] = self.cnt[i] + obj.cnt[i]
        return res
    
    def score(self):
        result = 0
        for i in range(1, COLOR_MAX + 1):
            result += 1 if self.cnt[i] else 0 
        
        return result * result

nodes = [Node() for _ in range(MAX_ID)]

def canMakeChild(curr, needDepth):
    if curr.id == 0:
        return True
    if curr.maxDepth <= needDepth:
        return False
    
    return canMakeChild(nodes[curr.parentId], needDepth + 1)

def getColor(curr):
    if curr.id == 0:
        return 0, 0
    info = getColor(nodes[curr.parentId])
    if info[1] > curr.lastUpdate:
        return info
    else:
        return curr.color, curr.lastUpdate

def getBeauty(curr, color, lastUpdate):
    if lastUpdate < curr.lastUpdate:
        lastUpdate = curr.lastUpdate
        color = curr.color
    result = [0, ColorCount()]
    result[1].cnt[color] = 1

    for childId in curr.childIds:
        child = nodes[childId]
        subResult = getBeauty(child, color, lastUpdate)
        result[1] = result[1] + subResult[1]
        result[0] += subResult[0]
    result[0] += result[1].score()
    return result


if __name__ == "__main__":
    Q = int(input())

    for i in range(1, Q+1):
        query = list(map(int, input().split()))

        T = query[0]

        if T == 100:
            mId, pId, color, maxDepth = query[1:]
            if pId == -1:
                isRoot[mId] = True
            if isRoot[mId] or canMakeChild(nodes[pId], 1):
                nodes[mId].id = mId
                nodes[mId].color = color
                nodes[mId].maxDepth = maxDepth
                nodes[mId].parentId = 0 if isRoot[mId] else pId
                nodes[mId].lastUpdate = i

                if not isRoot[mId]:
                    nodes[pId].childIds.append(mId)
        elif T == 200:
            mId, color = query[1:]
            nodes[mId].color = color
            nodes[mId].lastUpdate = i
        elif T == 300:
            mId = query[1]
            print(getColor(nodes[mId])[0])
        elif T == 400:
            beauty = 0
            for i in range(1, MAX_ID):
                if isRoot[i]:
                    beauty += getBeauty(nodes[i], nodes[i].color, nodes[i].lastUpdate)[0]
            print(beauty)