import io

from image_editor import app


def test_main_runs_menu_and_exits_cleanly(monkeypatch, samples_dir, tmp_path):
    monkeypatch.setattr("sys.stdin", io.StringIO("a.png\n0\n"))
    monkeypatch.chdir(samples_dir.parent)
    monkeypatch.setattr("image_editor.app.image_io.show", lambda arr: None)

    app.main()


def test_main_swallows_eof_error(monkeypatch, samples_dir):
    monkeypatch.setattr("sys.stdin", io.StringIO(""))
    monkeypatch.chdir(samples_dir.parent)

    app.main()
