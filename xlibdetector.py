#!/usr/bin/python3.8
import Xlib
import Xlib.display
import pylru
import clipboard
from pynput.keyboard import Key, Controller
from time import sleep

disp = Xlib.display.Display()
root = disp.screen().root

NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')
NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')

root.change_attributes(event_mask=Xlib.X.FocusChangeMask)

last_fetched = None
keyboard = Controller()

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

lru = pylru.lrucache(size=20)
SLEEP_TIME = 0.05 #sec
SLEEP_TIME_COPY = 0.1 #seconds
BROWSER_ENDS = (b'Mozilla Firefox', b'Google Chrome', b'Opera', b'Brave')
NEW_TABS = (b'New Tab - Google Chrome', b'Mozilla Firefox', b'Untitled - Brave', b'New Tab - Brave')
FIREFOX = (b'Mozilla Firefox')
CHROME = (b'Google Chrome', b'Opera', b'Brave')
backup_clipboard = None

while True:
    try:
        window_id = root.get_full_property(NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
        window = disp.create_resource_object('window', window_id)
        window.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
        # window_name = window.get_full_property(NET_WM_NAME, 0).value
        window_name = window.get_full_text_property(NET_WM_NAME).encode()
    except Xlib.error.XError: #simplify dealing with BadWindow
        window_name = None
        continue
    if window_name != last_fetched:
        last_fetched = window_name
        print('[w] '+window_name.decode() if window_name else '')
        is_firefox = False
        if window_name \
        and ((is_firefox:= window_name.endswith(FIREFOX)) or window_name.endswith(CHROME)) \
        and not any(map(lambda x: x==window_name, NEW_TABS)):
            try:
                data = lru[window_name]
                print('  [u] '+data+'\n')
            except KeyError:
                backup_clipboard = clipboard.paste()
                go_url_bar(SLEEP_TIME)
                copy_text(SLEEP_TIME_COPY)
                if is_firefox:
                    f6_out_of_url(SLEEP_TIME)
                else:
                    f10_out_of_url(SLEEP_TIME)
                    f10_out_of_url(SLEEP_TIME)
                lru[window_name] = clipboard.paste()
                clipboard.copy(backup_clipboard)
                print('  [u] '+lru.peek(window_name)+'\n')
    event = disp.next_event()


