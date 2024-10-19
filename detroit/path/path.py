import math

pi = math.pi
tau = 2 * pi
epsilon = 1e-6
tauEpsilon = tau - epsilon

class Path:
    def __init__(self, digits=None):
        self._x0 = self._y0 = 0  # start of current subpath
        self._x1 = self._y1 = None  # end of current subpath
        self._ = ""
        self._append = self.append if digits is None else self.append_round(digits)

    def append(self, strings):
        self._ += strings[0]
        for i in range(1, len(strings)):
            self._ += str(arguments[i]) + strings[i]

    def append_round(self, digits):
        d = math.floor(digits)
        if d < 0:
            raise ValueError(f"invalid digits: {digits}")
        if d > 15:
            return self.append
        k = 10 ** d

        def round_append(strings):
            self._ += strings[0]
            for i in range(1, len(strings)):
                self._ += str(round(arguments[i] * k) / k) + strings[i]

        return round_append

    def move_to(self, x, y):
        self._append([f'M{self._x0 := self._x1 := float(x)}, {self._y0 := self._y1 := float(y)}'])

    def close_path(self):
        if self._x1 is not None:
            self._x1, self._y1 = self._x0, self._y0
            self._append(['Z'])

    def line_to(self, x, y):
        self._append([f'L{self._x1 := float(x)}, {self._y1 := float(y)}'])

    def quadratic_curve_to(self, x1, y1, x, y):
        self._append([f'Q{float(x1)}, {float(y1)}, {self._x1 := float(x)}, {self._y1 := float(y)}'])

    def bezier_curve_to(self, x1, y1, x2, y2, x, y):
        self._append([f'C{float(x1)}, {float(y1)}, {float(x2)}, {float(y2)}, {self._x1 := float(x)}, {self._y1 := float(y)}'])

    def arc_to(self, x1, y1, x2, y2, r):
        x1, y1, x2, y2, r = float(x1), float(y1), float(x2), float(y2), float(r)

        # Is the radius negative? Error.
        if r < 0:
            raise ValueError(f"negative radius: {r}")

        x0, y0 = self._x1, self._y1
        x21, y21 = x2 - x1, y2 - y1
        x01, y01 = x0 - x1, y0 - y1
        l01_2 = x01 * x01 + y01 * y01

        # Is this path empty? Move to (x1,y1).
        if self._x1 is None:
            self._append([f'M{self._x1 := x1}, {self._y1 := y1}'])

        # Or, is (x1,y1) coincident with (x0,y0)? Do nothing.
        elif not (l01_2 > epsilon):
            pass

        # Or, are (x0,y0), (x1,y1) and (x2,y2) collinear?
        # Equivalently, is (x1,y1) coincident with (x2,y2)?
        # Or, is the radius zero? Line to (x1,y1).
        elif not (abs(y01 * x21 - y21 * x01) > epsilon) or not r:
            self._append([f'L{self._x1 := x1}, {self._y1 := y1}'])

        # Otherwise, draw an arc!
        else:
            x20, y20 = x2 - x0, y2 - y0
            l21_2 = x21 * x21 + y21 * y21
            l20_2 = x20 * x20 + y20 * y20
            l21 = math.sqrt(l21_2)
            l01 = math.sqrt(l01_2)
            l = r * math.tan((pi - math.acos((l21_2 + l01_2 - l20_2) / (2 * l21 * l01))) / 2)
            t01 = l / l01
            t21 = l / l21

            # If the start tangent is not coincident with (x0,y0), line to.
            if abs(t01 - 1) > epsilon:
                self._append([f'L{(x1 + t01 * x01)}, {(y1 + t01 * y01)}'])

            self._append([f'A{r}, {r}, 0, 0, {int(y01 * x20 > x01 * y20)}, {self._x1 := (x1 + t21 * x21)}, {self._y1 := (y1 + t21 * y21)}'])

    def arc(self, x, y, r, a0, a1, ccw):
        x, y, r, ccw = float(x), float(y), float(r), bool(ccw)

        # Is the radius negative? Error.
        if r < 0:
            raise ValueError(f"negative radius: {r}")

        dx = r * math.cos(a0)
        dy = r * math.sin(a0)
        x0 = x + dx
        y0 = y + dy
        cw = 1 ^ ccw
        da = a0 - a1 if ccw else a1 - a0

        # Is this path empty? Move to (x0,y0).
        if self._x1 is None:
            self._append([f'M{x0}, {y0}'])

        # Or, is (x0,y0) not coincident with the previous point? Line to (x0,y0).
        elif abs(self._x1 - x0) > epsilon or abs(self._y1 - y0) > epsilon:
            self._append([f'L{x0}, {y0}'])

        # Is this arc empty? We’re done.
        if not r:
            return

        # Does the angle go the wrong way? Flip the direction.
        if da < 0:
            da = da % tau + tau

        # Is this a complete circle? Draw two arcs to complete the circle.
        if da > tauEpsilon:
            self._append([f'A{r}, {r}, 0, 1, {cw}, {x - dx}, {y - dy} A{r}, {r}, 0, 1, {cw}, {self._x1 := x0}, {self._y1 := y0}'])

        # Is this arc non-empty? Draw an arc!
        elif da > epsilon:
            self._append([f'A{r}, {r}, 0, {int(da >= pi)}, {cw}, {self._x1 := (x + r * math.cos(a1))}, {self._y1 := (y + r * math.sin(a1))}'])

    def rect(self, x, y, w, h):
        self._append([f'M{self._x0 := self._x1 := float(x)}, {self._y0 := self._y1 := float(y)} h{w := float(w)} v{float(h)} h{-w} Z'])

    def __str__(self):
        return self._

def path():
    return Path()

# Allow isinstance d3.path
path.__class__ = Path

def path_round(digits=3):
    return Path(float(digits))
