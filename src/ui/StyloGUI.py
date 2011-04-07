#!/usr/bin/python

import rpErrorHandler, tkFileDialog
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
        #logoImage = PhotoImage(file="stylologo_redblack.gif")
        #image = self.__Canvas1.create_image(0,0,anchor=NE,image=logoImage)
        line = self.__Canvas1.create_line(0,0,191,135)
        line = self.__Canvas1.create_line(191,0,0,135)
        self.__Canvas1.pack(side='top')
        self.__Button1 = Button(self.__Frame3,text='Train',width=20, command=self.trainCorpora)
        self.__Button1.pack(side='top')
        self.__Button2 = Button(self.__Frame3,text='Analyze',width=20, command=self.analyzeDocument)
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
        newFileName = tkFileDialog.askopenfilename(title="Select A File to Add to the Corpus")
        if(len(newFileName) > 0):
            print("Add new File " + newFileName)
        else:
            print("Canceled")
    
    def closeStylo(self):
        print("I should totally do some cleanup before exiting. LOL!")
        self.quit()
		
    def openHelp(self):
        print("NO HELP IS COMING")
		
    def openAbout(self):
        about = Toplevel()
        about.__Label1 = Label(about,anchor='nw',justify='left', padx=15,pady=15 ,text='The Stylo Team is:\nKyle Musal\nMatthew Tornetta\nAndrew Orner\nAaron Chapin\n\nAdvised By:\nRachel Greenstadt\nJeff Salvage\n\nVersion 0.1\nApril 6 2011')
        about.__Label1.pack(anchor='nw',side='top')

    def openCorpora(self):
        newCorpusName = tkFileDialog.askdirectory(parent=self,initialdir="/",title='Please select the Corpus Directory')
        if(len(newCorpusName) > 0):
            print("Selected " + newCorpusName)
        else:
            print("Canceled")
            
    def analyzeDocument(self):
        documentToAnalyze = tkFileDialog.askopenfilename(title='Select A File to Analyze')
        
    def trainCorpora(self):
        self.__Text1.insert(END,"BEGINNING TRAINING PROCESS\n")
        self.__Text1.insert(END,"TRAINING PROCESS COMPLETE\n")
		
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
        Root.title('Stylo')
        Root.mainloop()
    #--------------------------------------------------------------------------#
    # User code should go above this comment.                                  #
    #--------------------------------------------------------------------------#
except:
    rpErrorHandler.RunError()