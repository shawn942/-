def hanoi_recursive(n, source, target, auxiliary):
    """河內塔：遞迴解法"""
    if n == 1:
        print(f"移動盤子 1 從 {source} -> {target}")
        return
    # 將 n-1 個盤子從來源柱移到輔助柱
    hanoi_recursive(n - 1, source, auxiliary, target)
    print(f"移動盤子 {n} 從 {source} -> {target}")
    # 將 n-1 個盤子從輔助柱移到目標柱
    hanoi_recursive(n - 1, auxiliary, target, source)

if __name__ == "__main__":
    print("--- 河內塔 (遞迴) ---")
    hanoi_recursive(3, 'A', 'C', 'B')
  def hanoi_non_recursive(n, source, target, auxiliary):
    """河內塔：非遞迴解法（使用 Stack 模擬遞迴過程）"""
    # 堆疊儲存格式：(n, source, target, auxiliary)
    stack = [(n, source, target, auxiliary)]
    
    while stack:
        n, source, target, auxiliary = stack.pop()
        if n == 1:
            print(f"移動盤子 1 從 {source} -> {target}")
        else:
            # 由於 Stack 是 LIFO（後進先出），順序要與遞迴相反
            stack.append((n - 1, auxiliary, target, source))
            stack.append((1, source, target, auxiliary))
            stack.append((n - 1, source, auxiliary, target))

if __name__ == "__main__":
    print("\n--- 河內塔 (非遞迴) ---")
    hanoi_non_recursive(3, 'A', 'C', 'B')
