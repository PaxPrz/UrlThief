import win32gui as win
from time import sleep
import uiautomation as auto
from contextlib import suppress
import psutil
from typing import Tuple, List, Any, Union
try:
    from utils.cache import lru
    from utils.constants import SLEEP_TIME, BROWSERS, BROWSER_PS_NAMES
except ImportError:
    from .utils.cache import lru
    from .utils.constants import SLEEP_TIME, BROWSERS, BROWSER_PS_NAMES

last_win = ''

def get_window_name()-> Tuple[str, int]:
    '''
        Get the foreground window and returns its name and handler

        Returns:
            win_name (str): Title of current active window
            window (int): Window Handle for the active window
    '''
    window = win.GetForegroundWindow()
    win_name = win.GetWindowText(window)
    return win_name, window

def get_url(win_name:str, window:int)-> Union[str, None]:
    '''
        Gets the URL if the current active window is browser
        Checks the process ID of current active window to determine if window is a browser process or not

        Args:
            win_name (str): Name/Title of currently foreground window (to check if its browser)
            window (int): Window handler ID
            
        Returns:
            url (str): If None is returned, the active window is not a browser
    '''
    global last_win
    PROCESS_IS_BROWSER: bool = False
    if any(browser in win_name for browser in BROWSERS):
        if win_name != last_win:
            last_win = win_name
            try:
                url = lru[win_name]
            except KeyError:            
                url = None
                browserControl = auto.ControlFromHandle(window)
                ps_id = browserControl.ProcessId
                ps = psutil.Process(pid=ps_id)
                if any(name in ps.name().lower() for name in BROWSER_PS_NAMES):
                    name_regex = r'.*[Aa]{0,1}ddress(?! bar)'
                    with suppress(LookupError, AttributeError):
                        #for i in range(1,4):
                        #    edit = browserControl.EditControl(foundIndex=i)
                        #    if edit.Name.lower().find('address field' if win_name.endswith('Opera') else 'address') >= 0:
                        #        break
                        edit = browserControl.EditControl(RegexName=name_regex)
                        url = edit.GetValuePattern().Value
                        PROCESS_IS_BROWSER = True
                if url.lstrip('https:// ') != "":
                    lru[win_name] = url
            if PROCESS_IS_BROWSER:
                # print(f"\n[w] {win_name}")
                # print("   [u] ", end="")
                # print(url)
                return url
    return None

def get_window_and_url()-> Tuple[str, Union[str, None]]:
    '''
        Returns the active window name and URL if it's a browser

        Returns:
            win_name (str): Title of currently active window
            url (str): If None is returned the active window is not a Browser
    '''
    win_name, window = get_window_name()
    url = get_url(win_name, window)
    return win_name, url

if __name__ == "__main__":
    print("Searching for Browsers")
    while True:
        win_name, url = get_window_and_url()
        if url:
            print(f"\n[w] {win_name}")
            print(f"   [u] {url}", end="\n\n")
        sleep(SLEEP_TIME)