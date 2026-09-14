"""Pure numpy point/geometry/two-image operations. No Pillow, no I/O."""

import numpy as np

LMAX = 255


def brightness(arr, factor):
    f = arr.astype(int) + int(factor)
    return np.clip(f, 0, LMAX).astype(np.uint8)


def contrast(arr, factor):
    f = arr.astype(float) * float(factor)
    return np.clip(np.round(f), 0, LMAX).astype(np.uint8)


def negative(arr):
    return (LMAX - arr.astype(int)).astype(np.uint8)


def grayscale(arr):
    f = arr.astype(float)
    gray = 0.299 * f[:, :, 0] + 0.587 * f[:, :, 1] + 0.114 * f[:, :, 2]
    return np.uint8(gray)  # truncates, matching the original tool's rule


def rotate(arr):
    return np.rot90(arr, 1)


def mirror(arr, axis):
    return np.flip(arr, axis=axis)


def _blend(a, b, weight):
    """Weighted blend when weight is in [0, 100]; plain otherwise (transparency disabled)."""
    if 0 <= weight <= 100:
        w = weight / 100
        return w * a.astype(float), (1 - w) * b.astype(float)
    return a.astype(float), b.astype(float)


def add(a, b, weight):
    fa, fb = _blend(a, b, weight)
    result = fa + fb
    return np.clip(np.round(result), 0, LMAX).astype(np.uint8)


def subtract(a, b, weight):
    fa, fb = _blend(a, b, weight)
    result = fa - fb
    return np.clip(np.round(result), 0, LMAX).astype(np.uint8)


def multiply(a, b):
    f = a.astype(float) * (b.astype(float) / LMAX)
    return np.clip(np.round(f), 0, LMAX).astype(np.uint8)


def divide(a, b):
    with np.errstate(divide="ignore", invalid="ignore"):
        f = a.astype(float) / (b.astype(float) / LMAX)
    f[np.isnan(f)] = LMAX  # 0/0 is defined as full brightness (original rule)
    return np.clip(np.round(f), 0, LMAX).astype(np.uint8)


def anaglyph(arr):
    disp = int(arr.shape[1] * 0.002)

    f = arr.astype(int).copy()
    f[:, :, 1] = 0
    f[:, :, 2] = 0

    g = arr.astype(int).copy()
    g[:, :, 0] = 0

    f = np.roll(f, disp, axis=1)
    g = np.roll(g, -disp, axis=1)

    return np.clip(f + g, 0, LMAX).astype(np.uint8)
