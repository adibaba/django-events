# Code - Documentation - Django Event Management

Contents:

- [Code formatting](#code-formatting)
- [IDEs](#ides)

## Code formatting

- Since Django 4.1, black is used to format code, see: <https://docs.djangoproject.com/en/4.2/ref/django-admin/#black-formatting>
- This project should be configured to use a maximum line length of 120.

### pre-commit

- "A framework for managing and maintaining multi-language pre-commit hooks"
- **Configuration file: [.pre-commit-config.yaml](../.pre-commit-config.yaml)**
- Website: <https://pre-commit.com/>
  - Supported hooks: <https://pre-commit.com/hooks.html>
    - <https://github.com/psf/black>
    - <https://github.com/PyCQA/flake8>

### Black

- "The uncompromising code formatter"
- Website: <https://black.readthedocs.io/en/stable/>
  - Using Black with other tools: [Flake8](https://black.readthedocs.io/en/stable/guides/using_black_with_other_tools.html#flake8)
    - Set flake8 config: `max-line-length = XYZ`
    - Set flake8 config: `extend-ignore = E203`
  - Line length: [Flake8](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html#flake8)
    - Set flake8 config: `max-line-length = XYZ`
    - Set flake8 config: `extend-ignore = E203, E704`
  
### Flake8

- "Your Tool For Style Guide Enforcement"
- "A wrapper around these tools: PyFlakes, pycodestyle, Ned Batchelder's McCabe script"
- **Configuration file: [.flake8](../.flake8)**
- Website: <https://flake8.pycqa.org/en/stable/>
  - [Usage with the pre-commit git hooks framework](https://flake8.pycqa.org/en/stable/user/using-hooks.html#usage-with-the-pre-commit-git-hooks-framework)
    - [Error / Violation Codes](https://flake8.pycqa.org/en/stable/user/error-codes.html) (codes starting with F)

### pycodestyle

- "Python style guide checker"
- Website: <https://pycodestyle.pycqa.org/en/stable/>
  - [Error codes](https://pycodestyle.pycqa.org/en/stable/intro.html#error-codes) (codes starting with E and W)
    - *E203* whitespace before ‘,’, ‘;’, or ‘:’
    - *E704* multiple statements on one line (def)
    - *W503* line break before binary operator

## IDEs

### Visual Studio Code

- Website: <https://code.visualstudio.com/>
  - Extension [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
  - Extension [Django Template Support](https://marketplace.visualstudio.com/items?itemName=junstyle.vscode-django-support)
- Intro: <https://code.visualstudio.com/docs/python/tutorial-django>
- Configuration file (`.vscode/settings.json`)

```json
{
    // https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true
    },
    "black-formatter.args": [
        "--line-length=120"
    ],
}
```
