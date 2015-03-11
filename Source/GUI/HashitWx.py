__author__ = 'jwright'

import wx
import hashlib

app = wx.App(redirect=True)
top = wx.Frame(None, title="Hash It", size=(300,200))
top.Show()
app.MainLoop()


#hash_object = hashlib.md5(self.inputHashTextField.get())
#print self.inputHashTextField.get()
#print(hash_object.hexdigest())
#
#print hash_object.hexdigest()

word = raw_input('Enter a word to hash \n')
hash_object = hashlib.md5(word)
print hash_object.hexdigest()
