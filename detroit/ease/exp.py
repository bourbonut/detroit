from .tqmt import tqmt

def ease_exp_in(t: float) -> float:
    return tqmt(1 - t)

def ease_exp_out(t: float) -> float:
    return 1 - tqmt(t)

def ease_exp_in_out(t: float) -> float:
    t *= 2
    if t <= 1:
        return tqmt(1 - t) * 0.5
    else:
        return (2 - tqmt(t - 1)) * 0.5
