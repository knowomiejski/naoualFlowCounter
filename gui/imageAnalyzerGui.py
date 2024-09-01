from tkinter import *
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import askdirectory
import threading
from os import path
from os import listdir
from os import walk
from os import fsdecode

class ImageAnalyzerGui:
    files = ()

    def __init__(self, imageAnalyzer) -> None:
        self.imageAnalyzer = imageAnalyzer
        self.startTinker();

    def startTinker(self):
        root = Tk()
        root.title("Naoual image analyzer")
        root.geometry("1400x900+100+50")
        root.minsize(700, 500)

        self.createSections(root)
        self.populateFrames()


        self.directoriesWithSegmentedImages = []
        self.frameDirectoriesWithSegmentedImages = {}
        root.mainloop()

    def createSections(self, root):
        self.leftFrame = Frame(root, bg='#05021c')
        self.rightFrame = Frame(root)

        root.columnconfigure(0, weight=4, minsize=230)
        root.columnconfigure(1, weight=8, minsize=700)

        root.rowconfigure(0, weight=1, minsize=250)
        root.rowconfigure(1, weight=1, minsize=250)

        self.leftFrame.pack(expand=True, fill="both")

        self.rightFrame.columnconfigure(1, weight=1, pad=5, minsize=700)
        self.rightFrame.rowconfigure(0, weight=1, minsize=400)

        self.leftFrame.grid(row=0, rowspan=2, column=0, sticky="nesw")
        self.rightFrame.grid(row=0, rowspan=2, column=1, sticky="nesw")

        #====================================================================================
        #TOP RIGHT
        self.cziFilesFrameParent = Frame(self.rightFrame)

        #Canvas child of cziFilesFrameParent
        self.cziFilesCanvas = Canvas(self.cziFilesFrameParent, bg='#12021a', scrollregion=(0, 0, 1000, 1000), bd=0, highlightthickness=0)
        self.cziFilesCanvas.pack(side=LEFT, expand=True, fill=BOTH)

        #Scrollbar of cziFilesFrameParent
        self.cziFilesScrollbar = Scrollbar(self.cziFilesFrameParent, orient="vertical", command=self.cziFilesCanvas.yview)
        self.cziFilesScrollbar.place(relx=1, rely=0, relheight=1, anchor=NE)
        self.cziFilesCanvas.config(yscrollcommand=self.cziFilesScrollbar.set)

        self.cziFilesFrame = Frame(self.cziFilesCanvas, bg='#12021a')
        self.cziFilesCanvasWindow = self.cziFilesCanvas.create_window((0,0), window=self.cziFilesFrame, anchor=NW)
        self.cziFilesFrameParent.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        self.cziFilesFrame.bind("<Configure>", self.OnFrameConfigureCziFiles)
        self.cziFilesCanvas.bind('<Configure>', self.FrameWidthCziFiles)
        #====================================================================================


    def FrameWidthCziFiles(self, event):
        canvas_width = event.width
        self.cziFilesCanvas.itemconfig(self.cziFilesCanvasWindow, width = canvas_width)

    def OnFrameConfigureCziFiles(self, event):
        self.cziFilesCanvas.configure(scrollregion=self.cziFilesCanvas.bbox("all"))


    def populateFrames(self):
        selectFileLabel = Label(self.leftFrame, text="Select files", bg='#05021c', fg="#fff")
        selectFileLabel.grid(row=0, column=0, padx=5, pady=5,  sticky=NSEW)

        selectFileButton = Button(self.leftFrame, text="Select files", command=self.openFilesSelectionDialog)
        selectFileButton.grid(row=1, column=0, padx=5, pady=5,  sticky=NSEW)

        splitButton = Button(self.leftFrame, text="Run flow count", command=self.startFlowCellCounting)
        splitButton.grid(row=3, column=0, padx=5, pady=5,  sticky=NSEW)

    def testPopulateList(self):
        for i in range(100):
            selectFileLabel = Label(self.cziFilesFrame)
            selectFileLabel.columnconfigure(0, weight=12)
            selectFileLabel.grid(row= i, columnspan=12, padx=5, pady=5, sticky="nesw")
            label = Label(selectFileLabel, text="Test file " + str(i), bg='#b1eba4')
            label.pack(expand=True, fill="both")

    def openTestImage(self):
        self.imageAnalyzer.testLoadImage()

    def findExistingOutputs(self):
        self.directoriesWithSegmentedImages = []

    def openFilesSelectionDialog(self):
        self.files = askopenfilenames()
        self.renderFilesList()

    def removeItemFileFromList(self, file):
        filesList = list(self.files)
        filesList.remove(file)
        self.files = tuple(filesList)
        self.frameFiles[file].destroy()
        print("self.frameFiles[file]", self.frameFiles[file])
        print("self.files",  self.files)

    def renderFilesList(self):
        i = 0
        self.frameFiles = {}
        for file in self.files:
            frameFile = Frame(self.cziFilesFrame, pady=2)
            frameFile.grid(row=i, column=0, columnspan=9, sticky="we")
            imageName = Label(frameFile, text=file, bg="#b1eba4", width=90)
            imageName.pack(side=LEFT, expand=True, fill=BOTH)
            # imageName.grid(row=0, column=0, columnspan=11, sticky=NSEW)
            button = Button(frameFile, text="X", command= lambda file=file: self.removeItemFileFromList(file), pady=0)
            button.pack(side=RIGHT, expand=False, fill=BOTH)
            # button.grid(row=0, column=11,  sticky=NSEW)
            self.frameFiles[file] = frameFile
            i = i + 1

    def startFlowCellCounting(self):
        fileA = ""
        fileB = ""

        for file1 in self.files:
            if (file1.endswith("a.jpg") and fileA == ""):
                fileA = file1
                for file2 in self.files:
                    if (file2.startswith(fileA.replace("a.jpg", "b.jpg"))):
                        fileB = file2
                        self.imageAnalyzer.countFlowCells(fileA, fileB)
                        break
                fileA = ""
                fileB = ""
                continue