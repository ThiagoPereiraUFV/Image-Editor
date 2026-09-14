"""3x3 (and larger) convolution kernels and the convolution operation itself."""

import numpy as np

KERNELS = {
    "gauss": [[1 / 16, 1 / 8, 1 / 16], [1 / 8, 1 / 4, 1 / 8], [1 / 16, 1 / 8, 1 / 16]],
    "laplaceSmooth1": [[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]],
    "laplaceSmooth2": [[0, 1, 0], [1, -4, 1], [0, 1, 0]],
    "laplaceEdge1": [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]],
    "laplaceEdge2": [[0, -1, 0], [-1, 4, -1], [0, -1, 0]],
    "emboss1": [[-1, -1, 0], [-1, 1, 1], [0, 1, 1]],
    "emboss2": [[1, 1, 0], [1, 1, -1], [0, -1, -1]],
    "embossEdge": [[-1, -1, 0], [-1, 0, 1], [0, 1, 1]],
    "relief1": [[-2, -1, 0], [-1, 1, 1], [0, 1, 2]],
    "relief2": [[2, 1, 0], [1, 1, -1], [0, -1, -2]],
    "reliefEdge": [[-2, -1, 0], [-1, 0, 1], [0, 1, 2]],
    "sobel1": [[-1, -2, -1], [0, 0, 0], [1, 2, 1]],
    "sobel2": [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]],
    "prewitt1": [[1, 0, -1], [1, 0, -1], [1, 0, -1]],
    "prewitt2": [[1, 1, 1], [0, 0, 0], [-1, -1, -1]],
    "scharr1": [[3, 10, 3], [0, 0, 0], [-3, -10, -3]],
    "scharr2": [[3, 0, -3], [10, 0, -10], [3, 0, -3]],
    "roberts1": [[1, 0], [0, -1]],
    "roberts2": [[0, 1], [-1, 0]],
}


def gaussian_kernel(size, sigma):
    if size % 2 == 0:
        raise ValueError("kernel size must be odd")

    x = np.arange(-(size - 1) / 2, (size - 1) / 2 + 1)
    h1, h2 = np.meshgrid(x, x)
    hg = np.exp(-(h1**2 + h2**2) / (2 * sigma**2))

    return hg / np.sum(hg)


def convolve(arr, kernel):
    """Convolve an HxWx3 uint8 array; pixels without a full neighbourhood keep the input value."""
    kernel = np.asarray(kernel, dtype=float)
    size = kernel.shape[0]
    if size % 2 == 0:
        raise ValueError("kernel size must be odd")  # symmetric border needs size//2 on each side

    half = size // 2
    height, width = arr.shape[:2]

    result = arr.astype(float).copy()

    windows = np.lib.stride_tricks.sliding_window_view(arr, kernel.shape, axis=(0, 1))
    convolved = np.einsum("ijckl,kl->ijc", windows.astype(float), kernel)
    result[half : height - half, half : width - half] = convolved

    return np.clip(np.round(result), 0, 255).astype(np.uint8)
