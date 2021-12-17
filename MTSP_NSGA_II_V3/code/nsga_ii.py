import math


def fast_non_dominated_sort(f1val, f2val):
    S = [[] for i in range(0, len(f1val))]
    front = [[]]
    n = [0 for i in range(0, len(f1val))]
    rank = [0 for i in range(0, len(f1val))]

    for p in range(0, len(f1val)):
        S[p] = []
        n[p] = 0
        for q in range(0, len(f1val)):
            if (
                    (f1val[p] > f1val[q] and f2val[p] > f2val[q])
                    or (f1val[p] >= f1val[q] and f2val[p] > f2val[q])
                    or (f1val[p] > f1val[q] and f2val[p] >= f2val[q])
            ):
                if q not in S[p]:
                    S[p].append(q)
            elif (
                    (f1val[q] > f1val[p] and f2val[q] > f2val[p])
                    or (f1val[q] >= f1val[p] and f2val[q] > f2val[p])
                    or (f1val[q] > f1val[p] and f2val[q] >= f2val[p])
            ):
                n[p] = n[p] + 1
        if n[p] == 0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)

    i = 0
    while front[i] != []:
        Q = []
        for p in front[i]:
            for q in S[p]:
                n[q] = n[q] - 1
                if n[q] == 0:
                    rank[q] = i + 1
                    if q not in Q:
                        Q.append(q)
        i = i + 1
        front.append(Q)

    del front[len(front) - 1]

    front.reverse()
    return front


def crowding_distance(f1val, f2val, front):
    distance = [0 for i in range(0, len(front))]
    sorted1 = sorted(front, key=lambda x: f1val[x])
    sorted2 = sorted(front, key=lambda x: f2val[x])
    distance[0] = math.inf
    distance[len(front) - 1] = math.inf
    flag = (not math.isclose(max(f1val), min(f1val), rel_tol=1e-5)) and \
           (not math.isclose(max(f2val), min(f2val), rel_tol=1e-5))

    for k in range(1, len(front) - 1):
        if flag:
            distance[k] = distance[k] + (
                    f1val[sorted1[k + 1]] - f2val[sorted1[k - 1]]
            ) / (max(f1val) - min(f1val))
        else:
            distance[k] = math.inf
    for k in range(1, len(front) - 1):
        if flag:
            distance[k] = distance[k] + (
                    f1val[sorted2[k + 1]] - f2val[sorted2[k - 1]]
            ) / (max(f2val) - min(f2val))
        else:
            distance[k] = math.inf
    return distance
