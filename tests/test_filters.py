import numpy as np
import pytest

from image_editor import filters


def test_kernels_has_19_entries():
    assert len(filters.KERNELS) == 19


def test_kernels_all_odd_square_except_roberts():
    roberts = {"roberts1", "roberts2"}
    for name, kernel in filters.KERNELS.items():
        kernel = np.asarray(kernel)
        if name in roberts:
            assert kernel.shape == (2, 2)
        else:
            assert kernel.shape[0] == kernel.shape[1]
            assert kernel.shape[0] % 2 == 1


def test_gauss_custom_not_in_table():
    assert "gaussCustom" not in filters.KERNELS


def test_gaussian_kernel_sums_to_one_and_symmetric():
    kernel = filters.gaussian_kernel(3, 1)
    assert kernel.shape == (3, 3)
    assert np.isclose(kernel.sum(), 1)
    assert np.allclose(kernel, kernel.T)


def test_gaussian_kernel_even_size_raises():
    with pytest.raises(ValueError, match="kernel size must be odd"):
        filters.gaussian_kernel(4, 1)


def test_convolve_identity_kernel_returns_input():
    arr = np.arange(3 * 3 * 3, dtype=np.uint8).reshape(3, 3, 3)
    identity = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=float)
    result = filters.convolve(arr, identity)
    assert result.tolist() == arr.tolist()


def test_convolve_mean_kernel_changes_only_centre():
    arr = np.array(
        [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [90, 90, 90], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        ],
        dtype=np.uint8,
    )
    mean = np.full((3, 3), 1 / 9, dtype=float)
    result = filters.convolve(arr, mean)

    # only the centre pixel has a full 3x3 neighbourhood; borders keep the input.
    assert result[1, 1].tolist() == [10, 10, 10]
    for y in range(3):
        for x in range(3):
            if (y, x) != (1, 1):
                assert result[y, x].tolist() == arr[y, x].tolist()


def test_convolve_5x5_kernel_border_rule():
    arr = np.arange(5 * 5 * 3, dtype=np.uint8).reshape(5, 5, 3)
    kernel = np.zeros((5, 5), dtype=float)
    kernel[2, 2] = 1
    result = filters.convolve(arr, kernel)

    # only the centre pixel (2,2) has a full 5x5 neighbourhood inside a 5x5 image.
    assert result[2, 2].tolist() == arr[2, 2].tolist()
    border_mask = np.ones((5, 5), dtype=bool)
    border_mask[2, 2] = False
    assert result[border_mask].tolist() == arr[border_mask].tolist()


def test_convolve_even_kernel_raises():
    arr = np.zeros((3, 3, 3), dtype=np.uint8)
    kernel = np.zeros((2, 2), dtype=float)
    with pytest.raises(ValueError, match="kernel size must be odd"):
        filters.convolve(arr, kernel)


def test_convolve_clips_and_rounds():
    arr = np.full((3, 3, 3), 200, dtype=np.uint8)
    kernel = np.full((3, 3), 1.0, dtype=float)  # sums to 9, will overflow past 255
    result = filters.convolve(arr, kernel)
    assert result[1, 1].tolist() == [255, 255, 255]
