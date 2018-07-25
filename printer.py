importance = ("36","32","33","31","43","31;42","31;43","41","33;41",)
def iprint(message,imp):
    color = str(importance[imp])
    message = massage.replace('\n','\033[0m\n' + color)
    print("\033["+ color +"m", message, "\033[0m")

def getInput(message, default, nonAccepts = ("",))
    msg = message + " [" + default + "] :"
    out = input(msg)
    if out in nonAccepts:
        out = default
    return out

def space(num):
    for i in range(num):
        print("\n")