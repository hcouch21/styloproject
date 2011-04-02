#!/usr/bin/python

import rpErrorHandler
from Tkinter import *
#------------------------------------------------------------------------------#
#                                                                              #
#                                   StyloGUI                                   #
#                                                                              #
#------------------------------------------------------------------------------#
class StyloGUI(Frame):
    def __init__(self,Master=None,**kw):
        #
        #Your code here
        #

        apply(Frame.__init__,(self,Master),kw)
        self.__Frame4 = Frame(self)
        self.__Frame4.pack(padx=15,pady=15,side='left')
        self.__Label2 = Label(self.__Frame4,anchor='nw',justify='left'
            ,text='Corpus')
        self.__Label2.pack(anchor='nw',fill='x',side='top')
        self.__Listbox1 = Listbox(self.__Frame4,height=300,width=50)
        self.__Listbox1.pack(anchor='w',expand='yes',fill='both',side='top')
        self.__Frame3 = Frame(self)
        self.__Frame3.pack(padx=15,pady=15,side='left')
        self.__Canvas1 = Canvas(self.__Frame3,height=135,width=191)
        self.__Canvas1.pack(side='top')
        self.__Button1 = Button(self.__Frame3,text='Train',width=20)
        self.__Button1.pack(side='top')
        self.__Button2 = Button(self.__Frame3,text='Analyze',width=20)
        self.__Button2.pack(side='top')
        self.__Label1 = Label(self.__Frame3,anchor='w',justify='left'
            ,text='Progress')
        self.__Label1.pack(anchor='sw',side='top')
        self.__Text1 = Text(self.__Frame3,height=12)
        self.__Text1.pack(anchor='s',side='top')
        #
        #Your code here
        #
        menubar = Menu(Master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open File", command=self.openFile)
        filemenu.add_command(label="Quit",command=self.closeStylo)
        toolsmenu = Menu(menubar, tearoff=0)
        toolsmenu.add_command(label="Manage Corpora", command=self.openCorpora)
        toolsmenu.add_command(label="Manage Feature Sets", command=self.openFeatureSets)
        toolsmenu.add_command(label="Manage Plugins", command=self.openPlugins)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help", command=self.openHelp)
        helpmenu.add_command(label="About",command=self.openAbout)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Tools", menu=toolsmenu)
        menubar.add_cascade(label="Help", menu=helpmenu)
		
        Master.config(menu=menubar)
    #
    #Start of event handler methods
    #

    #
    #Start of non-Rapyd user code
    #
    def openFile(self):
        print("I should totally be opening a file now!")
    
    def closeStylo(self):
        print("I should totally do some cleanup before exiting. LOL!")
        self.quit()
		
    def openHelp(self):
        print("NO HELP IS COMING")
		
    def openAbout(self):
        print("Why don't you tell me a little bit about yourself?")

    def openCorpora(self):
        print("You're a corpora-te tool!")
		
    def openFeatureSets(self):
        print("Here are some sets...of features.")
		
    def openPlugins(self):
        print("<plug-in joke goes here>")
try:
    #--------------------------------------------------------------------------#
    # User code should go after this comment so it is inside the "try".        #
    #     This allows rpErrorHandler to gain control on an error so it         #
    #     can properly display a Rapyd-aware error message.                    #
    #--------------------------------------------------------------------------#

    #Adjust sys.path so we can find other modules of this project
    import sys
    if '.' not in sys.path:
        sys.path.append('.')
    #Put lines to import other modules of this project here
    
    if __name__ == '__main__':

        Root = Tk()
        import Tkinter
        Tkinter.CallWrapper = rpErrorHandler.CallWrapper
        del Tkinter
        App = StyloGUI(Root)
        App.pack(expand='yes',fill='both')

        Root.geometry('640x480+10+10')
        Root.title('StyloGUI')
        Root.mainloop()
    #--------------------------------------------------------------------------#
    # User code should go above this comment.                                  #
    #--------------------------------------------------------------------------#
except:
    rpErrorHandler.RunError()