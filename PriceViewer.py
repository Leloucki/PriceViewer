import shelve
import threading
import time
from tkinter import *
import requests

DEFAULT_POSITION = "+0+0"
s = shelve.open('test_shelf.db')
try:
    position = s['key1']['string']
except KeyError:
    position = DEFAULT_POSITION
finally:
    s.close()


def shelveOpen(e):
    s = shelve.open('test_shelf.db')
    try:
        s['key1'] = {'string': '+' + str(root.winfo_x()) + '+' + str(root.winfo_y())}
    finally:
        s.close()
    root.destroy()


def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y


def move_app(e):
    x, y = e.x - lastClickX + root.winfo_x(), e.y - lastClickY + root.winfo_y()
    root.geometry(f'+{x}+{y}')


def getCoin(root):
    while True:
        global label
        global coinN
        global coinN_label
        global fiat_label
        count = 0
        for i in coinN:

            if coinN_label[count]['text'] == '':
                coinN_label[count] = Label(root, text=i, bg='darkgreen', fg='white',
                                           font=("AppleGothic", 12))
                coinN_label[count].grid(row=count, column=0, pady=10, padx=10, sticky=W)

            if fiat_label[count]['text'] == '':
                fiat_label[count] = Label(root, text='R$', bg='black', fg='white', font=("AppleGothic", 12))
                fiat_label[count].grid(row=count, column=1, pady=10, padx=10, sticky=E)

            response = requests.get(f'https://www.mercadobitcoin.net/api/{i}/ticker').json()
            price = round(float(response['ticker']['last']), 2)
            if label[count]['text'] == '':
                label[count] = Label(root, text=f'{price:.2f}', bg='black', fg='white', font=("AppleGothic", 12))
                label[count].grid(row=count, column=2, pady=10, padx=10, sticky=E)
            elif float(label[count]['text']) != price:
                label[count].destroy()
                label[count] = Label(root, text=f'{price:.2f}', bg='black', fg='white', font=("AppleGothic", 12))
                label[count].grid(row=count, column=2, pady=10, padx=10, sticky=E)

            count = count + 1

        time.sleep(5)


root = Tk()
root.configure(background='black')
root.bind('<Button-1>', SaveLastClickPos)
root.bind('<B1-Motion>', move_app)
root.bind('<Double-Button-1>', shelveOpen)
root.overrideredirect(True)
root.attributes('-topmost', 1)
root.geometry(position)

coinN_label = [Label(root), Label(root), Label(root), Label(root)]
fiat_label = [Label(root), Label(root), Label(root), Label(root)]
coinN = ['BTC', 'ETH', 'ADA', 'USDC']
label = [Label(root), Label(root), Label(root), Label(root)]
t1 = threading.Thread(target=getCoin, args=(root,))
t1.daemon = True
t1.start()

root.mainloop()
