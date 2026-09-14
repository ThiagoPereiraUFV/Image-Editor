import numpy as np
from PIL import Image

from image_editor import image_io


def test_save_then_load_round_trip(tmp_path):
    arr = np.arange(4 * 4 * 3, dtype=np.uint8).reshape(4, 4, 3)
    path = tmp_path / "out.png"

    image_io.save(arr, path)
    loaded = image_io.load_rgb(path)

    assert loaded.tolist() == arr.tolist()


def test_load_rgb_converts_grayscale_to_hxwx3(tmp_path):
    gray = np.arange(4 * 4, dtype=np.uint8).reshape(4, 4)
    path = tmp_path / "gray.png"
    Image.fromarray(gray, mode="L").save(path)

    loaded = image_io.load_rgb(path)

    assert loaded.shape == (4, 4, 3)


def test_save_creates_missing_parent_dirs(tmp_path):
    arr = np.zeros((2, 2, 3), dtype=np.uint8)
    path = tmp_path / "nested" / "dir" / "out.png"

    image_io.save(arr, path)

    assert path.is_file()


def test_show_calls_pil_image_show(monkeypatch):
    calls = []
    monkeypatch.setattr(Image.Image, "show", lambda self: calls.append(self))

    arr = np.zeros((2, 2, 3), dtype=np.uint8)
    image_io.show(arr)

    assert len(calls) == 1
