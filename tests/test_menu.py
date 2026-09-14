import io

import pytest

from image_editor.menu import Menu

LEAF_CASES = [
    # (script, expected_result_name)
    (["a.png", "1", "1", "1", "10"], "a-const-brightness.png"),
    (["a.png", "1", "1", "2", "1.5"], "a-const-contrast.png"),
    (["a.png", "1", "1", "3"], "a-const-negative.png"),
    (["a.png", "1", "1", "4"], "a-const-mono.png"),
    (["a.png", "1", "2"], "a-rotate.png"),
    (["a.png", "1", "3", "0"], "a-mirror.png"),
    (["a.png", "2", "b.png", "1", "50"], "a-images-sum.png"),
    (["a.png", "2", "b.png", "2", "50"], "a-images-sub.png"),
    (["a.png", "2", "b.png", "3"], "a-images-mult.png"),
    (["a.png", "2", "b.png", "4"], "a-images-div.png"),
    (["a.png", "2", "b.png", "5"], "a-images-3d.png"),
    (["a.png", "1", "4", "1"], "a-gauss.png"),
    (["a.png", "1", "4", "2"], "a-laplaceEdge1.png"),
    (["a.png", "1", "4", "3"], "a-emboss1.png"),
    (["a.png", "1", "4", "4"], "a-relief1.png"),
    (["a.png", "1", "4", "5"], "a-sobel1.png"),
    (["a.png", "1", "4", "6"], "a-prewitt1.png"),
    (["a.png", "1", "4", "7"], "a-scharr1.png"),
]


@pytest.mark.parametrize("script,expected_name", LEAF_CASES)
def test_menu_leaf_produces_expected_result(make_menu, samples_dir, script, expected_name):
    menu, out, shown = make_menu(samples_dir, script)
    menu.run()

    result_path = menu.result_dir / expected_name
    assert result_path.is_file()
    assert len(shown) == 1
    assert f"Saved {result_path}" in out.getvalue()


def test_invalid_image_name_then_valid(make_menu, samples_dir):
    menu, out, shown = make_menu(samples_dir, ["nope.png", "a.png", "1", "2"])
    menu.run()

    assert "Invalid path, try again!" in out.getvalue()
    assert (menu.result_dir / "a-rotate.png").is_file()


def test_non_numeric_menu_choice_reprompts(make_menu, samples_dir):
    menu, out, shown = make_menu(samples_dir, ["a.png", "abc", "1", "2"])
    menu.run()

    assert "Invalid operation, type again: " in out.getvalue()
    assert (menu.result_dir / "a-rotate.png").is_file()


def test_out_of_range_menu_choice_reprompts(make_menu, samples_dir):
    menu, out, shown = make_menu(samples_dir, ["a.png", "9", "1", "2"])
    menu.run()

    assert "Invalid operation, type again: " in out.getvalue()
    assert (menu.result_dir / "a-rotate.png").is_file()


def test_brightness_out_of_range_reprompts(make_menu, samples_dir):
    menu, out, shown = make_menu(samples_dir, ["a.png", "1", "1", "1", "999", "10"])
    menu.run()

    assert "Invalid value, try again: " in out.getvalue()
    assert (menu.result_dir / "a-const-brightness.png").is_file()


def test_contrast_non_numeric_reprompts(make_menu, samples_dir):
    menu, out, shown = make_menu(samples_dir, ["a.png", "1", "1", "2", "abc", "1.5"])
    menu.run()

    assert "Invalid value, try again: " in out.getvalue()
    assert (menu.result_dir / "a-const-contrast.png").is_file()


def test_mirror_axis_out_of_range_reprompts(make_menu, samples_dir):
    menu, out, shown = make_menu(samples_dir, ["a.png", "1", "3", "5", "0"])
    menu.run()

    assert "Invalid value, try again: " in out.getvalue()
    assert (menu.result_dir / "a-mirror.png").is_file()


def test_transparency_minus_one_is_plain_sum(make_menu, samples_dir):
    menu, out, shown = make_menu(samples_dir, ["a.png", "2", "b.png", "1", "-1"])
    menu.run()

    assert (menu.result_dir / "a-images-sum.png").is_file()


def test_exit_with_zero_produces_no_result(make_menu, samples_dir):
    menu, out, shown = make_menu(samples_dir, ["a.png", "0"])
    menu.run()

    assert not menu.result_dir.exists() or not any(menu.result_dir.iterdir())
    assert "Saved" not in out.getvalue()


def test_size_mismatch_writes_message_and_returns(make_menu, samples_dir):
    menu, out, shown = make_menu(samples_dir, ["a.png", "2", "other.png"])
    menu.run()

    assert "Images must have the same dimensions" in out.getvalue()
    assert shown == []


def test_gray_sample_loads_as_rgb(make_menu, samples_dir):
    menu, out, shown = make_menu(samples_dir, ["gray.png", "1", "2"])
    menu.run()

    assert (menu.result_dir / "gray-rotate.png").is_file()


def test_eof_error_propagates(tmp_path, samples_dir):
    menu = Menu(
        io.StringIO(""),
        io.StringIO(),
        lambda arr: None,
        samples_dir=samples_dir,
        result_dir=tmp_path / "result",
    )

    with pytest.raises(EOFError):
        menu.run()
