# PyTermStylePlus: Elegant Terminal Styling for Python

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

PyTermStylePlus is a lightweight yet powerful Python library designed to bring vibrant colors, rich formatting, and consistent semantic styling to your terminal output. It provides a fluent, chainable API and a theme management system, making it easy to create beautiful and readable command-line interfaces and debug logs.

![Preview](https://github.com/Mohammedcha/PyTermStylePlus/raw/main/screen.png)

## Features

* **Fluent API:** Chain multiple styling methods intuitively (e.g., `style("text").red().bold().underline()`).

* **Semantic Styling:** Define and apply named styles (e.g., `error`, `success`, `info`) that adapt to chosen themes.

* **Theme Management:** Switch between predefined or custom themes to instantly change your application's visual identity.

* **Comprehensive Color Support:** Includes standard 8-bit ANSI colors, with options for 256-color and true-color (RGB) extensions.

* **Text Formatting:** Apply bold, italic, underline, strikethrough, and more.

* **Automatic ANSI Detection:** Gracefully degrades to unstyled text in terminals that don't support ANSI escape codes.

## Installation

You can install PyTermStylePlus directly from PyPI using pip:

```bash
pip install PyTermStylePlus
```

### Manual Installation (for development or specific use cases)

For manual installation or when developing the library:

1.  Download the `PyTermStylePlus.py` file.

2.  Place it in your Python project directory, or in a location included in your Python path.

## Quick Start

Here's a simple example of how to use PyTermStylePlus in your Python script:

```python
# my_app.py
from PyTermStylePlus import style, set_theme

# 1. Basic fluent API usage
print(style("Hello, colorful world!").green().bold())

# 2. Semantic styling with the default theme
print(style.info("Application starting..."))
print(style.success("Operation completed successfully."))

# 3. Switch to a different theme
set_theme("dark")
print(style.error("ERROR: Something critical occurred!"))

# 4. Use within f-strings
username = "DevUser"
action = "login attempt"
print(f"User: {style(username).cyan()} made a {style(action).orange().underline()}.")

# 5. Switch back
set_theme("default")
print(style.notice("Remember to check the logs for details."))
```

## Examples

A comprehensive example file, `examples.py`, demonstrates all available colors, background colors, text formats, chained styles, and semantic themes.

To run the examples:

1.  If running from the cloned repository, ensure `PyTermStylePlus.py` and `examples.py` are in the same directory (or `PyTermStylePlus.py` is in your Python path).

2.  Execute `examples.py` from your terminal:

    ```bash
    python examples.py
    ```

You will see various styled messages, demonstrating:

* All foreground and background colors.

* All text formatting options (bold, underline, italic, etc.).

* Combinations of styles.

* Semantic styles (e.g., `error`, `success`, `info`, `notice`, `emphasis`, `status_ok`)

    * These will appear differently when the theme is switched from `default` to `dark`.

* Graceful degradation behavior in simulated "dumb" terminals.

## API Reference

### `style(text: str) -> TermStyle`

The main entry point for the fluent API. Call `style()` with your text to start chaining styling methods.

```python
print(style("My text").red().bold().underline())
```

### `style.semantic_name(text: str) -> TermStyle`

Applies a predefined semantic style based on the currently active theme.

**Available Semantic Styles:**

* `style.error(text)`

* `style.success(text)`

* `style.info(text)`

* `style.warning(text)`

* `style.highlight(text)`

* `style.primary(text)`

* `style.secondary(text)`

* `style.notice(text)`

* `style.emphasis(text)`

* `style.status_ok(text)`

### `set_theme(theme_name: str)`

Changes the active theme for all subsequent semantic styling calls.

**Available Themes:** `"default"`, `"dark"`

```python
from PyTermStylePlus import set_theme

set_theme("dark") # All semantic styles will now use the 'dark' theme definitions
print(style.info("This is now dark theme info."))
```

### Available Basic Styling Methods

These methods are chained onto `style(text)`:

**Foreground Colors:**
`red()`, `green()`, `blue()`, `yellow()`, `white()`, `black()`, `cyan()`, `magenta()`, `light_grey()`, `dark_grey()`, `orange()`, `purple()`, `teal()`, `olive()`

**Background Colors:**
`bg_red()`, `bg_green()`, `bg_blue()`, `bg_yellow()`, `bg_white()`, `bg_black()`, `bg_cyan()`, `bg_magenta()`, `bg_light_grey()`, `bg_dark_grey()`, `bg_orange()`, `bg_purple()`, `bg_teal()`, `bg_olive()`

**Text Formats:**
`bold()`, `faint()`, `italic()`, `underline()`, `blink()`, `reverse()`, `concealed()`, `strikethrough()`

## Terminal Compatibility

PyTermStylePlus automatically checks if your terminal environment supports ANSI escape codes. If support is not detected (e.g., `TERM=dumb`, or older Windows consoles), styling will be automatically disabled to prevent garbled output. This ensures your application remains readable across various terminal environments.

For Windows users, PyTermStylePlus attempts to enable ANSI support using `os.system('')` on initialization, which is often sufficient for modern terminals like Windows Terminal, PowerShell, or VS Code's integrated terminal.

## Contributing

Contributions are welcome! If you have ideas for new features, bug fixes, or improvements to existing styles/themes, please feel free to:

1.  Fork the repository at `https://github.com/Mohammedcha/PyTermStylePlus`.

2.  Create a new branch (`git checkout -b feature/your-feature`).

3.  Make your changes.

4.  Commit your changes (`git commit -am 'Add new feature'`).

5.  Push to the branch (`git push origin feature/your-feature`).

6.  Create a new Pull Request.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
