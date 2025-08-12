def format_decimal(x, _):
    x = round(x)
    if abs(x) >= 1e21:
        return str(x).replace(",", "")
    return str(x)


def format_decimal_parts(x, p):
    try:
        if p is not None:
            x_str = f"{x:.{p - 1}e}"
        else:
            x_str = f"{x:e}"

        i = x_str.find("e")
        if i < 0:
            return None  # NaN, ±Infinity

        coefficient = x_str[:i]
        if len(coefficient) > 1:
            coefficient = coefficient[0] + coefficient[2:]  # Remove decimal point

        return [coefficient, int(x_str[i + 1 :])]
    except (ValueError, TypeError):
        return None
