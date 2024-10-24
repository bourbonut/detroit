def sinebow(t):
    pi_1_3 = np.pi / 3
    pi_2_3 = np.pi * 2 / 3
    t = (0.5 - t) * np.pi
    r = 255 * (x := np.sin(t)) * x
    g = 255 * (x := np.sin(t + pi_1_3)) * x
    b = 255 * (x := np.sin(t + pi_2_3)) * x
    return f"rgb({int(r)}, {int(g)}, {int(b)})"
