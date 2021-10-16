import tkinter as tk
from PIL import Image,ImageTk
import test
import threading
import tkinter.font as tkFont

# initial the window of demonstration
window = tk.Tk()
window.title('Bike-counting System')
window.geometry('1100x600')
window.resizable(width=False, height=False)



canvas = tk.Canvas(
    window,
    height = 500,
    width = 500
)

bk=Image.open("background.jpg")
bk = bk.resize((500,500),Image.ANTIALIAS)
bk=ImageTk.PhotoImage(bk)

image = canvas.create_image(
    (0,0),
    anchor = 'nw',
    image = bk,
)

img=Image.open("images_1.jpeg")
img=ImageTk.PhotoImage(img)

WIDTH = img.width()
HEIGHT = img.height()

image = canvas.create_image(
    (0,0),
    anchor = 'nw',
    image = img
)

canvas.place(
    x = 10,
    y = 20,
    anchor = 'nw'
)

def move(_):
    canvas.moveto(image,x = scale_x.get()-WIDTH/2.0,y = scale_y.get()-HEIGHT/2.0)
    position.config(text = '当前位置：({:.2f},{:.2f})'.format(scale_x.get()-WIDTH/2.0,scale_y.get()-HEIGHT/2.0))

scale_x = tk.Scale(
    window,
    from_ = WIDTH/2.0,
    to = 500-WIDTH/2.0,
    length = 500-WIDTH,
    orient = tk.HORIZONTAL,
    showvalue = False,
    resolution = 0.01,
    command = move
)

scale_x.place(
    x = WIDTH/2.0,
    y = 550,
    anchor = 'nw'
)

scale_y = tk.Scale(
    window,
    from_ = HEIGHT/2.0,
    to = 500-HEIGHT/2.0,
    length = 500-WIDTH,
    orient = tk.VERTICAL,
    showvalue = False,
    resolution = 0.01,
    command = move
)

scale_y.place(
    x = 520,
    y = HEIGHT/2.0,
    anchor = 'nw'
)


var = tk.StringVar()


position = tk.Label(
    window,
    text = '当前位置：',
)

position.place(
    x = 0,
    y = 0,
    anchor = 'nw'
)
number = tk.Label(
    window,
    text = '',
    font=tkFont.Font(family='ComicSansMS', size=20, weight=tkFont.BOLD)
)

number.place(
    x = 550,
    y = 0,
    anchor = 'nw'
)



# initial another thread to measure the pressure distribution
thread = threading.Thread(target=test.From, args=(window,scale_x,scale_y,number))
thread.setDaemon(True)
thread.start()

# define the keyboard effect
def left(event):
    if scale_x.get()>=10:
        scale_x.set(scale_x.get()-10)
        move(None)

def right(event):
    if scale_x.get()<=470:
        scale_x.set(scale_x.get()+10)
        move(None)

def up(event):
    if scale_y.get()>=10:
        scale_y.set(scale_y.get()-10)
        move(None)

def down(event):
    if scale_y.get()<=470:
        scale_y.set(scale_y.get()+10)
        move(None)
    
# define the keyboard event
window.bind("<Left>",left)
window.bind("<Right>",right)
window.bind("<Up>",up)
window.bind("<Down>",down)

window.mainloop()

