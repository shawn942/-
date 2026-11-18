from itertools import product
from math import prod
from random import Random


def derivative(f, x, h=1e-5):
    """單變數中央差分：f'(x) ≈ [f(x+h)-f(x-h)]/(2h)。"""
    return (f(x + h) - f(x - h)) / (2 * h)


def riemann_1d(f, low, high, m=1000):
    """一維中點黎曼和。"""
    if m < 1:
        raise ValueError("m 必須大於 0")
    dx = (high - low) / m
    return sum(f(low + (k + 0.5) * dx) for k in range(m)) * dx


def monte_carlo_1d(f, low, high, samples=100000, seed=42):
    """一維蒙地卡羅積分。"""
    if samples < 1:
        raise ValueError("samples 必須大於 0")
    rng = Random(seed)
    width = high - low
    return width * sum(f(low + width * rng.random()) for _ in range(samples)) / samples


def gradient(f, x, h=1e-5):
    """中央差分算 n 維梯度，f 接收一個座標陣列。"""
    result = []
    for i in range(len(x)):
        plus, minus = list(x), list(x)
        plus[i] += h
        minus[i] -= h
        result.append((f(plus) - f(minus)) / (2 * h))
    return result


def integral(f, low, high, m=10):
    """n 維中點黎曼和，n = len(low) = len(high)。

    一般函數：直接列舉 m**n 個小方格（最多 100 萬格）。
    可加性分離的函數：若提供 f.additive_terms(n)，可把完整
    n 維黎曼和等價地分解為 n 個一維黎曼和，支援 100 維。
    """
    n = len(low)
    if n == 0 or n != len(high):
        raise ValueError("low 和 high 必須是相同長度的非空陣列")
    if not isinstance(m, int) or m < 1:
        raise ValueError("m 必須是正整數")
    widths = [high[i] - low[i] for i in range(n)]
    volume = prod(widths)
    if volume == 0:
        return 0.0

    if m ** n <= 1_000_000:
        steps = [width / m for width in widths]
        cell_volume = prod(steps)
        total = 0.0
        for indexes in product(range(m), repeat=n):
            x = [low[i] + (indexes[i] + 0.5) * steps[i]
                 for i in range(n)]
            total += f(x)
        return total * cell_volume

    # 對 f(x) = g_1(x_1) + ... + g_n(x_n)，這是「同一個」
    # n 維黎曼網格求和的代數化簡，而不是蒙地卡羅近似。
    if hasattr(f, "additive_terms"):
        terms = f.additive_terms(n)
        if len(terms) != n:
            raise ValueError("additive_terms 必須回傳 n 個一維函數")
        mean_sum = 0.0
        for i, g in enumerate(terms):
            dx = widths[i] / m
            mean_sum += sum(g(low[i] + (k + 0.5) * dx)
                            for k in range(m)) / m
        return volume * mean_sum

    raise ValueError(
        f"{n} 維、每維 {m} 格，需要 {m**n} 個網格點；"
        "一般函數無法實際逐格列舉。請減少 m，或對可加性分離函數提供 additive_terms。"
    )


def monte_carlo_nd(f, low, high, samples=50000, seed=42):
    """n 維蒙地卡羅積分，計算成本約為 samples*n。"""
    n = len(low)
    if n == 0 or n != len(high):
        raise ValueError("low 和 high 必須是相同長度的非空陣列")
    if samples < 1:
        raise ValueError("samples 必須大於 0")
    widths = [high[i] - low[i] for i in range(n)]
    volume = prod(widths)
    if volume == 0:
