from ..hierarchy import Node


def binary(parent: Node, x0: float, y0: float, x1: float, y1: float):
    """
    Recursively partitions the specified nodes into an approximately-balanced
    binary tree, choosing horizontal partitioning for wide rectangles and
    vertical partitioning for tall rectangles.

    Parameters
    ----------
    parent : Node
        Parent node
    x0 : float
        X-coordinate rectangular edge
    y0 : float
        Y-coordinate rectangular edge
    x1 : float
        X-coordinate rectangular edge
    y1 : float
        Y-coordinate rectangular edge
    """
    nodes = parent.children
    n = len(nodes)
    sums = [None] * (n + 1)

    sum_value = sums[0] = 0
    for i in range(n):
        sum_value += nodes[i].value
        sums[i + 1] = sum_value

    def partition(i, j, value, x0, y0, x1, y1):
        if i >= j - 1:
            node = nodes[i]
            node.x0 = x0
            node.x1 = x1
            node.y0 = y0
            node.y1 = y1
            return

        value_offset = sums[i]
        value_target = (value * 0.5) + value_offset
        k = i + 1
        hi = j - 1

        while k < hi:
            mid = k + hi >> 1
            if sums[mid] < value_target:
                k = mid + 1
            else:
                hi = mid

        if (value_target - sums[k - 1]) < (sums[k] - value_target) and i + 1 < k:
            k -= 1

        value_left = sums[k] - value_offset
        value_right = value - value_left

        if (x1 - x0) > (y1 - y0):
            xk = (x0 * value_right + x1 * value_left) / value if value else x1
            partition(i, k, value_left, x0, y0, xk, y1)
            partition(k, j, value_right, xk, y0, x1, y1)
        else:
            yk = (y0 * value_right + y1 * value_left) / value if value else y1
            partition(i, k, value_left, x0, y0, x1, yk)
            partition(k, j, value_right, x0, yk, x1, y1)

    partition(0, n, parent.value, x0, y0, x1, y1)
