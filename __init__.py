import sys

platform = sys.platform

if platform.startswith('win'):
    from .windetector import get_window_and_url, get_url
else:
    from .xlibdetector import get_url, get_window_and_url, get_window_name