#!/usr/bin/python3.8
import Xlib
import Xlib.display
import pyperclip
from pynput.keyboard import Key, Controller
from time import sleep
from typing import Union, Tuple
try:
    from utils.cache import lru
    from utils.constants import BROWSER_ENDS, CHROME, FIREFOX, NEW_TABS, SLEEP_TIME_COPY, SLEEP_TIME_KEYS
    from utils.exceptions import CannotWorkOnThisSystem
except ImportError:
    from .utils.cache import lru
    from .utils.constants import BROWSER_ENDS, CHROME, FIREFOX, NEW_TABS, SLEEP_TIME_COPY, SLEEP_TIME_KEYS
    from .utils.exceptions import CannotWorkOnThisSystem

def go_url_bar(sleeptime:float)-> None:
    '''
        Almost all browsers use Ctrl+L to jump to url bar
        
        Args:
            sleeptime (float): Time to sleep between key press
    '''
    keyboard.press(Key.ctrl)
    keyboard.press('l')
    sleep(sleeptime)
    keyboard.release('l')
    keyboard.release(Key.ctrl)

def copy_text(sleeptime:float)-> None:
    '''
        Copies text to OS clipboard

        Args:
            sleeptime (float): Time to sleep between key press
    '''
    keyboard.press(Key.ctrl)
    keyboard.press('c')
    sleep(sleeptime)
    keyboard.release('c')
    keyboard.release(Key.ctrl)

def f6_out_of_url(sleeptime:float)-> None:
    '''
        On Mozilla Firefox, F6 key switches you back to the DOM

        Args:
            sleeptime (float): Time to sleep between key press
    '''
    keyboard.press(Key.f6)
    sleep(sleeptime)
    keyboard.release(Key.f6)

def f10_out_of_url(sleeptime:float)-> None:
    '''
        On Chromium browser, F10 key switches you back to the DOM

        Args:
            sleeptime (float): Time to sleep between key press
    '''
    keyboard.press(Key.f10)
    sleep(sleeptime)
    keyboard.release(Key.f10)

disp = Xlib.display.Display() # import this disp too, and add disp.next_event() in your loop
root = disp.screen().root

NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')
NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')

root.change_attributes(event_mask=Xlib.X.FocusChangeMask)

last_fetched = ''

keyboard = Controller()

backup_clipboard = None

def get_window_name()-> str:
    '''
        Returns currently active window name or None in case of error

        Returns:
            window_name (str): Title of currently active window
    '''
    try:
        window_id = root.get_full_property(NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
        window = disp.create_resource_object('window', window_id)
        window.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
        # window_name = window.get_full_property(NET_WM_NAME, 0).value
        window_name = window.get_full_text_property(NET_WM_NAME)
    except Xlib.error.XError: #simplify dealing with BadWindow
        window_name = None
    return window_name

def get_url(window_name:str)-> Union[str, None]:
    '''
        Gets the url from the currently active window, if window_name denotes its a browser

        Args:
            window_name (str): Currently active window title

        Returns:
            url (str): If gets valid URL returns string else None
    '''
    global last_fetched
    if window_name != last_fetched:
        last_fetched = window_name
        # print('[w] '+window_name if window_name else '')
        is_firefox = False
        if window_name \
        and ((is_firefox:= window_name.endswith(FIREFOX)) or window_name.endswith(CHROME)) \
        and not any(map(lambda x: x==window_name, NEW_TABS)):
            try:
                data = lru[window_name]
                # print('  [u] '+data+'\n')
            except KeyError:
                try:
                    backup_clipboard = pyperclip.paste()
                except pyperclip.PyperclipException:
                    raise CannotWorkOnThisSystem
                go_url_bar(SLEEP_TIME_KEYS)
                copy_text(SLEEP_TIME_COPY)
                if is_firefox:
                    f6_out_of_url(SLEEP_TIME_KEYS)
                else:
                    f10_out_of_url(SLEEP_TIME_KEYS)
                    f10_out_of_url(SLEEP_TIME_KEYS)
                data = pyperclip.paste()
                pyperclip.copy(backup_clipboard)
                if ' ' in data:
                    return None
                lru[window_name] = data
                # print('  [u] '+lru.peek(window_name)+'\n')
            return data
    return None

def get_window_and_url()-> Tuple[str, Union[str, None]]:
    '''
        Gets the window_name and url if window is browser

        Returns:
            window_name (str): Title of current active window
            url (str): If None is returned, the window is not a browser
    '''
    window_name = get_window_name()
    url = None
    if window_name:
        url = get_url(window_name)
    return window_name, url

if __name__ == "__main__":
    print("Searching for Browsers!")
    while True:
        win_name, url = get_window_and_url()
        if url:
            print('[w] '+win_name if win_name else '')
            print('  [u] '+url+'\n')
        event = disp.next_event()