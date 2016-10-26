import string

def translate_one(cc, lst, nn):
    '''
    >>> translate_one('a', 'abcde', 2)
    'c'
    >>> translate_one('a', 'abcde', 4)
    'e'
    >>> translate_one('a', 'abcde', 5)
    'a'
    '''
    idx = lst.find(cc) + nn
    if idx >= len(lst):
        idx -= len(lst)
    return lst[idx : idx + 1]

def translate_text(ss, nn, na, nA):
    nums = string.digits
    lows = string.ascii_lowercase
    upps = string.ascii_uppercase
    
    s1 = ''
    for cc in ss:
        if cc in nums:
            cc = translate_one(cc, nums, nn)
        elif cc in lows:
            cc = translate_one(cc, lows, na)
        elif cc in upps:
            cc = translate_one(cc, upps, nA)
        else:
            pass
        s1 = s1 + cc
    return s1;

if __name__ == '__main__':
    nn = int(input('numeric: '))
    na = int(input('lower: '))
    nA = int(input('upper: '))
    ss = input('your text or enter to quit: ')
    while ss:
        ss = translate_text(ss, nn, na, nA)
        print(ss)
        ss = input('your text or enter to quit: ')
     
