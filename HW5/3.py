# --- 1. 自製 map, filter, reduce (禁止使用內建或迴圈) ---

def my_map(func, iterable):
    if not iterable:
        return []
    return [func(iterable[0])] + my_map(func, iterable[1:])

def my_filter(func, iterable):
    if not iterable:
        return []
    head, tail = iterable[0], iterable[1:]
    if func(head):
        return [head] + my_filter(func, tail)
    else:
        return my_filter(func, tail)

def my_reduce(func, iterable, initializer=None):
    if not iterable:
        return initializer
    if initializer is None:
        return my_reduce(func, iterable[1:], iterable[0])
    return my_reduce(func, iterable[1:], func(initializer, iterable[0]))


# --- 2. 不使用迴圈的泡沫排序 ---

def _bubble_pass(arr):
    """單次氣泡掃描：把較大的元素往右推，完全不使用迴圈"""
    if len(arr) <= 1:
        return arr
    
    head1, head2 = arr[0], arr[1]
    if head1 > head2:
        # 交換並繼續往後掃描
        rest = _bubble_pass([head1] + arr[2:])
        return [head2] + rest
    else:
        rest = _bubble_pass([head2] + arr[2:])
        return [head1] + rest

def bubble_sort_no_loop(arr):
    """利用遞迴與單次掃描實現無迴圈泡沫排序"""
    if len(arr) <= 1:
        return arr
    
    # 執行一次完整掃描，將最大值推到最右側
    pass_result = _bubble_pass(arr)
    
    # 排除最後一個已定位的最大值，對其餘部分遞迴排序
    sorted_rest = bubble_sort_no_loop(pass_result[:-1])
    return sorted_rest + [pass_result[-1]]

if __name__ == "__main__":
    print("\n--- 無迴圈泡沫排序測試 ---")
    data = [64, 34, 25, 12, 22, 11, 90]
    print(f"排序前: {data}")
    sorted_data = bubble_sort_no_loop(data)
    print(f"排序後: {sorted_data}")
