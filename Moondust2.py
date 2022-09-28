#!/bin/python

# V.2.0.0.1 --- changes to the frame width, height, and modified the math output_area_height 

import wx
from random import randint
import re


# APP DEFINITIONS

FRAME_WIDTH = 1300
FRAME_HEIGHT = 700
FRAME_SIZE = (FRAME_WIDTH + 15, FRAME_HEIGHT)

#OUTPUT_AREA_HEIGHT = int(2 / 5 * FRAME_HEIGHT) 
# It appears as though it doesn't like the math going on here?  

OUTPUT_AREA_HEIGHT = int(FRAME_HEIGHT*.4)
INPUT_AREA_HEIGHT = FRAME_HEIGHT - OUTPUT_AREA_HEIGHT

WIDGET_SPACING = 10

BUTTON_HEIGHT = 20

OTHER_AREAS_HEIGHT = BUTTON_HEIGHT + 2 * WIDGET_SPACING

TEXT_CTRL_COLUMNS = 6	# controls the number of columns 
TEXT_CTRL_ROWS = 1		# and how many rows
TEXT_CTRL_WIDTH = int(FRAME_WIDTH / TEXT_CTRL_COLUMNS - WIDGET_SPACING)
TEXT_CTRL_HEIGHT = int(INPUT_AREA_HEIGHT / TEXT_CTRL_ROWS - 2 * WIDGET_SPACING - BUTTON_HEIGHT)
TEXT_CTRL_SIZE = (TEXT_CTRL_WIDTH, TEXT_CTRL_HEIGHT)

OUTPUT_TEXT_CTRL_SIZE = (FRAME_WIDTH - 2 * WIDGET_SPACING, OUTPUT_AREA_HEIGHT - BUTTON_HEIGHT -2 * WIDGET_SPACING - 80)


# GENERATION MODEL DEFINITIONS

STATEMENT_SEPARATORS = "[!\.?]\s"
WORD_SEPARATOR = " "
STATEMENT_LENGTH_SPREAD = .5

GENERATION_COUNT = 10
# GENERATION_COUNT = randint(1,11)
# Change this number to decide how many lines of random text you want to create.




class ScrambleFrame(wx.Frame):

    textControls = dict()

    def __init__(self, parent, title=None):
        wx.Frame.__init__(self, parent, title=title, size=FRAME_SIZE, style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        panel = wx.Panel(self)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Moondust: Is up and running. Give me that sweet, sweet text.")

        offset = int(WIDGET_SPACING / 2)
        for y in range(0, TEXT_CTRL_ROWS):
            for x in range(0, TEXT_CTRL_COLUMNS):
                textCtrlPosition = (offset + x * (TEXT_CTRL_WIDTH + WIDGET_SPACING), offset + y * (TEXT_CTRL_HEIGHT + WIDGET_SPACING + BUTTON_HEIGHT))
                self.buildTextCheckBoxPair(panel, textCtrlPosition)


        self.generateButton = wx.Button(panel, label="Generate", pos=(WIDGET_SPACING, INPUT_AREA_HEIGHT))
        self.Bind(wx.EVT_BUTTON, self.OnGenerate)

        outputTextBoxPosition = (WIDGET_SPACING, INPUT_AREA_HEIGHT + WIDGET_SPACING + BUTTON_HEIGHT)
        self.outputTextBox = wx.TextCtrl(panel, style=wx.TE_MULTILINE, pos=outputTextBoxPosition, size=OUTPUT_TEXT_CTRL_SIZE)

        self.Show(True)

    def buildTextCheckBoxPair(self, panel, textCtrlPosition):
        textCtrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE, pos=textCtrlPosition, size=TEXT_CTRL_SIZE)
        textCheckBoxPosition = (textCtrlPosition[0], textCtrlPosition[1] + TEXT_CTRL_HEIGHT + WIDGET_SPACING)
        textCheckBox = wx.CheckBox(panel, label="Include", pos=textCheckBoxPosition)
        self.textControls[textCheckBox] = textCtrl


    def makeMenuBar(self):
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&User Manual...\tCtrl-U",
                                    "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnGenerate(self, event):
        model = Model()

        for checkBox in self.textControls.keys():
            if checkBox.IsChecked():
                model.loadTextIntoModel(self.textControls[checkBox].GetValue())

        self.outputTextBox.Clear()
        for i in range(GENERATION_COUNT):
            statement = model.generateRandomStatement()
            self.outputTextBox.AppendText(statement)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnHello(self, event):
     """Say hello to the user."""
     wx.MessageBox("Hello, and welcome to Scramble, a new age dream machine.  First, fill as many boxes with text that you clip from various sources.  Then select 'Include' for various lines.")





    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This application developed by Stelian Serban for Peter J. Haas.  It is a take on the David Bowie 'Verbasizer' as requested by Squinting Rabbit Productions.",
                      "About Scramble",
                      wx.OK|wx.ICON_INFORMATION)

# GENERATION MODEL

class Model:
    def __init__(self):
        self.words = list()
        self.statementCount = 0
        self.statementLengthCounter = 0

    def __str__(self):
        return "\nWords in model: " + str(self.words) + \
               "\nModel word count: " + str(len(self.words)) + \
               "\nModel statement count: " + str(self.statementCount) + \
               "\nModel statement average statement length: " + str(self.getAverageStatementLength())


    def getAverageStatementLength(self):
        return self.statementLengthCounter / self.statementCount

    def loadStatementIntoModel(self, statement):
        words = [word.strip() for word in statement.split(WORD_SEPARATOR)]
        for word in words:
            if word not in self.words:
                self.words.append(word)
        self.statementCount += 1
        self.statementLengthCounter += len(words)

    def loadTextIntoModel(self, text):
        statements = re.split(STATEMENT_SEPARATORS, text)
        for statement in statements:
            self.loadStatementIntoModel(statement)

    def generateRandomStatement(self):
        statementLen = randint(1, int(self.getAverageStatementLength() * STATEMENT_LENGTH_SPREAD))
        statement = ""
        for i in range(0, statementLen):
            statement += self.words[randint(0, len(self.words)) - 1] + " "
        statement = statement.strip() + ".\n"
        return statement



app = wx.App(False)
frame = ScrambleFrame(None, title='Scramble')
app.MainLoop()
