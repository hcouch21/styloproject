#!/usr/bin/python

import rpErrorHandler, tkFileDialog, os, subprocess, shutil, pickle, tempfile, shutil
from Tkinter import *
#------------------------------------------------------------------------------#
#                                                                              #
#                                   StyloGUI                                   #
#                                                                              #
#------------------------------------------------------------------------------#
class StyloGUI(Frame):

    corpusPath = ""
    authors = []
    lastPath = ""
    userSettings = {}
    hiddenDeleteDir = ""

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
        self.__Listbox1 = Listbox(self.__Frame4,height=300,width=50, selectmode=MULTIPLE)
        self.__Scrollbar1 = Scrollbar(self.__Frame4)
        self.__Scrollbar1.pack(side=RIGHT, fill=Y, anchor='e')
        self.__Listbox1.pack(side=LEFT,expand=1,fill=BOTH, anchor='w')
        self.__Scrollbar1.config(command=self.__Listbox1.yview)
        self.__Listbox1.config(yscrollcommand=self.__Scrollbar1.set)
        self.__Frame3 = Frame(self)
        self.__Frame3.pack(padx=15,pady=15,side='left')
        self.__Canvas1 = Canvas(self.__Frame3,height=191,width=250)
        self.logoImage = PhotoImage(file="./stylologo_redblack.gif")
        self.__Canvas1.create_image(125,96,image=self.logoImage)
        self.__Canvas1.pack(side='top')
        self.__Button1 = Button(self.__Frame3,text='Train',width=20, command=self.trainCorpora)
        self.__Button1.pack(side='top')
        self.__Button2 = Button(self.__Frame3,text='Analyze',width=20, command=self.analyzeDocument)
        self.__Button2.pack(side='top')
        self.__Label1 = Label(self.__Frame3,anchor='w',justify='left'
            ,text='Progress')
        self.__Label1.pack(anchor='sw',side='top')
        self.__Text1 = Text(self.__Frame3,height=12,state=DISABLED)
        self.__Scrollbar2 = Scrollbar(self.__Frame3)
        self.__Scrollbar2.pack(side=RIGHT, fill=Y)
        self.__Text1.pack(anchor='s',side='top')
        self.__Scrollbar2.config(command=self.__Text1.yview)
        self.__Text1.config(yscrollcommand=self.__Scrollbar2.set)
        #
        #Your code here
        #
        menubar = Menu(Master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Add A File To The Corpus", command=self.openFile)
        filemenu.add_command(label="Add A Folder of Files to the Corpus", command=self.openFolder)
        filemenu.add_command(label="Remove Selected Files From the Corpus", command=self.removeFiles)
        filemenu.add_command(label="Select Corpus", command=self.openCorpora)
        filemenu.add_command(label="Save Corpus", command=self.saveCorpus)
        filemenu.add_command(label="Quit",command=self.destroy)
        toolsmenu = Menu(menubar, tearoff=0)
        toolsmenu.add_command(label="Manage Feature Sets", command=self.openFeatureSets)
        toolsmenu.add_command(label="Manage Plugins", command=self.openPlugins)
        toolsmenu.add_command(label="Create A New Corpus", command=self.newCorpus)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help", command=self.openHelp)
        helpmenu.add_command(label="About",command=self.openAbout)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Tools", menu=toolsmenu)
        menubar.add_cascade(label="Help", menu=helpmenu)
		
        Master.config(menu=menubar)
        
        if os.path.exists('./guisettings.sgo'):
            settingsFile = open('./guisettings.sgo','r')
            self.userSettings = pickle.load(settingsFile)
            self.corpusPath = self.userSettings['lastCorpus']
            self.updateCorpus()
    #
    #Start of event handler methods
    #

    #
    #Start of non-Rapyd user code
    #
    def openFolder(self):
        if self.corpusPath == "":
            about = Toplevel()
            about.__Label1 = Label(about,anchor='nw',justify='left', padx=15,pady=15 ,text='A corpus must be selected before it can have files added to it!')
            about.__Label1.pack(anchor='nw',side='top')
            about.__OkayButton1 = Button(about, anchor='s',justify='center', text='Okay', command=about.destroy)
            about.__OkayButton1.pack(anchor='s',side='bottom')
            return
        folderLoc = tkFileDialog.askdirectory(parent=self,initialdir=self.corpusPath,title='Please select the Folder containing the files')
        filesToAdd = []
        for work in os.listdir(folderLoc):
            filesToAdd.append(folderLoc+"/"+work)
        #TODO: FINISH THIS, FIX ADDING A SINGLE FILE
    
    def openFile(self):
        if self.corpusPath == "":
            about = Toplevel()
            about.__Label1 = Label(about,anchor='nw',justify='left', padx=15,pady=15 ,text='A corpus must be selected before it can have files added to it!')
            about.__Label1.pack(anchor='nw',side='top')
            about.__OkayButton1 = Button(about, anchor='s',justify='center', text='Okay', command=about.destroy)
            about.__OkayButton1.pack(anchor='s',side='bottom')
            return
        self.newFileName = tkFileDialog.askopenfilename(title="Select A File to Add to the Corpus")
        if(len(self.newFileName) <= 0):
            return
        self.authorSelect = Toplevel()
        self.authorSelect.__Label1 = Label(self.authorSelect,anchor='nw',justify='left', padx=15,pady=15 ,text='Select an author, or add a new one!')
        self.authorSelect.__Label1.pack(anchor='nw',side='top')
        
        self.selection = StringVar()
        self.selection.set("Other")
        self.customselection = StringVar()
        self.customselection.set("")
        
        for author in self.authors:
            b = Radiobutton(self.authorSelect, text=author, variable=self.selection, value=author)
            b.pack(anchor='w')
        b = Radiobutton(self.authorSelect, text="Other", variable=self.selection, value="Other")
        b.pack(anchor='w')
        self.authorSelect.__Entry1 = Entry(self.authorSelect, textvariable=self.customselection)
        self.authorSelect.__Entry1.pack(anchor='w')
        self.authorSelect.__Button1 = Button(self.authorSelect, text="Okay", command=self.addFile)
        self.authorSelect.__Button1.pack()
        
    def saveCorpus(self):
        print "TODO"
    
    def addFile(self):
        newAuthor = self.selection.get()
        if(self.selection.get() == "Other"):
            newAuthor = self.customselection.get()
        self.authorSelect.destroy()
        if self.authors.count(newAuthor) == 0:
            os.mkdir(self.corpusPath+"/"+newAuthor)
        shutil.copy(self.newFileName,self.corpusPath+"/"+newAuthor+"/"+self.newFileName.split("/")[-1])
        self.updateCorpus()
        
    def removeFiles(self):
        if self.hiddenDeleteDir=="":
            self.hiddenDeleteDir = tempfile.mkdtemp()
        for file in self.__Listbox1.curselection():
            print self.__Listbox1.get(file)
        
    def destroy(self):
        outputfile = open('./guisettings.sgo','w')
        pickle.dump(self.userSettings,outputfile)
        self.quit()
		
    def openHelp(self):
        print "TODO"
		
    def openAbout(self):
        about = Toplevel()
        about.__Label1 = Label(about,anchor='nw',justify='left', padx=15,pady=15 ,text='The Stylo Team is:\nKyle Musal\nMatthew Tornetta\nAndrew Orner\nAaron Chapin\n\nAdvised By:\nRachel Greenstadt\nJeff Salvage\n\nVersion 0.1\nApril 6 2011')
        about.__Label1.pack(anchor='nw',side='top')

    def newCorpus(self):
        print "TODO"
        
    def openCorpora(self):
        newCorpusName = tkFileDialog.askdirectory(parent=self,initialdir="../corpora/",title='Please select the Corpus Directory')
        if(len(newCorpusName) <= 0): #No corpus selected
            return
        self.corpusPath = newCorpusName
        self.userSettings['lastCorpus'] = self.corpusPath
        self.updateCorpus()
        
    def updateCorpus(self):
        self.__Listbox1.delete(0,END)
        self.authors = []
        for author in os.listdir(self.corpusPath):
            self.__Listbox1.insert(END,author)
            self.authors.append(author)
            for work in os.listdir(self.corpusPath+"/"+author):
                self.__Listbox1.insert(END, "  " + work)
    
    def analyzeDocument(self):
        if self.corpusPath == "":
            about = Toplevel()
            about.__Label1 = Label(about,anchor='nw',justify='left', padx=15,pady=15 ,text='A corpus must be selected before it can analyze any files!')
            about.__Label1.pack(anchor='nw',side='top')
            about.__OkayButton1 = Button(about, anchor='s',justify='center', text='Okay', command=about.destroy)
            about.__OkayButton1.pack(anchor='s',side='bottom')
            return
        documentToAnalyze = tkFileDialog.askopenfilename(title='Select A File to Analyze')
        if len(documentToAnalyze) <= 0:
            return
        print documentToAnalyze
        analyzeProcess = subprocess.Popen(['python','../stylo.py', '-c', self.corpusPath.split("/")[-1], documentToAnalyze], stdout=subprocess.PIPE)
        while(analyzeProcess.returncode == None):
            analyzeProcess.poll()
            self.__Text1.config(state=NORMAL)
            self.__Text1.insert(END, analyzeProcess.communicate()[0])
            self.__Text1.config(state=DISABLED)
        self.__Text1.config(state=NORMAL)
        self.__Text1.insert(END,"\nANALYSIS COMPLETE!\n")
        self.__Text1.config(state=DISABLED)
        
    def trainCorpora(self):
        if(self.corpusPath ==""):
            about = Toplevel()
            about.__Label1 = Label(about,anchor='nw',justify='left', padx=15,pady=15 ,text='A corpus must be selected before it can be trained on!')
            about.__Label1.pack(anchor='nw',side='top')
            about.__OkayButton1 = Button(about, anchor='s',justify='center', text='Okay', command=about.destroy)
            about.__OkayButton1.pack(anchor='s',side='bottom')
            return
        trainProcess = subprocess.Popen(['python','../stylo.py', '-c', self.corpusPath.split("/")[-1], '-t'], stdout=subprocess.PIPE)
        while(trainProcess.returncode == None):
            trainProcess.poll()
            self.__Text1.config(state=NORMAL)
            self.__Text1.insert(END, trainProcess.communicate()[0])
            self.__Text1.config(state=DISABLED)
        if(trainProcess.returncode == 0):
            self.__Text1.config(state=NORMAL)
            self.__Text1.insert(END,"\nTRAINING PROCESS SUCCESSFUL\n")
            self.__Text1.config(state=DISABLED)
        else:
            self.__Text1.config(state=NORMAL)
            self.__Text1.insert(END,"\nTRAINING PROCESS FAILED!\n")
            self.__Text1.config(state=DISABLED)
		
    def openFeatureSets(self):
        print "TODO"
		
    def openPlugins(self):
        print "TODO"
        

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
        Root.iconbitmap(default='stylo.ico')
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