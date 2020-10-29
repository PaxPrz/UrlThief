class PlatformNotSupported(Exception):
    def __init__(self, platform):
        self.platform = platform

    def __repr__(self):
        return f"Platform '{self.platform}' is not currently supported"
    
    def __str__(self):
        return str(self.__repr__())

class CannotWorkOnThisSystem(Exception):
    def __repr__(self):
        return "Cannot copy text to clipboard: Unsupported by pyperclip"
    
    def __str__(self):
        return str(self.__repr__())