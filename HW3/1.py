from itertools import product

def solve_sat(variables, clauses):
    solutions = []

    print(" | ".join(variables) + " | Result")
    print("-" * 25)

    # 列舉所有 True / False 組合
    for values in product([False, True], repeat=len(variables)):
        assignment = dict(zip(variables, values))

        def check(literal):
            if literal.startswith("!"):
                return not assignment[literal[1:]]
            return assignment[literal]

        # OR 子句之間使用 AND 連接
        result = all(
            any(check(x) for x in clause)
            for clause in clauses
        )

        print(*[int(x) for x in values], "|", int(result))

        if result:
            solutions.append(assignment)

    if solutions:
        print("\nSAT：有解")
        for solution in solutions:
            print(solution)
    else:
        print("\nUNSAT：無解")


# 主程式
variables = ["A", "B", "C"]

# (A OR B) AND (NOT A OR C) AND (NOT B OR NOT C)
clauses = [
    ["A", "B"],
    ["!A", "C"],
    ["!B", "!C"]
]

solve_sat(variables, clauses)
