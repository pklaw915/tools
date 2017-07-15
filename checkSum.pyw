import os
import hashlib
import tkinter
import tkinter.filedialog
import tkinter.messagebox


def calc_md5(fileName):
    with open(fileName, 'rb') as f:
        sh = hashlib.md5()
        sh.update(f.read())
        return sh.hexdigest()
    return ''

def calc_sha256(fileName):
    with open(fileName, 'rb') as f:
        sh = hashlib.sha256()
        sh.update(f.read())
        return sh.hexdigest()
    return ''

class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.labelFile = tkinter.Label(self, text='文件')
        self.labelFile.grid(row=0, column=0, pady=10, padx=10)

        self.inputFile = tkinter.StringVar()
        input_file_command = self.register(self.check_input_file)
        self.editInput = tkinter.Entry(self, width=70, textvariable=self.inputFile, validate='key', validatecommand=(input_file_command, '%P'))
        self.editInput.grid(row=0, column=1, columnspan=2)

        self.browseInput = tkinter.Button(self, text='...', command=self.sel_input)
        self.browseInput.grid(row=0, column=3, ipadx=5)

        self.choiceOption = tkinter.IntVar()
        self.choiceOption.set(0)
        
        self.radioMD5 = tkinter.Radiobutton(self, text='MD5', value=0, variable=self.choiceOption)
        self.radioMD5.grid(row=1, column=1, sticky=tkinter.W)

        self.radioSHA256 = tkinter.Radiobutton(self, text='sha256', value=1, variable=self.choiceOption)
        self.radioSHA256.grid(row=2, column=1, sticky=tkinter.W)

        self.strResult = tkinter.StringVar()
        self.editResultStr = tkinter.Entry(self, width=70, textvariable=self.strResult)
        self.editResultStr['state'] = 'readonly'
        self.editResultStr.grid(row=3, column=1, columnspan=2, sticky=tkinter.W)

        self.btnCalculate = tkinter.Button(self, text='计算', command=self.calculate, default=tkinter.DISABLED, state=tkinter.DISABLED)
        self.btnCalculate.grid(row=3, column=3, ipadx=5, padx=20, pady=10)

        self.strCompare = tkinter.StringVar()
        self.editCompareStr = tkinter.Entry(self, width=70, textvariable=self.strCompare)
        self.editCompareStr.grid(row=4, column=1, columnspan=2, sticky=tkinter.W)

        self.btnCompare = tkinter.Button(self, text='比较', command=self.compare)
        self.btnCompare.grid(row=4, column=3, ipadx=5, padx=20, pady=10)

    def check_input_file(self, file):
        if not file:
            self.btnCalculate.configure(state = tkinter.DISABLED)
        else:
            self.check_calculate(inputFile=file)
        return True

    def sel_input(self):
        inputFile = tkinter.filedialog.askopenfilename()
        if inputFile:
            self.inputFile.set(inputFile)
            self.check_calculate()

    def check_calculate(self, inputFile = ''):
        if not inputFile:
            inputFile = self.inputFile.get()
        is_ok = True
        if not inputFile or not os.path.isfile(inputFile):
            is_ok = False
        if is_ok:
            self.btnCalculate.configure(state = tkinter.NORMAL)
        else:
            self.btnCalculate.configure(state = tkinter.DISABLED)

    def calculate(self):
        inputFile = self.inputFile.get()
        if self.choiceOption.get() == 0:
            res = calc_md5(inputFile)
        else:
            res = calc_sha256(inputFile)
        self.strResult.set(res)

    def compare(self):
        strResult = self.strResult.get()
        strCompare = self.strCompare.get()
        if strResult == strCompare:
            tkinter.messagebox.showinfo('Result', 'Check Sums are the same')
        else:
            tkinter.messagebox.showinfo('Result', 'Check Sums are different!!!!')

if __name__ == '__main__':
    root = Application()
    root.mainloop()
