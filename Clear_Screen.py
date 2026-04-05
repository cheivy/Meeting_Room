import os
import platform

def clear_screen():
    """跨平台清屏函数"""
    if platform.system() == 'Windows':
        os.system('cls')
    else:  # Linux, macOS
        os.system('clear')