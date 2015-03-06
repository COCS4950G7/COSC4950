__author__ = 'Chris Hamm'
#GUI_EventPropagation

import wx

class myPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(myPanel, self).__init__(*args,  **kw)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

    def OnButtonClicked(self, e): #event handler
        print 'event reached panel class'
        e.Skip() #propagates the event further

class myButton(wx.Button):
    def __init__(self,*args,**kw):
        super(myButton, self).__init__(*args,**kw)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

    def OnButtonClicked(self, e): #event handler
        print 'event has reached button class'
        e.Skip() #propogates the event further, This is a chain, break the chain and then nobody receives the event after that

class example(wx.Frame):
    def __init__(self,*args, **kw):
        super(example, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        thePanel= myPanel(self)
        myButton(thePanel, label='Ok',pos=(15,15))
        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)
        self.SetTitle('Propagate event')
        self.Centre()
        self.Show(True)

    def OnButtonClicked(self, e): #event handler
        print 'event reached frame class'
        e.Skip() #propogates the event further

def main():
    ex= wx.App()
    example(None)
    ex.MainLoop()

if __name__ == '__main__':
    main()
