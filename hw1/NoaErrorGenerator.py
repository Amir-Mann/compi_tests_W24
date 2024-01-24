import random
import string

def setProb(dictonary, toSet, value):
    for key in toSet:
        dictonary[key] = value



def rndChar():
    printable = {chr(c): 20 if chr(c) in string.ascii_letters else 1 for c in range(0X20,0X7E+1)}
    return random.choices(list(printable.keys()), weights=list(printable.values()), k=1)[0]


def rndBool(true = 8, false = 2):
    return random.choices([True, False], [true, false])[0]


def rndId():
    idLen = random.randrange(1,15,1);
    id = [random.choice(string.ascii_letters)] + random.choices(string.ascii_letters+string.digits, k = idLen)
    if not rndBool():
        id = [random.choice(string.digits)] + id
    return "".join(id)

# return a string of hex with lower/upper letters
def hexStr(num):
    l = list(hex(num)[2:])
    if len(l) < 2 and rndBool(7,3):
        l = ["0"] + l
    for i in range(len(l)):
        if rndBool():
            l[i] = l[i].upper()
    # l = ["\\x"] + l
    return "".join(l)

def validHex():
    validHex = list(range(0X20, 0X7E + 1))
    return hexStr(random.choice(validHex))

def invalidHex():
    inValidHex = list(range(0X00, 0X20)) + list(range(0X7F, 0XFF))
    return hexStr(random.choice(inValidHex))

# return a string representation of valid/invalid hex
def rndHex():
    if rndBool():
        return validHex()
    return invalidHex()


def rndEscapeSeq():
    if rndBool():
        valid = ["x"+validHex(), "\\", "n", "r", "t", "0", "\"", "\\\\"]
        return "\\" + random.choice(valid)
    else:
        return "\\" + random.choice([rndChar(), "x"+invalidHex()])

def rndNum():
    number = str(random.randrange(0, 100000, 1))
    if not rndBool():
        return "0" * random.randrange(1, 3, 1) + number
    return number

def rndString():
    len = random.randrange(0, 20, 1)
    str = "\""
    for i in range(len):
        opt = [rndNum(), rndChar(), rndId(), rndEscapeSeq(), rndEscapeSeq(), rndEscapeSeq()]
        str += random.choice(opt)
        if rndBool():
            str += " "
    if rndBool(1,100):
        str += "\\"
    if rndBool():
        str + "\""
    return str




def getLine():
    line_len = 10
    WHITE_SPACES = [" ", "\t", "\n", "\r"]
    SAVED_WORDS = ["void", "int", "byte", "b", "bool", "and", "or", "not", "true", "false", "return", "if", "else",
                   "while", "break", "continue",";", "(", ")", "{", "}", "=", "==", "!=", "<", ">", "<=", ">=", "+", "-", "*", "/"]
    opt = {}
    for i in range(line_len):
        opt[rndString()] = 20
    for i in range(line_len):
        opt[rndId()] = 10
    opt.update({word : 10 for word in SAVED_WORDS})
    opt.update({word : 2 for word in WHITE_SPACES})
    opt[" "] = 20
    line = random.choices(list(opt.keys()), weights = list(opt.values()), k = line_len)
    return "".join(line)


def main():
    lines_num = 10
    for i in range(lines_num):
        print(getLine())

if __name__ == '__main__':
    main()