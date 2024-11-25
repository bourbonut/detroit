def format_numerals(numerals):
    def replace(value):
        return "".join(numerals[int(c)] if c.isdigit() else c for c in value)

    return replace
