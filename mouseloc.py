import pyautogui

# Func


def double(a):
    b = "%.2f" % round(a, 2)
    return float(b)


# Code
print('Press Ctrl-C to quit.')
try:
    while True:
        x, y = pyautogui.position()
        x = double(x * 65535 / 2880)
        y = double(y * 65535 / 1920)
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4) + ' Cords:' + str(x).rjust(4) + ',' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
except KeyboardInterrupt:
    print('\n')


