import sys
try:
    from utils.exceptions import PlatformNotSupported
except ImportError:
    from .utils.exceptions import PlatformNotSupported

platform = sys.platform

if platform.startswith('win'):
    from .windetector import get_window_and_url, get_url, get_window_name
elif platform.startswith('linux'):
    from .xlibdetector import get_url, get_window_and_url, get_window_name
else:
    raise PlatformNotSupported(platform)