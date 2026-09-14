<h1 align="center">
	Image Editor v1.0
</h1>

<h4 align="center">
	:hammer: Thiago Marinho Pereira
</h4>

<p align="center">
<img alt="GitHub language count" src="https://img.shields.io/github/languages/count/ThiagoPereiraUFV/Image-Editor">

<img alt="Repository size" src="https://img.shields.io/github/repo-size/ThiagoPereiraUFV/Image-Editor">

<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/ThiagoPereiraUFV/Image-Editor">

<img alt="License" src="https://img.shields.io/badge/license-MIT-brightgreen">
</p>

<p align="center">
	<a href="#rocket-technologies">Technologies</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
	<a href="#computer-project">Project</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
	<a href="#wrench-installation">Installation</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
	<a href="#memo-license">License</a>
</p>

<br>

## :rocket: Technologies

This project was built using following technologies:

- [Python](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/)
- [Pillow](https://python-pillow.org/)
- [NumPy](https://numpy.org/)
- [pytest](https://docs.pytest.org/)
- [Ruff](https://docs.astral.sh/ruff/)

## :computer: Project

*Image Editor is an interactive terminal program that loads a PNG image from the `samples/` folder and applies a chosen effect, saving the result to `result/` and opening it in the system's default image viewer. It supports:*

- *One-image constant operations: brightness, contrast, negative and grayscale ("shades of gray").*
- *Rotation (90 degrees) and mirroring (horizontal, vertical or color-channel axis).*
- *3x3 convolution filters: Gauss, Laplace, Emboss, Relief, Sobel, Prewitt and Scharr.*
- *Two-image operations: sum and subtraction (both with an optional transparency weight), multiplication, division and a 3D anaglyph effect.*

*Two notes on behaviour: the 2x2 Roberts kernel is not offered in the filters menu (the convolution only supports odd-sized, symmetric-border kernels), and the 3D Anaglyph effect uses only the first selected image, even though it lives in the two-image menu — both are pre-existing, deliberately kept quirks of the original implementation.*

## :wrench: Installation

__This project uses [uv](https://docs.astral.sh/uv/) to manage its Python version and dependencies. Execute the following command to install them:__

```bash
$ uv sync
```

__Execute the following command to run the editor on your Terminal:__

```bash
$ make run
```

__Execute the following command to check linting and formatting:__

```bash
$ make lint
```

__Execute the following command to apply the lint fixes and formatting:__

```bash
$ make format
```

__Execute the following command to run the automated tests:__

```bash
$ make test
```

__Execute the following command to run the tests and generate an HTML coverage report (written to `htmlcov/`):__

```bash
$ make coverage
```

## :memo: License

This project is under MIT License. Check out [LICENSE](LICENSE) file to more details.

---

<p align="center">
	Built with :hearts: by <a href="https://github.com/ThiagoPereiraUFV" target="_blank">Thiago Pereira</a>
</p>
