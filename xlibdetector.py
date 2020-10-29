#!/usr/bin/python3.8
import Xlib
import Xlib.display
import pylru
import clipboard
from pynput.keyboard import Key, Controller
from time import sleep
from utils.cache import lru
from utils.constants import BROWSER_ENDS, CHROME, FIREFOX, NEW_TABS, SLEEP_TIME_COPY, SLEEP_TIME_KEYS

def go_url_bar(sleeptime):
    keyboard.press(Key.ctrl)
    keyboard.press('l')
    sleep(sleeptime)
    keyboard.release('l')
    keyboard.release(Key.ctrl)

def copy_text(sleeptime):
    keyboard.press(Key.ctrl)
    keyboard.press('c')
    sleep(sleeptime)
    keyboard.release('c')
    keyboard.release(Key.ctrl)

def f6_out_of_url(sleeptime):
    keyboard.press(Key.f6)
    sleep(sleeptime)
    keyboard.release(Key.f6)

def f10_out_of_url(sleeptime):
    keyboard.press(Key.f10)
    sleep(sleeptime)
    keyboard.release(Key.f10)

disp = Xlib.display.Display()
root = disp.screen().root

NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')
NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')

root.change_attributes(event_mask=Xlib.X.FocusChangeMask)

last_fetched = ''

keyboard = Controller()

backup_clipboard = None

def get_window_name():
    try:
        window_id = root.get_full_property(NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
        window = disp.create_resource_object('window', window_id)
        window.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
        # window_name = window.get_full_property(NET_WM_NAME, 0).value
        window_name = window.get_full_text_property(NET_WM_NAME)
    except Xlib.error.XError: #simplify dealing with BadWindow
        window_name = None
    return window_name

def get_url(window_name):
    global last_fetched
    if window_name != last_fetched:
        last_fetched = window_name
        # print('[w] '+window_name if window_name else '')
        url = None
        is_firefox = False
        if window_name \
        and ((is_firefox:= window_name.endswith(FIREFOX)) or window_name.endswith(CHROME)) \
        and not any(map(lambda x: x==window_name, NEW_TABS)):
            try:
                data = lru[window_name]
                # print('  [u] '+data+'\n')
            except KeyError:
                backup_clipboard = clipboard.paste()
                go_url_bar(SLEEP_TIME_KEYS)
                copy_text(SLEEP_TIME_COPY)
                if is_firefox:
                    f6_out_of_url(SLEEP_TIME_KEYS)
                else:
                    f10_out_of_url(SLEEP_TIME_KEYS)
                    f10_out_of_url(SLEEP_TIME_KEYS)
                lru[window_name] = clipboard.paste()
                clipboard.copy(backup_clipboard)
                data = lru.peek(window_name)
                # print('  [u] '+lru.peek(window_name)+'\n')
            return data
    return None

def get_window_and_url():
    window_name = get_window_name()
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