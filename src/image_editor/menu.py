"""Terminal menu: prompts, validation and dispatch to operations/filters.

Terminal I/O and image display are injected (stdin/stdout streams, `show` callable)
so the whole flow is testable without a real terminal or an image viewer.
"""

from pathlib import Path

from image_editor import filters, image_io, operations

# Menu label -> KERNELS table name. Roberts (2x2) is not offered: convolve()
# only supports odd-sized kernels.
_FILTER_OPTIONS = [
    ("Gauss", "gauss"),
    ("Laplace", "laplaceEdge1"),
    ("Emboss", "emboss1"),
    ("Relief", "relief1"),
    ("Sobel", "sobel1"),
    ("Prewitt", "prewitt1"),
    ("Scharr", "scharr1"),
]


class Menu:
    def __init__(self, stdin, stdout, show, samples_dir=Path("samples"), result_dir=Path("result")):
        self.stdin = stdin
        self.stdout = stdout
        self._show = show
        self.samples_dir = samples_dir
        self.result_dir = result_dir

    def run(self):
        path = self._ask_sample("image")
        op = self._choose(
            "Image operations:", ["One image operations", "Two images operations"], allow_exit=True
        )

        if op == 0:
            return
        if op == 1:
            self._one_image(path)
        else:
            self._two_images(path)

    def _ask(self, prompt):
        self.stdout.write(prompt)
        self.stdout.flush()
        line = self.stdin.readline()
        if line == "":
            raise EOFError
        return line.rstrip("\n")

    def _ask_int(self, prompt, is_valid, retry_prompt):
        text = self._ask(prompt)
        while True:
            try:
                value = int(text)
                if is_valid(value):
                    return value
            except ValueError:
                # Narrow catch at the input-validation boundary (non-numeric text is an
                # expected user input, not an error to hide): this re-prompts exactly like
                # an invalid-but-numeric value does. Not the catch-all `except Exception`
                # the plan bans elsewhere, which swallowed real bugs alongside bad input.
                pass
            text = self._ask(retry_prompt)

    def _ask_float(self, prompt, is_valid, retry_prompt):
        text = self._ask(prompt)
        while True:
            try:
                value = float(text)
                if is_valid(value):
                    return value
            except ValueError:
                # See _ask_int: same narrow, intentional input-validation boundary.
                pass
            text = self._ask(retry_prompt)

    def _choose(self, title, options, allow_exit=False):
        self.stdout.write(title + "\n")
        for i, option in enumerate(options, start=1):
            self.stdout.write(f"{i} - {option}\n")
        if allow_exit:
            self.stdout.write("0 - Exit\n")

        low = 0 if allow_exit else 1
        return self._ask_int(
            "Type the corresponding operation number: ",
            lambda v: low <= v <= len(options),
            "Invalid operation, type again: ",
        )

    def _ask_sample(self, label):
        prompt = f"Enter {label} file name in {self.samples_dir.name} folder: "
        name = self._ask(prompt)
        while not (self.samples_dir / name).is_file():
            self.stdout.write("Invalid path, try again!\n\n")
            name = self._ask(prompt)
        return self.samples_dir / name

    def _finish(self, image_path, op_name, result):
        result_path = self.result_dir / f"{image_path.stem}-{op_name}{image_path.suffix}"
        image_io.save(result, result_path)
        self._show(result)
        self.stdout.write(f"Saved {result_path}\n")

    def _one_image(self, path):
        op = self._choose(
            "One image operations:", ["Constant operations", "Rotation", "Mirroring", "Filters"]
        )
        arr = image_io.load_rgb(path)

        if op == 1:
            self._constant(path, arr)
        elif op == 2:
            self._finish(path, "rotate", operations.rotate(arr))
        elif op == 3:
            axis = self._ask_int(
                "Type 0 to mirror around horizontal axis, 1 to mirror around vertical axis "
                "or 2 to mirror around color axis: ",
                lambda v: v in (0, 1, 2),
                "Invalid value, try again: ",
            )
            self._finish(path, "mirror", operations.mirror(arr, axis))
        elif op == 4:
            self._filters(path, arr)

    def _constant(self, path, arr):
        op = self._choose(
            "Constant image operations:", ["Brightness", "Contrast", "Negative", "Shades of gray"]
        )

        if op == 1:
            factor = self._ask_int(
                "Type a brightness factor between -255 and 255: ",
                lambda v: -255 <= v <= 255,
                "Invalid value, try again: ",
            )
            self._finish(path, "const-brightness", operations.brightness(arr, factor))
        elif op == 2:
            factor = self._ask_float(
                "Type a brightness factor between 0 and 100: ",
                lambda v: 0 <= v <= 100,
                "Invalid value, try again: ",
            )
            self._finish(path, "const-contrast", operations.contrast(arr, factor))
        elif op == 3:
            self._finish(path, "const-negative", operations.negative(arr))
        elif op == 4:
            self._finish(path, "const-mono", operations.grayscale(arr))

    def _filters(self, path, arr):
        options = [f"{label} filter" for label, _ in _FILTER_OPTIONS]
        op = self._choose("Filter image operations:", options)

        kernel_name = _FILTER_OPTIONS[op - 1][1]
        result = filters.convolve(arr, filters.KERNELS[kernel_name])
        self._finish(path, kernel_name, result)

    def _two_images(self, path):
        path2 = self._ask_sample("second image")
        arr1 = image_io.load_rgb(path)
        arr2 = image_io.load_rgb(path2)

        if arr1.shape != arr2.shape:
            self.stdout.write(
                f"Images must have the same dimensions ({arr1.shape} vs {arr2.shape})\n"
            )
            return

        op = self._choose(
            "Two image operations:",
            ["Sum", "Subtraction", "Multiplication", "Division", "3D Anaglyph"],
        )
        transparency_prompt = (
            "Type a transparency value to image 1 over image 2 between 0 and 100 "
            "(Type -1 to not apply transparency): "
        )

        if op == 1:
            weight = self._ask_int(
                transparency_prompt, lambda v: -1 <= v <= 100, "Invalid value, try again: "
            )
            self._finish(path, "images-sum", operations.add(arr1, arr2, weight))
        elif op == 2:
            weight = self._ask_int(
                transparency_prompt, lambda v: -1 <= v <= 100, "Invalid value, try again: "
            )
            self._finish(path, "images-sub", operations.subtract(arr1, arr2, weight))
        elif op == 3:
            self._finish(path, "images-mult", operations.multiply(arr1, arr2))
        elif op == 4:
            self._finish(path, "images-div", operations.divide(arr1, arr2))
        elif op == 5:
            self._finish(path, "images-3d", operations.anaglyph(arr1))
