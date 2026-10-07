def sym_diff(expr, var='x'):
    """
    符號數學式微分：支援常數、變數、加法、乘法
    表達式格式範例：
    - ('const', c) -> 常數 c
    - ('var', 'x') -> 變數 x
    - ('add', left, right) -> left + right
    - ('mul', left, right) -> left * right
    """
    expr_type = expr[0]
    
    if expr_type == 'const':
        # 常數微分為 0
        return ('const', 0)
    
    elif expr_type == 'var':
        # 若變數相符則微分為 1，否則為 0
        if expr[1] == var:
            return ('const', 1)
        else:
            return ('const', 0)
            
    elif expr_type == 'add':
        # 加法法則：d(f + g)/dx = df/dx + dg/dx
        _, left, right = expr
        return ('add', sym_diff(left, var), sym_diff(right, var))
        
    elif expr_type == 'mul':
        # 乘法法則：d(f * g)/dx = f * dg/dx + g * df/dx
        _, left, right = expr
        return ('add', 
                ('mul', left, sym_diff(right, var)), 
                ('mul', right, sym_diff(left, var)))
    
    raise ValueError(f"不支援的運算型態: {expr_type}")

if __name__ == "__main__":
    # 測試對表達式 x * x + 3 進行微分
    # 代表運算式：(x * x) + 3
    expr = ('add', ('mul', ('var', 'x'), ('var', 'x')), ('const', 3))
    diff_expr = sym_diff(expr, 'x')
    print("\n--- 符號微分結果 ---")
    print(f"原始運算式結構: {expr}")
    print(f"微分後結構: {diff_expr}")
