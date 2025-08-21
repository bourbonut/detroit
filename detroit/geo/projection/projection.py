from ..clip import geo_clip_antimeridian, geo_clip_circle, geo_clip_rectangle
from ..compose import Compose
from math import cos, degrees, radians, sin, sqrt, isnan
from ..rotation import RotateRadians
from ..transform import Transformer
from .fit import fit_extent, fit_size, fit_height, fit_width
from .resample import resample

def point(self, x, y):
    self._stream.point(radians(x), radians(y))

transform_radians = Transformer({"point": point})

def transform_rotate(rotate):
    def point(self, x, y):
        r = rotate(x, y)
        return self._stream.point(r[0], r[1])
    return Transformer({"point": point})


class ScaleTranslate:
    def __init__(self, k, dx, dy, sx, sy):
        self._k = k
        self._dx = dx
        self._dy = dy
        self._sx = sx
        self._sy = sy

    def __call__(self, x, y):
        x *= self._sx
        y *= self._sy
        return [self._dx + self._k * x, self._dy - self._k * y]

    def invert(self, x, y):
        return [(x - self._dx) / self._k * self._sx, (self._dy - y) / self._k * self._sy]

class ScaleTranslateRotate:

    def __init__(self, k, dx, dy, sx, sy, alpha):
        self._cos_alpha = cos(alpha)
        self._sin_alpha = sin(alpha)
        self._sx = sx
        self._sy = sy
        self._k = k
        self._a = self._cos_alpha * self._k
        self._b = self._sin_alpha * self._k
        self._ai = self._cos_alpha / self._k
        self._bi = self._sin_alpha / self._k
        self._ci = (self._sin_alpha * self._dy - self._cos_alpha * self._dx) / self._k
        self._fi = (self._sin_alpha * self._dx + self._cos_alpha * self._dy) / self._k

    def __call__(self, x, y):
        x *= self._sx
        y *= self._sy
        return [self._a * x - self._b * y + self._dx, self._dy - self._b * self._x - self._a * y]

    def invert(self, x, y):
        return [self._sx * (self._ai * x - self._bi * y + self._ci), self._sy * (self._fi - self._bi * x - self._ai * y)]

def scale_translate_rotate(k, dx, dy, sx, sy, alpha):
    if alpha:
        return ScaleTranslateRotate(k, dx, dy, sx, sy, alpha)
    else:
        return ScaleTranslate(k, dx, dy, sx, sy)

def identity(x):
    return x

class ProjectionMutator:

    def __init__(self, project):
        self._project = project
        self._invert = self._invert_default if hasattr(project, "invert") else self._invert_error
        self._k = 150
        self._x = 480
        self._y = 250
        self._lambda = 0
        self._phi = 0
        self._delta_lambda = 0
        self._delta_phi = 0
        self._delta_gamma = 0
        self._rotate = None
        self._alpha = 0
        self._sx = 1
        self._sy = 1
        self._theta = None
        self._preclip = geo_clip_antimeridian
        self._x0 = None
        self._y0 = None
        self._x1 = None
        self._y1 = None
        self._postclip = identity
        self._delta2 = 0.5
        self._project_resample = None
        self._project_transform = None
        self._project_rotate_transform = None
        self._cache = None
        self._cache_stream = None

    def __call__(self, point):
        return self._project_rotate_transform(radians(point[0]), radians(point[1]))

    def invert(self, point):
        return self._invert(point)

    def _invert_default(self, point):
        point = self._project_rotate_transform.invert(point[0], point[1])
        if isinstance(point, float) and isnan(point):
            return point
        else:
            return [degrees(point[0]), degrees(point[1])]

    def _invert_error(self, point):
        raise NotImplementedError("Projection does not support invert method.")

    def stream(self, stream):
        if self._cache and self._cache_stream == stream:
            return self._cache
        self._cache_stream = stream
        clipped_stream = self._preclip(self._project_resample(self._postclip(stream)))
        self._cache = transform_radians(transform_rotate(self._rotate)(clipped_stream))
        return self._cache

    def set_preclip(self, preclip):
        self._preclip = preclip
        self._theta = None
        return self.reset()

    def set_postclip(self, postclip):
        self._postclip = postclip
        self._x0 = None
        self._x1 = None
        self._y0 = None
        self._y1 = None
        return self.reset()

    def set_clip_angle(self, clip_angle):
        if clip_angle:
            self._theta = radians(clip_angle)
            self._preclip = geo_clip_circle(self._theta)
        else:
            self._theta = None
            self._preclip = geo_clip_antimeridian
        return self.reset()

    def set_clip_extent(self, clip_extent = None):
        if clip_extent is None:
            self._x0 = None
            self._x1 = None
            self._y0 = None
            self._y1 = None
            self._postclip = identity
        else:
            self._x0 = clip_extent[0][0]
            self._x1 = clip_extent[1][0]
            self._y0 = clip_extent[0][1]
            self._y1 = clip_extent[1][1]
            self._postclip = geo_clip_rectangle(self._x0, self._y0, self._x1, self._y1)
        return self.reset()

    def scale(self, k):
        self._k = k
        return self.recenter()

    def translate(self, translation):
        self._x = translation[0]
        self._y = translation[1]
        return self.recenter()

    def set_center(self, center):
        self._lambda = radians(center[0] % 360)
        self._phi = radians(center[1] % 360)
        return self.recenter()

    def rotate(self, rotation):
        self._delta_lambda = radians(rotation[0] % 360)
        self._delta_phi = radians(rotation[1] % 360)
        self._delta_gamma = radians(rotation[2] % 360) if len(rotation) > 2 else 0
        return self.recenter()

    def set_angle(self, angle):
        self._alpha = radians(angle % 360)
        return self.recenter()

    def set_reflect_x(self, reflect_x):
        self._sx = -1 if reflect_x else 1
        return self.recenter()

    def set_reflect_y(self, reflect_y):
        self._sy = -1 if reflect_y else 1
        return self.recenter()

    def set_precision(self, precision):
        self._delta2 = precision * precision
        self._project_resample = resample(self._project_transform, self._delta2)
        return self.reset()

    def fit_extent(self, extent, obj):
        return fit_extent(self, extent, obj)

    def fit_size(self, size, obj):
        return fit_size(self, size, obj)

    def fit_width(self, width, obj):
        return fit_width(self, width, obj)

    def fit_height(self, height, obj):
        return fit_height(self, height, obj)

    def recenter(self):
        center = scale_translate_rotate(self._k, 0, 0, self._sx, self._sy, self._alpha)(*self._project(self._lambda, self._phi))
        transform = scale_translate_rotate(self._k, self._x - center[0], self._y - center[1], self._sx, self._sy, self._alpha)
        self._rotate = RotateRadians(self._delta_gamma, self._delta_phi, self._delta_gamma)
        self._project_transform = Compose(self._project, transform)
        self._project_rotate_transform = Compose(self._rotate, self._project_transform)
        self._project_resample = resample(self._project_transform, self._delta2)
        return self.reset()

    def reset(self):
        self._cache = None
        self._cache_stream = None
        return self

    def get_preclip(self):
        return self._preclip

    def get_postclip(self):
        return self._postclip

    def get_clip_angle(self):
        return radians(self._theta)

    def get_clip_extent(self):
        if self._x0 is None:
            return None
        else:
            return [[self._x0, self._y0], [self._x1, self._y1]]

    def get_scale(self):
        return self._k

    def get_translation(self):
        return [self._x, self._y]

    def get_center(self):
        return [degrees(self._lambda), degrees(self._phi)]

    def get_rotation(self):
        return [degrees(self._delta_lambda), degrees(self._delta_phi), degrees(self._delta_gamma)]

    def get_angle(self):
        return degrees(self._alpha)

    def get_reflect_x(self):
        return self._sx < 0

    def get_reflect_y(self):
        return self._sy < 0

    def get_precision(self):
        return sqrt(self._delta2)


def projection(project):
    return ProjectionMutator(project).recenter()
