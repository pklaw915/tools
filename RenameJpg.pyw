import os
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import datetime
import exifread as EXIF

# options
READ_EXIF=0
FIXED_DATE=1
MODIFY_DATE=2


def is_valid_date_prefix(sdt, fmt = ''):
    '''
    >>> is_valid_date_prefix('19991231')
    True
    >>> is_valid_date_prefix('20100229')
    False
    >>> is_valid_date_prefix('20100228')
    True
    >>> is_valid_date_prefix('20150510')
    True
    >>> is_valid_date_prefix('20200510')
    False
    '''
    if not fmt:
        fmt = '%Y%m%d'
    try:
        c = datetime.datetime.strptime(sdt,fmt)
    except ValueError:
        return False
    if c > datetime.datetime.now():
        return False
    return True

def read_jpg_datetime(full_name):
    f = open(full_name, 'rb')
    tag = 'EXIF DateTimeOriginal'
    tags = EXIF.process_file(f, tag)
    if tag in tags.keys():
        return str(tags[tag])
    tag = 'EXIF DateTimeDigitized'
    if tag not in tags.keys():
        tags = EXIF.process_file(f, tag)
    f.close()

    if tag in tags.keys():
        return str(tags[tag])
    else:
        return ''

def split_date_try_format(sdt, fmt):
    try:
        c = datetime.datetime.strptime(sdt, fmt)
    except:
        return ''
    return c.strftime('%Y%m%d')


def split_date(sdt):
    '''
    >>> split_date('abdfdfdsfdsf')
    ''
    >>> split_date(' ')
    ''
    >>> split_date('ddddd ttttt')
    ''
    >>> split_date('2010:12:31 12:31')
    '20101231'
    >>> split_date('2010:12:31')
    ''
    >>> split_date('2010:02:01')
    ''
    >>> split_date('2010:02:01 12:31')
    '20100201'
    >>> split_date('2010:02:30 12:31')
    ''
    '''
    c = split_date_try_format(sdt, '%Y:%m:%d %H:%M:%S')
    if not c:
        c = split_date_try_format(sdt, '%Y:%m:%d %H:%M')
    return c

def make_new_name(full_name, userStr):
    sdt = userStr
    if not sdt:
        sdt = split_date(read_jpg_datetime(full_name))
    if len(sdt) != 8:   # YYYYMMDD, 8 bytes
        return ''
    sa = full_name.rpartition(os.sep)
    if len(sa) != 3 or len(sa[1]) == 0 or len(sa[2]) == 0:
        return ''
    if sa[2].find(sdt) != 0:
        if sa[2][0] != '_':
            sdt = sdt + '_'
        return sa[0] + sa[1] + sdt + sa[2]
    return ''

def name_begin_with_date(file_name):
    p_under_scroe = file_name.find('_')
    if p_under_scroe <= 0:
        return False
    sdt = file_name[0:p_under_scroe]
    return is_valid_date_prefix(sdt, '%Y%m%d') or is_valid_date_prefix(sdt, '%Y-%m-%d')

def rename_jpg(full_name, userStr):
    dot = full_name.rfind('.')
    if dot < 0 or full_name[dot + 1 :].lower() != 'jpg':
        return False
    old_name = os.path.split(full_name)[1]
    if name_begin_with_date(old_name):
        print('skipping file: ' + old_name)
        return False
    new_name = make_new_name(full_name, userStr)
    if len(new_name) != 0:
        os.rename(full_name, new_name)
        print(full_name + ' ==> ' + new_name)
        return True
    return False

def modify_date(full_name, matchStr):
    sa = full_name.rpartition(os.sep)
    if len(sa) != 3 or len(sa[1]) == 0 or len(sa[2]) == 0:
        return False
    old_name = sa[2]
    p_under_score = old_name.find('_')
    if p_under_score < 0:
        return False
    sdt = old_name[0:p_under_score]
    try:
        c = datetime.datetime.strptime(sdt,matchStr)
    except ValueError:
        return False
    if not c:
        return False
    sdt = c.strftime('%Y%m%d')
    new_name = sdt + old_name[p_under_score:]
    if new_name:
        os.rename(full_name, sa[0] + sa[1] + new_name)
        print(full_name + ' ==> ' + new_name)
        return True
    return False

def check_ignore(root):
    '''
    return bit combination:
    1==> ignore file
    2==> ignore path
    '''
    ignore = os.path.join(root, 'jpg.ignore')
    if not os.path.isfile(ignore):
        return 0
    f = open(ignore, 'r')
    if not f:
        return 0
    ignoreFile = False
    ignorePath = False
    for line in f.readlines():
        key_sep_val = line.partition('=')
        key = key_sep_val[0].strip()
        val = key_sep_val[2].strip()
        if len(key) == 0 or len(key_sep_val[1]) == 0 or len(val) == 0:
            pass
        else:
            val = int(val)
            key = key.lower()
            if key == 'ignore_file':
                ignoreFile = val != 0
            elif key == 'ignore_path':
                ignorePath = val != 0
    f.close()
    nRet = 0
    if ignoreFile:
        nRet = nRet + 1
    if ignorePath:
        nRet = nRet + 2
    return nRet

def loop_dir(root, subPath, func, addStr):
    ignore = check_ignore(root)
    ignoreFile = False
    ignorePath = False
    if ignore & 1:
        ignoreFile = True
        print('Skip Files in ' + root)
    if ignore & 2:
        ignorePath = True
        print('Skip sub folders in ' + root)
    
    numRenamed = 0
    for i in os.listdir(root):
        path = os.path.join(root,i)
        if os.path.isfile(path):
            if ignoreFile:
                pass
            elif func(path, addStr):
                numRenamed = numRenamed + 1
        elif subPath:
            if ignorePath:
                pass
            else:
                numRenamed = loop_dir(path, subPath, func, addStr) + numRenamed
    return numRenamed

class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.createWidgets()
        self.setDefault()

    def createWidgets(self):
        self.labelPath = tkinter.Label(self, text='目录')
        self.labelPath.grid(row=0, column=0, pady=10, padx=10)

        self.inputPath = tkinter.StringVar()
        input_path_command = self.register(self.check_input_path)
        self.editInput = tkinter.Entry(self, width=70, textvariable=self.inputPath, validate='key', validatecommand=(input_path_command, '%P'))
        self.editInput.grid(row=0, column=1, columnspan=2)

        self.browseInput = tkinter.Button(self, text='...', command=self.sel_input)
        self.browseInput.grid(row=0, column=3, ipadx=5)

        self.choiceOption = tkinter.IntVar()
        self.choiceOption.set(READ_EXIF)
        
        self.radioReadExif = tkinter.Radiobutton(self, text='从EXIF读取拍摄日期', command=self.sel_option, value=READ_EXIF, variable=self.choiceOption)
        self.radioReadExif.grid(row=1, column=1, sticky=tkinter.W)

        self.selSubPath = tkinter.IntVar()
        self.checkSubPath = tkinter.Checkbutton(self, text='包含子目录', variable=self.selSubPath)
        self.checkSubPath.grid(row=1, column=2, sticky=tkinter.W)

        self.radioUseStr = tkinter.Radiobutton(self, text='使用固定日期(不支持递归目录)', command=self.sel_option, value=FIXED_DATE, variable=self.choiceOption)
        self.radioUseStr.grid(row=2, column=1, sticky=tkinter.W)

        self.userStr = tkinter.StringVar()
        user_str_command = self.register(self.check_user_str)
        self.editUserStr = tkinter.Entry(self, width=40, textvariable=self.userStr, validate='key', validatecommand=(user_str_command, '%P'))
        self.editUserStr['state'] = 'readonly'
        self.editUserStr.grid(row=2, column=2, sticky=tkinter.W)

        self.radioModify = tkinter.Radiobutton(self, text='修改匹配的日期', command=self.sel_option, value=MODIFY_DATE, variable=self.choiceOption)
        self.radioModify.grid(row=3, column=1, sticky=tkinter.W)

        self.matchStr = tkinter.StringVar()
        match_str_command = self.register(self.check_match_str)
        self.editMatchStr = tkinter.Entry(self, width=40, textvariable=self.matchStr, validate='key', validatecommand=(match_str_command, '%P'))
        self.editMatchStr['state'] = 'readonly'
        self.editMatchStr.grid(row=3, column=2, sticky=tkinter.W)

        self.btnOK = tkinter.Button(self, text='OK', command=self.ok, default=tkinter.DISABLED, state=tkinter.DISABLED)
        self.btnOK.grid(row=4, column=3, ipadx=5, padx=20, pady=10)

        self.separator = tkinter.Label(self, text = '-----------------------------------------------------------------------------------------------------------')
        self.separator.grid(row=5, column=0, columnspan=4, sticky=tkinter.W, padx=10)

        self.hintIgnore = tkinter.Label(self, text = '可在目录中放置文件jpg.ignore，配置是否要跳过目录中的文件或子目录：')
        self.hintIgnore.grid(row=6, column=0, columnspan=4, sticky=tkinter.W, padx=10)
        self.hintIgnoreKey = tkinter.Label(self, text = '写入ignore_file = 1可跳过文件；写入ignore_path = 1可跳过子目录')
        self.hintIgnoreKey.grid(row=7, column=0, columnspan=4, sticky=tkinter.W, padx=10)

    def setDefault(self):
        self.inputPath.set(r'E:\photo\_ to clean up')
        self.matchStr.set('%Y-%m-%d')

    def sel_input(self):
        inputPath = tkinter.filedialog.askdirectory(initialdir = self.inputPath.get())
        if inputPath:
            self.inputPath.set(inputPath)
            self.check_ok()

    def check_input_path(self, path_after):
        if not path_after:
            self.btnOK.configure(state = tkinter.DISABLED)
        else:
            self.check_ok(inputPath=path_after)
        return True

    def sel_option(self):
        self.checkSubPath['state'] = 'normal' if self.choiceOption.get() == READ_EXIF or self.choiceOption.get() == MODIFY_DATE else 'disabled'
        self.editUserStr['state'] = 'normal' if self.choiceOption.get() == FIXED_DATE else 'disabled'
        self.editMatchStr['state'] = 'normal' if self.choiceOption.get() == MODIFY_DATE else 'disabled'
        self.check_ok()

    def check_user_str(self, user_str_after):
        if not user_str_after:
            self.btnOK.configure(state = tkinter.DISABLED)
        else:
            self.check_ok(addStr = user_str_after)
        return True

    def check_match_str(self, match_str_after):
        if not match_str_after:
            self.btnOK.config(state = tkinter.DISABLED)
        else:
            self.check_ok(addStr=match_str_after)
        return True

    def check_ok(self, inputPath = '', addStr = ''):
        if not inputPath:
            inputPath = self.inputPath.get()

        is_ok = True
        
        if not inputPath or not os.path.isdir(inputPath):
            is_ok = False
        elif self.choiceOption.get() == FIXED_DATE:
            if not addStr:
                addStr = self.userStr.get()
            is_ok = is_valid_date_prefix(addStr)
        elif self.choiceOption.get() == MODIFY_DATE:
            if not addStr:
                addStr = self.matchStr.get()
            if not addStr:
                is_ok = False
        if is_ok:
            self.btnOK.configure(state = tkinter.NORMAL)
        else:
            self.btnOK.configure(state = tkinter.DISABLED)

    def ok(self):
        inputPath = self.inputPath.get()
        if self.choiceOption.get() == READ_EXIF:
            subPath = self.selSubPath.get() != 0
            numRenamed = loop_dir(inputPath, subPath, rename_jpg, '')
        elif self.choiceOption.get() == FIXED_DATE:
            userStr = self.userStr.get()
            numRenamed = loop_dir(inputPath, False, rename_jpg, userStr)
        elif self.choiceOption.get() == MODIFY_DATE:
            subPath = self.selSubPath.get() != 0
            matchStr = self.matchStr.get()
            numRenamed = loop_dir(inputPath, subPath, modify_date, matchStr)
        tkinter.messagebox.showinfo('Finish', str(numRenamed) + '个文件重命名成功!!!!')

if __name__ == '__main__':
    root = Application()
    root.mainloop()
