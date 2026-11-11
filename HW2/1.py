import math

# 第 1 題：T(n) = T(n-1) + 8
def T1(n):
    if n == 1:
        return 1
    return T1(n-1) + 8

# 第 2 題：T(n) = 2T(n-1) + 9
def T2(n):
    if n == 1:
        return 1
    return 2 * T2(n-1) + 9

# 第 3 題：T(n) = 2T(n/2) + 1
def T3(n):
    if n == 1:
        return 1
    return 2 * T3(請寫一個程式可以系統性的列舉真值表，解決 SAT 問題
SAT 問題 -- https://en.wikipedia.org/wiki/Boolean_satisfiability_problem
n//2) + 1

# 第 4 題：T(n) = T(n/2) + 1
def T4(n):
    if n == 1:
        return 1
    return T4(n//2) + 1


# 主程式
n = 16

print("n =", n)
print("-----------------------------")

print("第1題:", T1(n))
print("公式: 8n - 7")
print("Big O: O(n)")

print("-----------------------------")

print("第2題:", T2(n))
print("公式: 10 * 2^(n-1) - 9")
print("Big O: O(2^n)")

print("-----------------------------")

print("第3題:", T3(n))
print("公式: 2n - 1")
print("Big O: O(n)")

print("-----------------------------")

print("第4題:", T4(n))
print("公式: log2(n) + 1")
print("Big O: O(log n)")
