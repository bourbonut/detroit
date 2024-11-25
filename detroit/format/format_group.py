def format_group(grouping, thousands):
    def group(value, width):
        i = len(value)
        t = []
        j = 0
        g = grouping[0]
        length = 0

        while i > 0 and g > 0:
            if length + g + 1 > width:
                g = max(1, width - length)
            i -= g
            t.append(value[max(0, i) : i + g])
            length += g + 1
            if length > width:
                break
            j = (j + 1) % len(grouping)
            g = grouping[j]

        return thousands.join(reversed(t))

    return group
