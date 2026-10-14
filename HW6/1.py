class Expr:
    pass

class Var(Expr):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

class Abs(Expr):
    def __init__(self, param, body):
        self.param = param
        self.body = body
    def __str__(self):
        return f"(λ{self.param}.{self.body})"

class App(Expr):
    def __init__(self, func, arg):
        self.func = func
        self.arg = arg
    def __str__(self):
        return f"({self.func} {self.arg})"

# 取得表達式中的自由變數
def free_vars(expr):
    if isinstance(expr, Var):
        return {expr.name}
    elif isinstance(expr, Abs):
        return free_vars(expr.body) - {expr.param}
    elif isinstance(expr, App):
        return free_vars(expr.func).union(free_vars(expr.arg))
    return set()

# 替換操作：expr[var_name := replacement]
def substitute(expr, var_name, replacement):
    if isinstance(expr, Var):
        if expr.name == var_name:
            return replacement
        return expr
    elif isinstance(expr, App):
        return App(
            substitute(expr.func, var_name, replacement),
            substitute(expr.arg, var_name, replacement)
        )
    elif isinstance(expr, Abs):
        if expr.param == var_name:
            return expr # 變數被遮蔽 (Shadowed)
        
        # 避免變數捕獲 (Alpha-conversion)
        if expr.param in free_vars(replacement) and var_name in free_vars(expr.body):
            new_param = expr.param + "'"
            # 先將原函數體內的舊參數換成新參數
            new_body = substitute(expr.body, expr.param, Var(new_param))
            return Abs(new_param, substitute(new_body, var_name, replacement))
        else:
            return Abs(expr.param, substitute(expr.body, var_name, replacement))

# 執行單步歸約 (Normal Order: 最左最外優先)
def reduce_step(expr):
    if isinstance(expr, Var):
        return expr, False
    elif isinstance(expr, Abs):
        new_body, reduced = reduce_step(expr.body)
        return Abs(expr.param, new_body), reduced
    elif isinstance(expr, App):
        # 找到 (λx.M) N 的形式，進行 Beta-reduction
        if isinstance(expr.func, Abs):
            return substitute(expr.func.body, expr.func.param, expr.arg), True
        
        # 否則先嘗試歸約左邊
        new_func, reduced_func = reduce_step(expr.func)
        if reduced_func:
            return App(new_func, expr.arg), True
        
        # 左邊無法歸約，再嘗試歸約右邊
        new_arg, reduced_arg = reduce_step(expr.arg)
        if reduced_arg:
            return App(expr.func, new_arg), True
            
    return expr, False

# 完整評估並顯示過程
def evaluate(expr, max_steps=50):
    print(f"初始輸入: {expr}")
    step = 1
    current_expr = expr
    while True:
        if step > max_steps:
            print("達到最大步數限制 (可能遇到無限迴圈，如 Omega 組合子)。")
            break
        current_expr, reduced = reduce_step(current_expr)
        if not reduced:
            print(f"最終結果 (Normal Form): {current_expr}\n")
            break
        print(f"Step {step}: {current_expr}")
        step += 1

# ==========================================
# 測試範例 (Lambda Calculus 程式輸入)
# ==========================================
if __name__ == "__main__":
    # 1. 恆等函數測試: (λx.x) y  -> y
    print("--- 範例 1: 恆等函數 (Identity) ---")
    id_func = Abs('x', Var('x'))
    expr1 = App(id_func, Var('y'))
    evaluate(expr1)

    # 2. 邱奇布林值 (Church Booleans): TRUE a b -> a
    # TRUE = λx.λy.x
    print("--- 範例 2: 邱奇布林值 TRUE ---")
    church_true = Abs('x', Abs('y', Var('x')))
    expr2 = App(App(church_true, Var('a')), Var('b'))
    evaluate(expr2)

    # 3. 邱奇布林值運算: NOT TRUE -> FALSE
    # FALSE = λx.λy.y
    # NOT = λp. p FALSE TRUE
    print("--- 範例 3: 邏輯 NOT 運算 ---")
    church_false = Abs('x', Abs('y', Var('y')))
    church_not = Abs('p', App(App(Var('p'), church_false), church_true))
    expr3 = App(church_not, church_true)
    evaluate(expr3)
