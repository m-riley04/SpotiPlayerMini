import os; import ctypes; import playerpages as ex

'''
App Credentials
My ID: "ca44a4c54b6e44d8bac44a11f26f9773"
My Secret: "c39263ba04d841d8a93657da99a80671"
'''

def hide_terminal():
    '''Hides the terminal'''
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')

    SW_HIDE = 0

    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, SW_HIDE)

def main():
    global sp #-- main Spotify variable

    #Login Window
    loginApp = ex.LoginApp()
    loginApp.mainloop()

    hide_terminal() #-- hides the terminal for better UI experience

    #Player Window
    playerApp = ex.PlayerApp()
    playerApp.title("SpotiPlayerMini")
    playerApp.mainloop()
    
    os._exit(os.EX_OK) #-- forcefully stops timers/code

#========================================================================#

if __name__ == "__main__":
    main()