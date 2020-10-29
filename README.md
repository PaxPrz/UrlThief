# URLThief

============================

## Introduction

This module will capture the URL from active browser from Firefox, Chrome, Brave, Opera and Edge browsers. It is currently supported in Windows operating system with **uiautomation** supported; and Linux operating system working with **Xlib** Desktop manager.

## Installation

`python3.8 -m pip install UrlThief`

## Usage

```
import UrlThief
while True:
    window_name, url = get_window_and_url()
    sleep(SLEEPTIME) # sleep as necessary or use event listener
```

## Console Usage

### Windows

`python3.8 -m UrlThief.windetector`

### Linux

`python3.8 -m UrlThief.xlibdetector`

