import os
import sys
# Import the main styling components from your 'PyTermStylePlus' library.
# 'style' is the primary entry point for fluent and semantic styling.
# 'set_theme' allows you to switch between predefined visual themes.
# 'TermStyle' (the class itself) is imported here to access its internal color/format dictionaries
# for iterating through all available styles in the examples.
from PyTermStylePlus import style, set_theme, TermStyle 

# --- Comprehensive Style Examples ---
# This section demonstrates various ways to use the PyTermStylePlus library.

# Display a prominent title for the examples section.
# .underline() and .bold() are fluent methods chained onto the style() call.
# .render() is explicitly called when concatenating with other strings (like the newline in print).
print(style("--- Comprehensive Style Examples ---").underline().bold().render())
print() # Add a blank line for better readability in the terminal output.

# --- Foreground Colors ---
print(style("--- Foreground Colors ---").underline().render())
# Iterate through all defined foreground colors in TermStyle._COLORS to demonstrate each one.
for color_name in TermStyle._COLORS.keys():
    text = f"This is {color_name.replace('_', ' ')} text."
    # Use getattr to dynamically call the corresponding color method (e.g., style(text).red()).
    colored_text = getattr(style(text), color_name)()
    print(colored_text)
print() # Blank line after section.

# --- Background Colors ---
print(style("--- Background Colors ---").underline().render())
# Iterate through all defined background colors in TermStyle._BG_COLORS.
for bg_color_name in TermStyle._BG_COLORS.keys():
    text = f"This has a {bg_color_name.replace('bg_', '').replace('_', ' ')} background."
    # Apply the background color.
    styled_text = getattr(style(text), bg_color_name)()
    # Adjust text color for better contrast on certain backgrounds (e.g., black text on light backgrounds, white on dark).
    if "black" in bg_color_name or "dark" in bg_color_name or "purple" in bg_color_name or "blue" in bg_color_name:
        styled_text = styled_text.white()
    else:
        styled_text = styled_text.black()
    print(styled_text)
print()

# --- Text Formatting ---
print(style("--- Text Formatting ---").underline().render())
# Iterate through all defined text formatting options in TermStyle._FORMATS.
for format_name in TermStyle._FORMATS.keys():
    text = f"This text is {format_name.replace('_', ' ')}."
    # Dynamically apply each formatting method (e.g., style(text).bold()).
    formatted_text = getattr(style(text), format_name)()
    print(formatted_text)
print()

# --- Chained Styles (Combinations) ---
print(style("--- Chained Styles (Combinations) ---").underline().render())
# Demonstrate combining multiple fluent styling methods on a single text string.
print(style("Red text, bold, and underlined.").red().bold().underline())
print(style("Green text with a yellow background, italic.").green().bg_yellow().italic())
print(style("Cyan text, bold, and reversed.").cyan().bold().reverse())
print(style("White text on dark grey background, strikethrough.").white().bg_dark_grey().strikethrough())
print(style("Orange text, bold, and blinking.").orange().bold().blink())
print(style("Purple background with faint olive text.").bg_purple().olive().faint())
print()

# --- Semantic API Examples (Default Theme) ---
# This section shows how to use semantic styles, which change based on the active theme.
# The 'default' theme is active initially.
print(style("--- Semantic API Examples (Default Theme) ---").underline().bold().render())
print(style.error("ERROR: Failed to connect to the database."))
print(style.success("SUCCESS: Data saved successfully."))
print(style.info("INFO: Starting data processing..."))
print(style.warning("WARNING: Disk space is low."))
print(style.highlight("Highlighted important information."))
print(style.primary("Primary action text."))
print(style.secondary("Secondary, less emphasized text."))
# New semantic examples added
print(style.notice("NOTICE: A critical update is available."))
# .render() is used here because the emphasis() call is part of a larger f-string,
# ensuring it returns the string representation for concatenation.
print(style.emphasis("This requires our immediate attention!").render()) 
print(style.status_ok("STATUS: All systems are operational."))
print()

# --- Semantic API Examples (Dark Theme) ---
print(style("--- Semantic API Examples (Dark Theme) ---").underline().bold().render())
# Switch the active theme to 'dark'.
# All subsequent calls to semantic styles will now use the definitions from the 'dark' theme.
set_theme("dark") 
print(style.error("ERROR: Failed to connect to the database."))
print(style.success("SUCCESS: Data saved successfully."))
print(style.info("INFO: Starting data processing..."))
print(style.warning("WARNING: Disk space is low."))
print(style.highlight("Highlighted important information."))
print(style.primary("Primary action text."))
print(style.secondary("Secondary, less emphasized text."))
# New semantic examples in dark theme
print(style.notice("NOTICE: A critical update is available."))
print(style.emphasis("This requires our immediate attention!").render())
print(style.status_ok("STATUS: All systems are operational."))
print()

# Switch back to default or another theme
print(style("--- Back to Default Theme ---").underline().bold().render())
set_theme("default")
print(style.info("Back to default theme info message."))
print()

# --- Handling Unsupported Terminals ---
# This section demonstrates the library's graceful degradation feature.
print(style("--- Handling Unsupported Terminals ---").underline().bold().render())
# Store the original environment variable 'TERM' and the original sys.stdout.isatty function.
original_term_env = os.getenv('TERM')
original_isatty_stdout_func = sys.stdout.isatty 

# Temporarily patch sys.stdout.isatty to simulate a terminal that doesn't support ANSI.
# This will cause TermStyle's internal check to disable styling.
def mock_isatty_false():
    return False
sys.stdout.isatty = mock_isatty_false

# Create a new TermStyle instance. Its _disable_styling flag will now be True.
temp_styler_disabled = TermStyle("This text should not be styled in a simulated dumb terminal.") 
# Even though we call .red().bold(), it will print without style because styling is disabled.
print(temp_styler_disabled.red().bold()) 

# Restore original environment and sys.stdout.isatty function to its normal state.
sys.stdout.isatty = original_isatty_stdout_func # Restore the original function reference
if original_term_env is not None:
    os.environ['TERM'] = original_term_env
else: # If TERM was not set originally, ensure it's deleted from the environment
    if 'TERM' in os.environ:
        del os.environ['TERM']
    
print(style("Terminal restoration attempt successful (next line should be styled).").green())
# This line should now be styled again, confirming that ANSI support is re-enabled.
print(style("This line should be styled again.").magenta().bold()) 
