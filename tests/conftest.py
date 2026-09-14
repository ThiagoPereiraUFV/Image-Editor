import io

import numpy as np
import pytest
from PIL import Image


@pytest.fixture
def rgb_4x4():
    """Deterministic 4x4 RGB array; values 0..47 so every op has distinct inputs."""
    return np.arange(4 * 4 * 3, dtype=np.uint8).reshape(4, 4, 3)


@pytest.fixture
def samples_dir(tmp_path):
    """Populate a samples directory with the fixture images the menu/app tests load from disk."""
    directory = tmp_path / "samples"
    directory.mkdir()

    a = np.arange(4 * 4 * 3, dtype=np.uint8).reshape(4, 4, 3)
    Image.fromarray(a).save(directory / "a.png")

    b = (255 - a).astype(np.uint8)
    Image.fromarray(b).save(directory / "b.png")

    gray = np.arange(4 * 4, dtype=np.uint8).reshape(4, 4)
    Image.fromarray(gray, mode="L").save(directory / "gray.png")

    other = np.zeros((2, 2, 3), dtype=np.uint8)
    Image.fromarray(other).save(directory / "other.png")

    return directory


@pytest.fixture
def make_menu(tmp_path):
    """Build a Menu on an in-memory script, capturing stdout and each image passed to `show`."""
    from image_editor.menu import Menu

    def _make(samples_dir, script):
        stdin = io.StringIO("\n".join(script) + "\n")
        stdout = io.StringIO()
        shown = []
        result_dir = tmp_path / "result"
        menu = Menu(stdin, stdout, shown.append, samples_dir=samples_dir, result_dir=result_dir)
        return menu, stdout, shown

    return _make
