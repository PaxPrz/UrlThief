import win32gui as win
from time import sleep
import uiautomation as auto
from contextlib import suppress
import psutil
from typing import Tuple, List, Any, Union
from utils.cache import lru
from utils.constants import SLEEP_TIME, BROWSERS, BROWSER_PS_NAMES

last_win = ''

def get_window_name():
    window = win.GetForegroundWindow()
    win_name = win.GetWindowText(window)
    return win_name, window

def get_url(win_name, window):
    global last_win
    PROCESS_IS_BROWSER: bool = False
    if any(browser in win_name for browser in BROWSERS):
        if win_name != last_win:
            last_win = win_name
            try:
                url = lru[win_name]
            except KeyError:            
                url = ''
                browserControl = auto.ControlFromHandle(window)
                ps_id = browserControl.ProcessId
                ps = psutil.Process(pid=ps_id)
                if any(name in ps.name().lower() for name in BROWSER_PS_NAMES):
                    name_regex = r'.*[Aa]{0,1}ddress(?! bar)'
                    with suppress(LookupError):
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

def get_window_and_url():
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