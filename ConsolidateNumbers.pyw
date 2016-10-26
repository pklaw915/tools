import tkinter
import tkinter.filedialog
import tkinter.messagebox
import os

def consolidate_one_line(one_line, sep, connector):
    '''
    >>> consolidate_one_line('1####', '#', '-')
    '1####'
    '''
    out = ''
    last_num = 0
    consolidated_num = 0
    lst = one_line.split(sep)
    for one_str in lst:
        if not one_str.isdigit():
            return one_line
        one_num = int(one_str)
        if one_num <= 0:
            return one_line
        if last_num == 0:               # the first number
            out = one_str
            consolidated_num = 0
        elif one_num != last_num + 1:   # 
            if consolidated_num > 0:
                out = out + connector + str(last_num)
            out = out + sep + one_str
            consolidated_num = 0
        else:
            consolidated_num = consolidated_num + 1
        last_num = one_num
    if consolidated_num > 0:
        out = out + connector + str(last_num)
    return out

def consolidate_one_file(iFile, oFile):
    iFile = iFile.lower()
    oFile = oFile.lower()
    if iFile == oFile:
        return
    hiFile = open(iFile)
    if not hiFile:
        return
    hoFile = open(oFile, mode='w')
    if not hoFile:
        hiFile.close()
        return
    for line in hiFile:
        nn = line.rfind('\n')
        if nn >= 0:
            line = line[0:nn]
        line = consolidate_one_line(line, ',', '-')
        hoFile.write(line)
        if nn >= 0:
            hoFile.write('\n')
    hiFile.close()
    hoFile.close()
    

class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.labelInput = tkinter.Label(self, text='要转换的文件')
        self.labelInput.grid(row=0, column=0, pady=5)

        self.inputFile = tkinter.StringVar()
        self.editInput = tkinter.Entry(self, width=80, textvariable=self.inputFile)
        self.editInput['state'] = 'readonly'
        self.editInput.grid(row=0, column=1)

        self.browseInput = tkinter.Button(self, text='...', command=self.sel_input)
        self.browseInput.grid(row=0, column=2, ipadx=5)

        self.labelOutput = tkinter.Label(self, text='输出到文件')
        self.labelOutput.grid(row=1, column=0)

        self.outputFile = tkinter.StringVar()
        self.editOutput = tkinter.Entry(self, width=80, textvariable=self.outputFile)
        self.editOutput['state'] = 'readonly'
        self.editOutput.grid(row=1, column=1)

        self.browseOutput = tkinter.Button(self, text='...', command=self.sel_output)
        self.browseOutput.grid(row=1, column=2, ipadx=5)

        self.btnOK = tkinter.Button(self, text='OK', command=self.ok, default=tkinter.DISABLED, state=tkinter.DISABLED)
        self.btnOK.grid(row=2, column=2, ipadx=5, padx=20, pady=10)

    def sel_input(self):
        filename = tkinter.filedialog.askopenfilename(defaultextension='.txt', filetypes=[('Text', '*.txt')])
        self.inputFile.set(filename)
        self.check_ok()

    def sel_output(self):
        filename = tkinter.filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text', '*.txt')])
        self.outputFile.set(filename)
        self.check_ok()

    def check_ok(self):
        iFile = self.inputFile.get()
        iFile = iFile.lower()
        oFile = self.outputFile.get()
        oFile = oFile.lower()

        enable_ok = True
        if not iFile or not oFile:
            enable_ok = False
        if os.path.splitext(iFile)[1] != '.txt' or os.path.splitext(oFile)[1] != '.txt':
            enable_ok = False
        elif not os.path.isfile(iFile):
            enable_ok = False
        elif iFile == oFile:
            enable_ok = False
        if enable_ok:
            self.btnOK.configure(state = tkinter.NORMAL)
        else:
            self.btnOK.configure(state = tkinter.DISABLED)

    def ok(self):
        iFile = self.inputFile.get()
        oFile = self.outputFile.get()
        consolidate_one_file(iFile, oFile)
        tkinter.messagebox.showinfo('Success', 'Consolidated Done!!!!')
        self.quit()

if __name__ == '__main__':
    app = Application()
    app.mainloop()
