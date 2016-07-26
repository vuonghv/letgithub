def _16_color(code):
    """
    16 colors supporter
    """
    def color_text(text):
        return '\033[{code}m{text}\033[0m'.format(code=code, text=text)
    return color_text

def _256_color(code):
    """
    256 colors supporter
    """
    def color_text(text):
        return '\033[38;5;{code}m{text}\033[0m'.format(code=code, text=text)
    return color_text

# 16 basic foreground (text) color
default = _16_color('39')
black = _16_color('30')
red = _16_color('31')
green = _16_color('32')
yellow = _16_color('33')
blue = _16_color('34')
magenta = _16_color('35')
cyan = _16_color('36')
light_gray = _16_color('37')
dark_gray = _16_color('90')
light_red = _16_color('91')
light_green = _16_color('92')
light_yellow = _16_color('93')
light_blue = _16_color('94')
light_magenta = _16_color('95')
light_cyan = _16_color('96')
white = _16_color('97')

# 16 basic background color
on_default = _16_color('49')
on_black = _16_color('40')
on_red = _16_color('41')
on_green = _16_color('42')
on_yellow = _16_color('43')
on_blue = _16_color('44')
on_magenta = _16_color('45')
on_cyan = _16_color('46')
on_gray = _16_color('100')
on_light_red = _16_color('101')
on_light_green = _16_color('102')
on_light_yellow = _16_color('103')
on_light_blue = _16_color('104')
on_light_magenta = _16_color('105')
on_light_cyan = _16_color('106')
on_white = _16_color('107')

