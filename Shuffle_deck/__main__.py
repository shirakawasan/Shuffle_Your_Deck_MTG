import wx
import wx._adv
import wx._html
import sys
import shuffle_gui as sg

def main():
    application = wx.App()
    guiobj = sg.GUI()
    guiobj.frame.Show()
    application.MainLoop()

if __name__ == "__main__":
    main()