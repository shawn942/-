
import math
import itertools
import random
import numpy as np
from scipy.optimize import linear_sum_assignment

# 六個城市的座標
cities = {
    "A": (0, 0),
    "B": (2, 6),
    "C": (5, 2),
    "D": (8, 6),
    "E": (9, 0),
    "F": (4, -3)
}

names = list(cities)
xy = np.array(list(cities.values()), dtype=float)
n = len(names)

# 建立距離矩陣
D = np.linalg.norm(
    xy[:, None, :] - xy[None, :, :], axis=2
)

# 計算完整巡迴路線的總距離
def length(route):
    return sum(
        D[route[i], route[(i + 1) % n]]
        for i in range(n)
    )

def show(route):
    return " -> ".join(
        names[i] for i in route + [route[0]]
    )


# 方法一：改良法（First Improvement 2-opt）
def two_opt(route):
    route = route[:]
    changed = True

    while changed:
        changed = False

        for i in range(1, n - 1):
            for j in range(i + 1, n):
                cand = (
                    route[:i]
                    + route[i:j + 1][::-1]
                    + route[j + 1:]
                )

                if length(cand) < length(route) - 1e-9:
                    route = cand
                    changed = True
                    break

            if changed:
                break

    return route


# 方法二：爬山演算法（Best Improvement）
def hill_climbing(route):
    while True:
        neighbors = [
            route[:i] + route[i:j + 1][::-1]
            + route[j + 1:]
            for i in range(1, n - 1)
            for j in range(i + 1, n)
        ]

        best = min(neighbors, key=length)

        if length(best) >= length(route) - 1e-9:
            return route

        route = best


# 方法三：模擬退火法
def simulated_annealing(route):
    rng = random.Random(42)
    best = cur = route[:]
    temperature = 20.0

    for step in range(8000):
        i, j = sorted(rng.sample(range(1, n), 2))

        cand = (
            cur[:i]
            + cur[i:j + 1][::-1]
            + cur[j + 1:]
        )

        delta = length(cand) - length(cur)

        # 接受較佳解，或依溫度接受較差解
        if delta < 0 or rng.random() < math.exp(
            -delta / temperature
        ):
            cur = cand

            if length(cur) < length(best):
                best = cur[:]

        temperature = max(
            0.01, temperature * 0.998
        )

    return best


# 方法四：梯度下降法（連續鬆弛）
def softmax(z):
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


def gradient_descent():
    rng = np.random.default_rng(7)

    # 每一列代表拜訪位置
    # 每一欄代表一座城市
    z = rng.normal(0, 0.1, (n, n))

    # 固定起點為 A
    z[0, :] = -8
    z[0, 0] = 8

    # 對連續鬆弛目標函數做梯度下降
    for step in range(7000):
        p = softmax(z)

        nxt = np.roll(p, -1, axis=0)
        prv = np.roll(p, 1, axis=0)

        # 每座城市應恰好出現一次
        col = p.sum(axis=0) - 1

        # 預期路程與重複城市懲罰的梯度
        gp = (
            nxt @ D.T
            + prv @ D
            + 30 * col[None, :]
        )

        # Softmax 的鏈式微分
        gz = p * (
            gp - (gp * p).sum(
                axis=1, keepdims=True
            )
        )

        # 更新，保留第一個位置為 A
        learning_rate = 0.1
        z[1:] -= learning_rate * gz[1:]

    p = softmax(z)

    # 將連續結果轉換成合法的城市排列
    # 第一個位置固定 A，其餘使用線性指派
    rows, cols = linear_sum_assignment(-p[1:, 1:])

    route = [0] + [
        int(cols[np.where(rows == r)[0][0]] + 1)
        for r in range(n - 1)
    ]

    return route


# 方法五：貪婪演算法（最近鄰居）
def greedy():
    path = [0]

    while len(path) < n:
        next_city = min(
            (i for i in range(n) if i not in path),
            key=lambda i: D[path[-1], i]
        )

        path.append(next_city)

    return path


# 統一比較五種演算法
initial = [0, 3, 1, 4, 2, 5]

methods = {
    "改良法": two_opt(initial),
    "爬山演算法": hill_climbing(initial),
    "模擬退火法": simulated_annealing(initial),
    "梯度下降法": gradient_descent(),
    "貪婪演算法": greedy()
}

print("初始路線：", show(initial))
print("初始距離：", round(length(initial), 3))
print()

for method, route in methods.items():
    print(method)
    print("路線：", show(route))
    print("總距離：", round(length(route), 3))
    print()

# 小型範例可使用窮舉法驗證最佳解
exact = min(
    ([0] + list(p)
     for p in itertools.permutations(range(1, n))),
    key=length
)

print("窮舉法驗證最佳路線：", show(exact))
print("最佳距離：", round(length(exact), 3))
