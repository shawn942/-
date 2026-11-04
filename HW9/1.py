
from collections import deque
from heapq import heappop, heappush
from itertools import count

# 上、右、下、左四個方向
DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))


# ==========================
# 共用函式
# ==========================

def locate(grid, mark):
    return next(
        (r, c)
        for r, row in enumerate(grid)
        for c, value in enumerate(row)
        if value == mark
    )


def passable(grid, point):
    r, c = point
    return (
        0 <= r < len(grid)
        and 0 <= c < len(grid[0])
        and grid[r][c] != "#"
    )


def neighbors(grid, point):
    for direction, (dr, dc) in enumerate(DIRECTIONS):
        nxt = (point[0] + dr, point[1] + dc)
        if passable(grid, nxt):
            yield nxt, direction


def rebuild(parent, end):
    path = []
    while end is not None:
        path.append(end)
        end = parent[end]
    return path[::-1]


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def draw(grid, path):
    board = [list(row) for row in grid]
    if path:
        for r, c in path[1:-1]:
            board[r][c] = "*"
    return "\n".join("".join(row) for row in board)


def bends(path):
    moves = [
        (b[0] - a[0], b[1] - a[1])
        for a, b in zip(path, path[1:])
    ]
    return sum(
        a != b for a, b in zip(moves, moves[1:])
    )


# ==========================
# 1. 老鼠走迷宮 DFS
# ==========================

MAZE = [
    "##########",
    "#S...#...#",
    "#.#.#.#..#",
    "#.#...#..#",
    "#.#####..#",
    "#.......G#",
    "##########",
]


def dfs(grid, start, goal):
    parent = {start: None}

    def visit(current):
        if current == goal:
            return True

        for nxt, _ in neighbors(grid, current):
            if nxt not in parent:
                parent[nxt] = current
                if visit(nxt):
                    return True

        return False

    return rebuild(parent, goal) if visit(start) else None


# ==========================
# 2. 狼羊甘藍菜 BFS
# ==========================

def solve_river():
    start = (0, 0, 0, 0)
    goal = (1, 1, 1, 1)

    queue = deque([start])
    parent = {start: (None, None)}

    while queue:
        state = queue.popleft()

        if state == goal:
            result = []
            while state is not None:
                previous, cargo = parent[state]
                result.append((state, cargo))
                state = previous
            return result[::-1]

        # None 表示農夫獨自過河
        for cargo in (None, 1, 2, 3):
            if cargo is not None and state[cargo] != state[0]:
                continue

            nxt = list(state)
            nxt[0] ^= 1

            if cargo is not None:
                nxt[cargo] ^= 1

            nxt = tuple(nxt)
            farmer, wolf, goat, cabbage = nxt

            safe = (
                (wolf != goat or farmer == wolf)
                and (goat != cabbage or farmer == goat)
            )

            if safe and nxt not in parent:
                parent[nxt] = (state, cargo)
                queue.append(nxt)

    return None


# ==========================
# 3. 八皇后 DFS + 回溯
# ==========================

def queens(n=8):
    solutions = []

    used_col = set()
    diag1 = set()
    diag2 = set()
    placement = []

    def search(row):
        if row == n:
            solutions.append(tuple(placement))
            return

        for col in range(n):
            if (
                col in used_col
                or row - col in diag1
                or row + col in diag2
            ):
                continue

            used_col.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            placement.append(col)

            search(row + 1)

            placement.pop()
            used_col.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    search(0)
    return solutions


def draw_queens(solution):
    n = len(solution)
    return "\n".join(
        " ".join(
            "Q" if solution[row] == col else "."
            for col in range(n)
        )
        for row in range(n)
    )


# ==========================
# 4. NPC A*
# 5. IC Dijkstra / A*
# ==========================

def best_first(
    grid, start, goal,
    bend_penalty=0,
    use_astar=True
):
    source = (start, -1)

    parent = {source: None}
    distance = {source: 0}
    ticket = count()

    first_h = manhattan(start, goal) if use_astar else 0

    queue = [(first_h, 0, next(ticket), source)]

    while queue:
        _, g, _, state = heappop(queue)

        if g != distance[state]:
            continue

        point, last_dir = state

        if point == goal:
            states = rebuild(parent, state)
            return [p for p, _ in states]

        for nxt, direction in neighbors(grid, point):
            turn = (
                bend_penalty
                if last_dir != -1 and direction != last_dir
                else 0
            )

            new_cost = g + 1 + turn
            new_state = (nxt, direction)

            if new_cost < distance.get(
                new_state, float("inf")
            ):
                distance[new_state] = new_cost
                parent[new_state] = state

                h = (
                    manhattan(nxt, goal)
                    if use_astar else 0
                )

                heappush(
                    queue,
                    (
                        new_cost + h,
                        new_cost,
                        next(ticket),
                        new_state,
                    ),
                )

    return None


NPC = [
    "############",
    "#S...#.....#",
    "#.#..#..##.#",
    "#.#........#",
    "#.#.###.##.#",
    "#...#......#",
    "###...##.#G#",
    "############",
]


# ==========================
# 5. IC 電路繞線
# ==========================

IC = [
    "###########",
    "#S..#.....#",
    "#.#.#.###.#",
    "#.#...#...#",
    "#.#####.#.#",
    "#.......#T#",
    "###########",
]


# 方法一：Lee Algorithm (BFS)
def bfs(grid, start, goal):
    queue = deque([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            return rebuild(parent, current)

        for nxt, _ in neighbors(grid, current):
            if nxt not in parent:
                parent[nxt] = current
                queue.append(nxt)

    return None


# 方法二：雙向 BFS
def bidirectional_bfs(grid, start, goal):
    if start == goal:
        return [start]

    front_a = {start}
    front_b = {goal}

    parent_a = {start: None}
    parent_b = {goal: None}

    def expand(frontier, own, other):
        next_frontier = set()

        for current in frontier:
            for nxt, _ in neighbors(grid, current):
                if nxt not in own:
                    own[nxt] = current

                    if nxt in other:
                        return next_frontier, nxt

                    next_frontier.add(nxt)

        return next_frontier, None

    def combine(meeting):
        left = rebuild(parent_a, meeting)
        right = []

        current = parent_b[meeting]

        while current is not None:
            right.append(current)
            current = parent_b[current]

        return left + right

    while front_a and front_b:
        front_a, meeting = expand(
            front_a, parent_a, parent_b
        )

        if meeting is not None:
            return combine(meeting)

        front_b, meeting = expand(
            front_b, parent_b, parent_a
        )

        if meeting is not None:
            return combine(meeting)

    return None


# 方法三：Hadlock Algorithm
def hadlock(grid, start, goal):
    queue = deque([start])
    detours = {start: 0}
    parent = {start: None}

    while queue:
        current = queue.popleft()

        for nxt, _ in neighbors(grid, current):
            away = int(
                manhattan(nxt, goal)
                > manhattan(current, goal)
            )

            new_cost = detours[current] + away

            if new_cost < detours.get(
                nxt, float("inf")
            ):
                detours[nxt] = new_cost
                parent[nxt] = current

                if away:
                    queue.append(nxt)
                else:
                    queue.appendleft(nxt)

    return (
        rebuild(parent, goal)
        if goal in parent
        else None
    )


# ==========================
# 主程式：執行五個題目
# ==========================

def main():
    print("\n===== 1. 老鼠走迷宮 DFS =====")

    start = locate(MAZE, "S")
    goal = locate(MAZE, "G")

    path = dfs(MAZE, start, goal)
    print(draw(MAZE, path))
    print("找到路徑：" if path else "無解",
          len(path) - 1 if path else "")

    print("\n===== 2. 狼羊甘藍菜 BFS =====")

    river = solve_river()
    names = {None: "獨自", 1: "狼", 2: "羊", 3: "甘藍菜"}

    for step, (state, cargo) in enumerate(river):
        if step == 0:
            print("起始狀態：", state)
        else:
            print(
                f"第 {step} 次：農夫帶 {names[cargo]} 過河 "
                f"=> {state}"
            )

    print("最少渡河次數：", len(river) - 1)

    print("\n===== 3. 八皇后 DFS =====")

    solutions = queens()
    print("解的總數：", len(solutions))
    print("第一組解：")
    print(draw_queens(solutions[0]))

    print("\n===== 4. NPC 搜尋玩家 A* =====")

    start = locate(NPC, "S")
    goal = locate(NPC, "G")

    path = best_first(NPC, start, goal)
    print(draw(NPC, path))
    print("最短步數：", len(path) - 1 if path else "無解")

    print("\n===== 5. IC 電路繞線 =====")

    start = locate(IC, "S")
    goal = locate(IC, "T")

    methods = [
        ("Lee BFS", bfs(IC, start, goal)),
        ("雙向 BFS", bidirectional_bfs(IC, start, goal)),
        ("DFS 回溯", dfs(IC, start, goal)),
        (
            "Dijkstra",
            best_first(IC, start, goal, 2, False),
        ),
        (
            "A*",
            best_first(IC, start, goal, 2, True),
        ),
        ("Hadlock", hadlock(IC, start, goal)),
    ]

    for name, path in methods:
        print(f"\n--- {name} ---")

        if path is None:
            print("無法完成繞線")
            continue

        steps = len(path) - 1
        turns = bends(path)
        cost = steps + 2 * turns

        print(draw(IC, path))
        print(f"線長：{steps} 格")
        print(f"轉彎：{turns} 次")
        print(f"加權成本：{cost}")


if __name__ == "__main__":
    main()
