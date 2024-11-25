def format_trim(s):
    n = len(s)
    i0 = -1
    i1 = 0
    for i in range(1, n):
        c = s[i]
        if c == ".":
            i0 = i1 = i
        elif c == "0":
            if i0 == 0:
                i0 = i
            i1 = i
        else:
            if not c.isdigit():
                break
            if i0 > 0:
                i0 = 0
    return s[:i0] + s[i1 + 1 :] if i0 > 0 else s
