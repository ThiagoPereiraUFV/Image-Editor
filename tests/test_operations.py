import numpy as np

from image_editor import operations


def _rgb(*rows):
    """Build a uint8 HxWx3 array from a list of rows of (r, g, b) pixels."""
    return np.array(rows, dtype=np.uint8)


def test_brightness_adds_and_clips_high():
    arr = _rgb([[10, 250, 0]])
    result = operations.brightness(arr, 10)
    assert result.tolist() == [[[20, 255, 10]]]


def test_brightness_clips_low():
    arr = _rgb([[10, 0, 5]])
    result = operations.brightness(arr, -20)
    assert result.tolist() == [[[0, 0, 0]]]


def test_contrast_multiplies_and_rounds():
    arr = _rgb([[10, 20, 100]])
    result = operations.contrast(arr, 1.5)
    assert result.tolist() == [[[15, 30, 150]]]


def test_contrast_clips_at_255():
    arr = _rgb([[200, 0, 0]])
    result = operations.contrast(arr, 100.0)
    assert result.tolist() == [[[255, 0, 0]]]


def test_negative():
    arr = _rgb([[0, 100, 255]])
    result = operations.negative(arr)
    assert result.tolist() == [[[255, 155, 0]]]


def test_grayscale_truncates():
    # 0.299*100 = 29.9 -> truncated to 29, not rounded to 30.
    arr = _rgb([[100, 0, 0]])
    result = operations.grayscale(arr)
    assert result.dtype == np.uint8
    assert result.tolist() == [[29]]


def test_grayscale_shape_is_2d():
    arr = _rgb([[10, 20, 30]], [[40, 50, 60]])
    result = operations.grayscale(arr)
    assert result.shape == (2, 1)


def test_rotate():
    arr = np.arange(4 * 3, dtype=np.uint8).reshape(2, 2, 3)
    result = operations.rotate(arr)
    assert result.tolist() == np.rot90(arr, 1).tolist()


def test_mirror_axis0():
    arr = _rgb([[1, 1, 1]], [[2, 2, 2]])
    result = operations.mirror(arr, 0)
    assert result.tolist() == [[[2, 2, 2]], [[1, 1, 1]]]


def test_mirror_axis1():
    arr = _rgb([[1, 1, 1], [2, 2, 2]])
    result = operations.mirror(arr, 1)
    assert result.tolist() == [[[2, 2, 2], [1, 1, 1]]]


def test_mirror_axis2_reverses_channels():
    arr = _rgb([[10, 20, 30]])
    result = operations.mirror(arr, 2)
    assert result.tolist() == [[[30, 20, 10]]]


def test_add_plain_when_weight_out_of_range():
    a = _rgb([[100, 100, 100]])
    b = _rgb([[50, 50, 50]])
    result = operations.add(a, b, -1)
    assert result.tolist() == [[[150, 150, 150]]]


def test_add_clips_at_255():
    a = _rgb([[200, 200, 200]])
    b = _rgb([[200, 200, 200]])
    result = operations.add(a, b, -1)
    assert result.tolist() == [[[255, 255, 255]]]


def test_add_blends_with_weight():
    a = _rgb([[100, 0, 0]])
    b = _rgb([[0, 100, 0]])
    result = operations.add(a, b, 50)
    # 0.5*100 + 0.5*0 = 50; 0.5*0 + 0.5*100 = 50
    assert result.tolist() == [[[50, 50, 0]]]


def test_add_weight_over_100_is_plain():
    a = _rgb([[10, 10, 10]])
    b = _rgb([[5, 5, 5]])
    result = operations.add(a, b, 150)
    assert result.tolist() == [[[15, 15, 15]]]


def test_subtract_plain_when_weight_out_of_range():
    a = _rgb([[100, 100, 100]])
    b = _rgb([[30, 30, 30]])
    result = operations.subtract(a, b, -1)
    assert result.tolist() == [[[70, 70, 70]]]


def test_subtract_clips_below_zero():
    a = _rgb([[10, 10, 10]])
    b = _rgb([[50, 50, 50]])
    result = operations.subtract(a, b, -1)
    assert result.tolist() == [[[0, 0, 0]]]


def test_subtract_blends_with_weight():
    a = _rgb([[100, 100, 100]])
    b = _rgb([[0, 0, 0]])
    result = operations.subtract(a, b, 50)
    # 0.5*100 - 0.5*0 = 50
    assert result.tolist() == [[[50, 50, 50]]]


def test_multiply():
    a = _rgb([[100, 100, 100]])
    b = _rgb([[128, 128, 128]])
    result = operations.multiply(a, b)
    # 100 * (128/255) = 50.196... -> round -> 50
    assert result.tolist() == [[[50, 50, 50]]]


def test_multiply_clips_at_255():
    a = _rgb([[255, 255, 255]])
    b = _rgb([[255, 255, 255]])
    result = operations.multiply(a, b)
    assert result.tolist() == [[[255, 255, 255]]]


def test_divide_by_zero_is_255():
    a = _rgb([[10, 10, 10]])
    b = _rgb([[0, 0, 0]])
    result = operations.divide(a, b)
    assert result.tolist() == [[[255, 255, 255]]]


def test_divide_zero_by_zero_is_255():
    a = _rgb([[0, 0, 0]])
    b = _rgb([[0, 0, 0]])
    result = operations.divide(a, b)
    assert result.tolist() == [[[255, 255, 255]]]


def test_divide_clips_at_255():
    a = _rgb([[255, 255, 255]])
    b = _rgb([[1, 1, 1]])
    result = operations.divide(a, b)
    assert result.tolist() == [[[255, 255, 255]]]


def test_divide_normal_case():
    a = _rgb([[128, 128, 128]])
    b = _rgb([[255, 255, 255]])
    result = operations.divide(a, b)
    # 128 / (255/255) = 128
    assert result.tolist() == [[[128, 128, 128]]]


def test_anaglyph_no_shift_below_width_500():
    arr = np.zeros((1, 4, 3), dtype=np.uint8)
    arr[0, 1] = [10, 20, 30]
    result = operations.anaglyph(arr)
    # width*0.002 truncates to 0 below width 500, so no roll happens.
    assert result.shape == arr.shape

    f = arr.copy().astype(int)
    f[:, :, 1] = 0
    f[:, :, 2] = 0
    g = arr.copy().astype(int)
    g[:, :, 0] = 0
    expected = np.clip(f + g, 0, 255).astype(np.uint8)
    assert result.tolist() == expected.tolist()


def test_anaglyph_shifts_on_wide_image():
    arr = np.zeros((1, 1000, 3), dtype=np.uint8)
    arr[0, 500] = [10, 20, 30]
    result = operations.anaglyph(arr)

    disp = int(arr.shape[1] * 0.002)
    assert disp == 2

    f = arr.copy().astype(int)
    f[:, :, 1] = 0
    f[:, :, 2] = 0
    g = arr.copy().astype(int)
    g[:, :, 0] = 0
    f = np.roll(f, disp, axis=1)
    g = np.roll(g, -disp, axis=1)
    expected = np.clip(f + g, 0, 255).astype(np.uint8)
    assert result.tolist() == expected.tolist()
