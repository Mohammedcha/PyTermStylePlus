"""
PyTermStylePlus: A Python library for elegant terminal text styling.

This library provides a fluent API for applying ANSI escape codes to strings,
enabling rich terminal output with colors, background colors, and text formatting
(bold, underline, italic, etc.). It also includes a theme management system
for semantic styling, allowing developers to define and apply consistent
visual styles (e.g., 'error', 'success', 'info') across their applications.

Features:
- Fluent, chainable API for applying styles.
- Support for common ANSI foreground and background colors.
- Support for various text formats (bold, underline, italic, strikethrough).
- Configurable themes for semantic styling.
- Automatic detection and graceful degradation for terminals that don't support ANSI.
"""

import os
import sys

class TermStyle:
    """
    Core class for applying ANSI escape codes to strings to style terminal output.
    Provides a fluent API for chaining style methods and supports semantic styling
    based on predefined themes.
    """

    _ANSI_RESET = "\033[0m"

    _COLORS = {
        "red": "\033[91m",
        "green": "\033[92m",
        "blue": "\033[94m",
        "yellow": "\033[93m",
        "white": "\033[97m",
        "black": "\033[30m",
        "cyan": "\033[96m",
        "magenta": "\033[95m",
        "light_grey": "\033[37m",
        "dark_grey": "\033[90m",
        "orange": "\033[38;5;208m",
        "purple": "\033[95m",
        "teal": "\033[38;5;38m",
        "olive": "\033[38;5;107m",
    }

    _BG_COLORS = {
        "bg_red": "\033[101m",
        "bg_green": "\033[102m",
        "bg_blue": "\033[104m",
        "bg_yellow": "\033[103m",
        "bg_white": "\033[107m",
        "bg_black": "\033[40m",
        "bg_cyan": "\033[106m",
        "bg_magenta": "\033[105m",
        "bg_light_grey": "\033[47m",
        "bg_dark_grey": "\033[100m",
        "bg_orange": "\033[48;5;208m",
        "bg_purple": "\033[48;5;129m",
        "bg_teal": "\033[48;5;38m",
        "bg_olive": "\033[48;5;107m",
    }

    _FORMATS = {
        "bold": "\033[1m",
        "faint": "\033[2m",
        "italic": "\033[3m",
        "underline": "\033[4m",
        "blink": "\033[5m",
        "reverse": "\033[7m",
        "concealed": "\033[8m",
        "strikethrough": "\033[9m",
    }

    _GLOBAL_ANSI_SUPPORTED = False

    def __init__(self, text=""):
        """
        Initializes the TermStyle instance with the text to be styled.
        """
        self._text = str(text)
        self._applied_codes = []
        self._disable_styling = not TermStyle._GLOBAL_ANSI_SUPPORTED

    @staticmethod
    def _initialize_ansi_support_check():
        """
        Performs a one-time check for ANSI support and enables it if possible.
        """
        if not sys.stdout.isatty():
            TermStyle._GLOBAL_ANSI_SUPPORTED = False
            return

        if os.name == 'nt':
            try:
                os.system('')
                TermStyle._GLOBAL_ANSI_SUPPORTED = True
                return
            except OSError:
                TermStyle._GLOBAL_ANSI_SUPPORTED = False
                return
        
        TermStyle._GLOBAL_ANSI_SUPPORTED = os.getenv('TERM') != 'dumb'

    def _apply_code(self, code):
        """
        Appends an ANSI escape code to the list of applied codes.
        Returns `self` for fluent chaining.
        """
        if self._disable_styling:
            return self
        self._applied_codes.append(code)
        return self

    for color_name, color_code in _COLORS.items():
        exec(f"def {color_name}(self): return self._apply_code(self._COLORS['{color_name}'])")
    
    for bg_color_name, bg_color_code in _BG_COLORS.items():
        exec(f"def {bg_color_name}(self): return self._apply_code(self._BG_COLORS['{bg_color_name}'])")

    for format_name, format_code in _FORMATS.items():
        exec(f"def {format_name}(self): return self._apply_code(self._FORMATS['{format_name}'])")

    def render(self):
        """
        Renders the text with all applied ANSI escape codes and resets the style.
        """
        if self._disable_styling:
            return self._text
        return "".join(self._applied_codes) + self._text + self._ANSI_RESET

    def __str__(self):
        """
        Allows the TermStyle object to be printed directly or used in f-strings,
        automatically calling `render()`.
        """
        return self.render()

TermStyle._initialize_ansi_support_check()

THEMES = {
    "default": {
        "semantic": {
            "error": ["red", "bold"],
            "success": ["green", "bold"],
            "info": ["blue"],
            "warning": ["yellow", "underline"],
            "highlight": ["bg_blue", "white"],
            "primary": ["cyan"],
            "secondary": ["dark_grey"],
            "notice": ["orange", "bold"],
            "emphasis": ["purple", "underline"],
            "status_ok": ["teal"],
        }
    },
    "dark": {
        "semantic": {
            "error": ["bg_red", "white", "bold"],
            "success": ["bg_green", "black"],
            "info": ["light_grey"],
            "warning": ["bg_yellow", "black", "bold"],
            "highlight": ["bg_dark_grey", "white"], 
            "primary": ["white", "bold"],
            "secondary": ["light_grey", "faint"],
            "notice": ["bg_orange", "black", "bold"],
            "emphasis": ["bg_purple", "white", "italic"],
            "status_ok": ["bg_teal", "white"],
        }
    },
}

_current_theme_name = "default"

class Style:
    """
    A factory class that creates TermStyle instances and provides semantic
    style shortcuts based on the currently active theme.
    This is the primary entry point for the TermStyle library.
    """
    def __call__(self, text):
        """
        Allows 'style("text")' for starting a fluent style chain.
        """
        return TermStyle(text)

    def _get_current_semantic_styles(self):
        """
        Helper to retrieve the semantic style definitions for the current theme.
        """
        return THEMES[_current_theme_name]["semantic"]

    def __getattr__(self, name):
        """
        Handles calls for semantic styles (e.g., style.error("message")).
        Dynamically applies styles defined in the current theme's semantic mapping.
        """
        semantic_styles = self._get_current_semantic_styles()
        if name in semantic_styles:
            def semantic_styler_func(text):
                styler = TermStyle(text)
                for method_name in semantic_styles[name]:
                    if hasattr(styler, method_name):
                        getattr(styler, method_name)()
                return styler
            return semantic_styler_func
        raise AttributeError(f"Semantic style '{name}' not found in theme '{_current_theme_name}'.")

style = Style()

def set_theme(theme_name):
    """
    Sets the active theme for semantic styling.
    Subsequent calls to semantic styles (e.g., `style.error()`) will use this theme's definitions.
    """
    global _current_theme_name
    if theme_name not in THEMES:
        raise ValueError(f"Theme '{theme_name}' not found. Available themes: {list(THEMES.keys())}")
    _current_theme_name = theme_name
