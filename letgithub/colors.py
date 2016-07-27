def color_16(code):
    """
    16 colors supporter
    """
    def color_text(text):
        return '\033[{code}m{text}\033[0m'.format(code=code, text=text)
    return color_text

def color_256(code, bg=False):
    """256 colors supporter

    Return 256 colors for forceground (default) or background (bg=True)
    """
    def color_text(text):
        type_color = 48 if bg else 38
        return '\033[{type_color};5;{code}m{text}\033[0m'.format(
                type_color=type_color, code=code, text=text)
    return color_text

# 16 basic foreground (text) color
default = color_16('39')
black = color_16('30')
red = color_16('31')
green = color_16('32')
yellow = color_16('33')
blue = color_16('34')
magenta = color_16('35')
cyan = color_16('36')
light_gray = color_16('37')
dark_gray = color_16('90')
light_red = color_16('91')
light_green = color_16('92')
light_yellow = color_16('93')
light_blue = color_16('94')
light_magenta = color_16('95')
light_cyan = color_16('96')
white = color_16('97')

# 16 basic background color
on_default = color_16('49')
on_black = color_16('40')
on_red = color_16('41')
on_green = color_16('42')
on_yellow = color_16('43')
on_blue = color_16('44')
on_magenta = color_16('45')
on_cyan = color_16('46')
on_gray = color_16('100')
on_light_red = color_16('101')
on_light_green = color_16('102')
on_light_yellow = color_16('103')
on_light_blue = color_16('104')
on_light_magenta = color_16('105')
on_light_cyan = color_16('106')
on_white = color_16('107')

def color(code):
    """
    Return color text function based on name
    """
    if str(code).isdigit():
        return color_256(code)
    return globals()[code]

def get_contrast(rgb: str):
    """Return color contrast
    """
    rgb = rgb.lstrip('#')
    if int(rgb, 16) > (0xffffff/2):
        return color('black')
    return color('white')

