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
    authorIndexes = []
    lastPath = ""
    userSettings = {}
    hiddenDeleteDir = ""
    filesToAdd = []
    addedFiles = []
    features = []
    featuresSelected = []
    plugins = []
    needsToBeTrained = True
    pluginsWindow=None

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
        self.__Listbox1 = Listbox(self.__Frame4,height=300,width=40, selectmode=MULTIPLE)
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
        #self.__Button1 = Button(self.__Frame3,text='Train',width=20, command=self.trainCorpora)
        #self.__Button1.pack(side='top')
        self.__Button2 = Button(self.__Frame3,text='Analyze',width=20, command=self.analyzeDocument)
        self.__Button2.pack(side='top')
        self.__Label1 = Label(self.__Frame3,anchor='w',justify='left',text='Progress')
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
        #filemenu.add_command(label="Save Corpus", command=self.saveCorpus)
        filemenu.add_command(label="Quit",command=self.destroy)
        toolsmenu = Menu(menubar, tearoff=0)
        toolsmenu.add_command(label="Select Feature Sets", command=self.openFeatureSets)
        toolsmenu.add_command(label="Manage Plugins", command=self.openPlugins)
        toolsmenu.add_command(label="Create A New Corpus", command=self.newCorpus)
        toolsmenu.add_command(label="Delete This Corpus", command=self.deleteCorpus)
        helpmenu = Menu(menubar, tearoff=0)
        #helpmenu.add_command(label="Help", command=self.openHelp)
        helpmenu.add_command(label="About",command=self.openAbout)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Tools", menu=toolsmenu)
        menubar.add_cascade(label="Help", menu=helpmenu)
		
        Master.config(menu=menubar)
        
        self.needsToBeTrained = True
        
        #Find which features are currently supported by stylo
        self.getFeatures()
        #print(self.features) #Uncomment to see features
        
        #Read in the GUI settings, such as the last corpus
        if os.path.exists('./guisettings.sgo'):
            settingsFile = open('./guisettings.sgo','r')
            self.userSettings = pickle.load(settingsFile)
            if self.userSettings.has_key('lastCorpus'):
                self.corpusPath = self.userSettings['lastCorpus']
            self.updateCorpus()
        
        #Get the active plugins
        self.plugins = []
        if os.path.exists('../enabled_plugins'):
            pluginsFile = open('../enabled_plugins','r')
            for line in pluginsFile:
                self.plugins.append(line.strip())
    #
    #Start of event handler methods
    #

    #
    #Start of non-Rapyd user code
    #
    
    def getFeatures(self):
        self.features = []
        featuresProcess = subprocess.Popen(['python','../stylo.py', '-l'], stdout=subprocess.PIPE)
        while(featuresProcess.returncode == None):
            featuresProcess.poll()
            newFeature = featuresProcess.communicate()[0].split('\n')
            for feature in newFeature:
                if len(feature.strip('\r')) > 0:
                    self.features.append(feature.strip('\r'))
    
    def openFolder(self):
        if self.corpusPath == "":
            about = Toplevel()
            about.__Label1 = Label(about,anchor='nw',justify='left', padx=15,pady=15 ,text='A corpus must be selected before it can have files added to it!')
            about.__Label1.pack(anchor='nw',side='top')
            about.__OkayButton1 = Button(about, anchor='s',justify='center', text='Okay', command=about.destroy)
            about.__OkayButton1.pack(anchor='s',side='bottom')
            return
        folderLoc = tkFileDialog.askdirectory(parent=self,initialdir=self.corpusPath,title='Please select the Folder containing the files')
        for work in os.listdir(folderLoc):
            self.filesToAdd.append(folderLoc+"/"+work)
        self.openAddDialog()
    
    def openFile(self):
        if self.corpusPath == "":
            about = Toplevel()
            about.__Label1 = Label(about,anchor='nw',justify='left', padx=15,pady=15 ,text='A corpus must be selected before it can have files added to it!')
            about.__Label1.pack(anchor='nw',side='top')
            about.__OkayButton1 = Button(about, anchor='s',justify='center', text='Okay', command=about.destroy)
            about.__OkayButton1.pack(anchor='s',side='bottom')
            return
        newFileName = tkFileDialog.askopenfilename(title="Select A File to Add to the Corpus")
        if(len(newFileName) <= 0):
            return
        self.filesToAdd.append(newFileName)
        self.openAddDialog()
        
    def openAddDialog(self):
        self.authorSelect = Toplevel()
        self.authorSelect.__Label1 = Label(self.authorSelect,anchor='nw',justify='left', padx=15,pady=15 ,text='Select an author, or add a new one!')
        self.authorSelect.__Label1.pack(anchor='nw',side='top')
        self.authorSelect.__Label2 = Label(self.authorSelect,anchor='nw',justify='left', padx=15,pady=15 ,text='Document: ' + self.filesToAdd[0].split('/')[-1])
        self.authorSelect.__Label2.pack(anchor='nw',side='top')
        
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
    
    def addFile(self):
        newAuthor = self.selection.get()
        if(self.selection.get() == "Other"):
            newAuthor = self.customselection.get()
        self.authorSelect.destroy()
        if self.authors.count(newAuthor) == 0:
            os.mkdir(self.corpusPath+"/"+newAuthor)
        shutil.copy(self.filesToAdd[0],self.corpusPath+"/"+newAuthor+"/"+self.filesToAdd[0].split("/")[-1])
        self.addedFiles.append(self.corpusPath+"/"+newAuthor+"/"+self.filesToAdd[0].split("/")[-1])
        self.updateCorpus()
        if len(self.filesToAdd) > 1:
            self.filesToAdd = self.filesToAdd[1:]
            self.openAddDialog()
        else:
            self.filesToAdd = []
        
    def removeFiles(self):
        if self.hiddenDeleteDir=="":
            self.hiddenDeleteDir = tempfile.mkdtemp()
        for file in self.__Listbox1.curselection():
            fileIndex = int(file)
            author = 0
            for authorIndex in range(len(self.authorIndexes) - 1):
                if fileIndex > self.authorIndexes[authorIndex] and fileIndex < self.authorIndexes[authorIndex + 1]:
                    author = authorIndex
                    break
            path = self.corpusPath+"/" + self.authors[author] + "/" + self.__Listbox1.get(file).lstrip()
            os.remove(path)
        self.updateCorpus()
        
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
        self.newCorpus = Toplevel()
        self.newCorpus.__Label1 = Label(self.newCorpus,anchor='nw',justify='left', padx=15,pady=15 ,text='What would you like to call this new corpus?')
        self.newCorpus.__Label1.pack(anchor='nw',side='top')
        self.newCorpusName = StringVar()
        self.newCorpusName.set("")
        self.newCorpus.__Entry1 = Entry(self.newCorpus, textvariable=self.newCorpusName)
        self.newCorpus.__Entry1.pack(anchor='w')
        self.newCorpus.__Button1 = Button(self.newCorpus, text="Okay", command=self.addCorpus)
        self.newCorpus.__Button1.pack()
        
    def addCorpus(self):
        newCorpus = self.newCorpusName.get()
        self.newCorpus.destroy()
        if len(newCorpus) <= 0:
            return
        newCorpus = "../corpora/" + newCorpus 
        os.mkdir(newCorpus)
        self.corpusPath = newCorpus
        self.updateCorpus()
        
    def deleteCorpus(self):
        if self.corpusPath == "":
            about = Toplevel()
            about.__Label1 = Label(about,anchor='nw',justify='left', padx=15,pady=15 ,text='A corpus must be selected before it can be deleted!')
            about.__Label1.pack(anchor='nw',side='top')
            about.__OkayButton1 = Button(about, anchor='s',justify='center', text='Okay', command=about.destroy)
            about.__OkayButton1.pack(anchor='s',side='bottom')
            return
        self.deleteCorpus = Toplevel()
        self.deleteCorpus.__Label1 = Label(self.deleteCorpus,anchor='nw',justify='left', padx=15,pady=15 ,text='Are you sure you want to delete this corpus?')
        self.deleteCorpus.__Label1.pack(anchor='nw',side='top')
        self.deleteCorpus.__Button1 = Button(self.deleteCorpus, text="Yes", command=self.reallyDeleteCorpus)
        self.deleteCorpus.__Button1.pack(anchor='w')
        self.deleteCorpus.__Button2 = Button(self.deleteCorpus, text="No", command=self.deleteCorpus.destroy)
        self.deleteCorpus.__Button2.pack(anchor='e')
    
    def reallyDeleteCorpus(self):
        self.deleteCorpus.destroy()
        shutil.rmtree(self.corpusPath)
        self.corpusPath = ""
        self.userSettings['lastCorpus'] = ""
        self.updateCorpus()
        
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
        self.authorIndexes = []
        self.__Label2.configure(text="Corpus: " + self.corpusPath.split('/')[-1])
        if self.corpusPath == "":
            return
        for author in os.listdir(self.corpusPath):
            if author == "stylo": #This is the folder auto-generated by feature extraction
                continue
            self.authorIndexes.append(self.__Listbox1.size())
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
        analysisArgs = ['python','../stylo.py', '-c', self.corpusPath.split("/")[-1]]
        
        if len(self.featuresSelected) > 0:
            analysisArgs.append('-f')
            features = ""
            for feature in self.featuresSelected:
                features += str(feature)+","
            #print "FEATURES STRING",features[0:-1]
            analysisArgs.append(features[0:-1])
        if self.needsToBeTrained:
            self.trainCorpora(features[0:-1])
            self.needsToBeTrained = False
        analysisArgs.append('-i')
        analysisArgs.append(documentToAnalyze)
        self.__Text1.insert(END, "PERFORMING ANALYSIS. STYLO WILL LOCK UNTIL THE PROCESS IS COMPLETE")
        print("ANALYSIS",analysisArgs)
        analyzeProcess = subprocess.Popen(analysisArgs, stdout=subprocess.PIPE)
        while(analyzeProcess.returncode == None):
            analyzeProcess.poll()
            self.__Text1.config(state=NORMAL)
            self.__Text1.insert(END, analyzeProcess.communicate()[0])
            self.__Text1.config(state=DISABLED)
        self.__Text1.config(state=NORMAL)
        self.__Text1.insert(END,"\nANALYSIS COMPLETE!\n")
        self.__Text1.see(END)
        self.__Text1.config(state=DISABLED)
        
    def trainCorpora(self,features):
        if(self.corpusPath ==""):
            about = Toplevel()
            about.__Label1 = Label(about,anchor='nw',justify='left', padx=15,pady=15 ,text='A corpus must be selected before it can be trained on!')
            about.__Label1.pack(anchor='nw',side='top')
            about.__OkayButton1 = Button(about, anchor='s',justify='center', text='Okay', command=about.destroy)
            about.__OkayButton1.pack(anchor='s',side='bottom')
            return
        trainingArgs = ['python','../stylo.py', '-c', self.corpusPath.split("/")[-1], '-t']
        if(features):
            trainingArgs.append('-f')
            trainingArgs.append(features)
        #print("TRAINING",trainingArgs)
        trainProcess = subprocess.Popen(trainingArgs, stdout=subprocess.PIPE)
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
        self.featureSelect = Toplevel()
        self.featureSelect.__Label1 = Label(self.featureSelect,anchor='nw',justify='left', padx=15,pady=15 ,text='Select the features to be analyzed.')
        self.featureSelect.__Label1.pack(anchor='nw',side='top')
        self.featureSelect.__Button1 = Button(self.featureSelect, anchor='w',justify='center', text='Select All', command=self.selectAllFeatures)
        self.featureSelect.__Button1.pack(anchor='w')
        self.featureSelect.__Button2 = Button(self.featureSelect,justify='center', text='Select None', command=self.selectNoFeatures)
        self.featureSelect.__Button2.pack(anchor='w')
        self.selectedFeatures = []
        self.featureSelect.checkBoxes = []
        for featureIndex in range(len(self.features)):
            featureVar = IntVar()
            checkBox = Checkbutton(self.featureSelect, text=self.features[featureIndex], variable=featureVar, offvalue=0, onvalue=featureIndex+1)#Default offvalue is 1, so add 1 to 1-index the list
            if self.featuresSelected.count(self.features[featureIndex].split('-')[0].strip()) > 0:
                checkBox.select()
            checkBox.pack(anchor='w')
            self.featureSelect.checkBoxes.append(checkBox)
            self.selectedFeatures.append(featureVar)
        
        self.featureSelect.__Button3 = Button(self.featureSelect, text="Okay", command=self.setFeatures)
        self.featureSelect.__Button3.pack()
        
    def selectAllFeatures(self):
        for checkBox in self.featureSelect.checkBoxes:
            checkBox.select()
            
    def selectNoFeatures(self):
        for checkBox in self.featureSelect.checkBoxes:
            checkBox.deselect()
    
    def setFeatures(self):
        self.selectedFeatures = filter(self.isEmpty, self.selectedFeatures)
        newfeatures = []
        for feature in self.selectedFeatures:
            newfeatures.append(self.features[feature.get() - 1].split('-')[0].strip())
        self.featuresSelected = newfeatures
        self.needsToBeTrained = True
        self.featureSelect.destroy()
	
    def isEmpty(self, var):
        if var.get() <= 0:
            return False
        else:
            return True
	
    def openPlugins(self):
        self.pluginsWindow = Toplevel()
        self.pluginsWindow.__Frame1 = Frame(self.pluginsWindow)
        self.pluginsWindow.__Frame1.pack(side='top')
        self.pluginsWindow.__Label1 = Label(self.pluginsWindow.__Frame1,anchor='nw',justify='left', padx=15,pady=15 ,text='Currently active plugins:')
        self.pluginsWindow.__Label1.pack(anchor='nw',side='top')
        self.pluginsWindow.__Frame2 = Frame(self.pluginsWindow)
        self.pluginsWindow.__Frame2.pack()
        self.pluginsWindow.__Frame2.__Listbox1 = Listbox(self.pluginsWindow.__Frame2,height=10,width=60, selectmode=NORMAL)
        self.pluginsWindow.__Frame2.__Scrollbar1 = Scrollbar(self.pluginsWindow.__Frame2)
        self.pluginsWindow.__Frame2.__Scrollbar1.pack(side=RIGHT, fill=Y, anchor='e')
        self.pluginsWindow.__Frame2.__Listbox1.pack(side=LEFT, anchor='w')
        self.pluginsWindow.__Frame2.__Scrollbar1.config(command=self.pluginsWindow.__Frame2.__Listbox1.yview)
        self.pluginsWindow.__Frame2.__Listbox1.config(yscrollcommand=self.pluginsWindow.__Frame2.__Scrollbar1.set)
        self.pluginsWindow.__Frame3 = Frame(self.pluginsWindow)
        self.pluginsWindow.__Frame3.pack(side='bottom',padx=7,pady=7)
        self.pluginsWindow.__Frame3.__Button3 = Button(self.pluginsWindow.__Frame3, text="Add A Plugin", command=self.addPlugin)
        self.pluginsWindow.__Frame3.__Button3.pack(side=LEFT, anchor='sw')
        self.pluginsWindow.__Frame3.__Button2 = Button(self.pluginsWindow.__Frame3, text="Remove Selected Plugin", command=self.deletePlugin)
        self.pluginsWindow.__Frame3.__Button2.pack(side=LEFT,anchor='s')
        self.pluginsWindow.__Frame3.__Button1 = Button(self.pluginsWindow.__Frame3, text="Save Settings", command=self.setPlugins)
        self.pluginsWindow.__Frame3.__Button1.pack(side=RIGHT, anchor='se')
        
        for plugin in self.plugins:
            self.pluginsWindow.__Frame2.__Listbox1.insert(END,plugin)
    
    def addPlugin(self):
        newPlugin = tkFileDialog.askdirectory(parent=self,initialdir='../plugins',title='Please select a plugin to add')
        if len(newPlugin) <= 0:
            return
        self.pluginsWindow.__Frame2.__Listbox1.insert(END,newPlugin.split('/')[-1])
        
    def deletePlugin(self):
        self.pluginsWindow.__Frame2.__Listbox1.delete(self.pluginsWindow.__Frame2.__Listbox1.curselection()[0])
    
    def setPlugins(self):
        self.plugins = []
        pluginsFile = open('../enabled_plugins','w')
        for index in range(self.pluginsWindow.__Frame2.__Listbox1.size()):
            pluginsFile.write(self.pluginsWindow.__Frame2.__Listbox1.get(index).strip() + "\n")
            self.plugins.append(self.pluginsWindow.__Frame2.__Listbox1.get(index).strip())
        pluginsFile.close()
        self.getFeatures()
        self.pluginsWindow.destroy()

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
        try:
		    Root.iconbitmap(default='stylo.ico')
        except:
		    a = 0 #Don't do anything
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