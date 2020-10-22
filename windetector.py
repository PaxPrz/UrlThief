import win32gui as win
from time import sleep
import uiautomation as auto
from contextlib import suppress
import pylru
import psutil

SLEEP_TIME = 1

lru = pylru.lrucache(size=20)
BROWSERS = ("Mozilla Firefox", "Google Chrome", "Edge", "Opera")
BROWSER_PS_NAMES = ("firefox", "chrome", "edge", "opera", "application") # 'application' if for edge

last_win = ''

if __name__ == "__main__":
    print("Searching for Browsers")
    while True:
        PROCESS_IS_BROWSER = False
        window = win.GetForegroundWindow()
        win_name = win.GetWindowText(window)
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
                    print(f"\n[w] {win_name}")
                    print("   [u] ", end="")
                    #if not url.startswith("http"):
                    #    print("http://", end='')
                    print(url)
        sleep(SLEEP_TIME)