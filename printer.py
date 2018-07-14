importance = ("36","32","33","31","43","31;42","31;43","41","33;41",)
def iprint(message,imp):
    print("\033["+importance[imp]+"m", message, "\033[0m")