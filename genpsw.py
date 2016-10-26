import random
import string

def allow_chars(allowNum, allowA2Z, allowSpe):
    '''
    >>> allow_chars(False, False, False)
    '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%&*'
    >>> allow_chars(True, False, False)
    '0123456789'
    >>> allow_chars(False, True, False)
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    >>> allow_chars(False, False, True)
    '!@#$%&*'
    '''
    if not allowNum and not allowA2Z and not allowSpe:
        allowNum = allowA2Z = allowSpe = True
    strAllow = ''
    if allowNum:
        strAllow = strAllow + string.digits
    if allowA2Z:
        strAllow = strAllow + string.ascii_letters
    if allowSpe:
        strAllow = strAllow + '!@#$%&*'
    return strAllow

def gen_psw(nn, strAllow):
    if not strAllow:
        return ''
    strPsw = ''
    while len(strPsw) < nn:
        strPsw = strPsw + random.choice(strAllow)
    return strPsw


if __name__ == '__main__':
    usrinput = input('allow num? (Y/N): ').upper()
    allowNum = usrinput != 'N'
    usrinput = input('allow A-Z and a-z? (Y/N): ').upper()
    allowA2Z = usrinput != 'N'
    usrinput = input('allow spec? (Y/N): ').upper()
    allowSpe = usrinput != 'N'
    strAllow = allow_chars(allowNum, allowA2Z, allowSpe)

    nn = int(input("password length: "))
    if nn >= 6 and nn < 20:
        usrinput = 'Y'
        while usrinput != 'N':
            print(gen_psw(nn, strAllow))
            usrinput = input('generate again? (Y/N): ').upper()
    else:
        print('wrong password length!!!!')
        print('exit!!!!')
    input("press any key to continue...")



 
