def colors(specifier):
    n = len(specifier) // 6
    return ["#" + specifier[i * 6 : (i + 1) * 6] for i in range(n)]
