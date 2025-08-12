def string_round(value, digit):
    value = str(round(float(value), digit)).removesuffix(".0")
    if "." in value:
        prefix, suffix = value.split(".")
        missing_zero = digit - len(suffix)
        if missing_zero > 0:
            suffix += "0" * missing_zero
        value = f"{prefix}.{suffix}"

    return "0" if value == "-0" else value
