from typing import Tuple

SLEEP_TIME: float = 1 #seconds

BROWSERS: Tuple[str, ...] = ("Mozilla Firefox", "Google Chrome", "Edge", "Opera", "Brave", "Chromium")
BROWSER_PS_NAMES: Tuple[str, ...] = ("firefox", "chrome", "edge", "opera", "brave", "application") # 'application' for edge

SLEEP_TIME_KEYS: float = 0.05 #seconds
SLEEP_TIME_COPY: float = 0.1 #seconds

BROWSER_ENDS: Tuple[str, ...] = ('Mozilla Firefox', 'Google Chrome', 'Opera', 'Brave')
NEW_TABS: Tuple[str, ...] = ('New Tab - Google Chrome', 'Mozilla Firefox', 'Untitled - Brave', 'New Tab - Brave')
FIREFOX: Tuple[str, ...] = ('Mozilla Firefox',)
CHROME: Tuple[str, ...] = ('Google Chrome', 'Opera', 'Brave')

# BROWSER_ENDS: Tuple[bytes, ...] = (b'Mozilla Firefox', b'Google Chrome', b'Opera', b'Brave')
# NEW_TABS: Tuple[bytes, ...] = (b'New Tab - Google Chrome', b'Mozilla Firefox', b'Untitled - Brave', b'New Tab - Brave')
# FIREFOX: Tuple[bytes, ...] = (b'Mozilla Firefox',)
# CHROME: Tuple[bytes, ...] = (b'Google Chrome', b'Opera', b'Brave')