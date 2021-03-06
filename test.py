import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image,ImageTk,ImageDraw
import os
import numpy as np
import matplotlib.pyplot as plt

x1 = 0
y1 = 0
x2 = 0
y2 = 0
rect_id = None
new_img = False
flag = 0
canvas = None
img_list = []

def openFile():
    if (btn3['state'] == 'normal'):
        btn3.config(state='disabled')
    if (btn4['state'] == 'normal'):
        btn3.config(state='disabled')
    window.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                      filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))
    fn.set(window.filename)
    displayFile()


def displayFile():
    global canvas,cropInitiated,new_img,img_list
    if not new_img:
        new_img = True
        img_list=[]
    try:
        filename = fn.get()
        img = Image.open(filename).convert('RGB')
        photo = ImageTk.PhotoImage(img)
        W, H = img.size
        if canvas is not None:
            canvas.destroy()
        canvas = tk.Canvas(window,width=W,height=H)
        canvas.grid(row=1,column=1)
        canvas.create_image(0,0,image=photo,anchor=tk.NW)
        canvas.img = photo
        if(btn3['state']=='disabled'):
            btn3.config(state='normal')
    except AttributeError:
        messagebox.showwarning('Warning', 'No file selected')


def startCrop():
    canvas.bind('<ButtonPress-1>',start)
    canvas.bind('<B1-Motion>', drag)
    canvas.bind('<ButtonRelease-1>',stop)

def start(event):
    global x1, y1,rect_id
    x1, y1 = event.x, event.y
    rect_id = canvas.create_rectangle(x1, y1, x2, y2, fill='', outline='red', width=2)
    # print('{}, {}'.format(x1, y1))

def drag(event):
    global x2, y2,rect_id
    x2, y2 = event.x, event.y
    # print('{}, {}'.format(x2, y2))
    canvas.coords(rect_id, x1, y1, x2, y2)

def stop(event):
    global x2, y2,flag,img_list
    x2, y2 = event.x, event.y
    # print('{}, {}'.format(x2, y2))
    flag=1
    if btn4['state'] == 'disabled':
        btn4.config(state='normal')
    img = Image.open(fn.get()).convert('RGB')
    cropped = img.crop((x1,y1,x2,y2))
    img_list.append(cropped)

def saveFiles():
    global cropInitiated,new_img,img_list
    folder_selected = filedialog.askdirectory()
    print(folder_selected)
    if new_img:
        os.chdir(folder_selected)
        new_img = False
    dir_name = os.path.split(fn.get())[1]
    if len(dir_name):
        dir_name = 'cropped_images_'+dir_name[0:dir_name.rindex('.')]
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        os.chdir(dir_name)
        for i in range(len(img_list)):
            # i.show()
            img_list[i].save(str(i)+'.jpg')
        if len(os.listdir('.')) == 0:
            messagebox.showinfo('Status','No images saved')
            window.destroy()
        else:
            messagebox.showinfo('Status','Cropped images saved successfully')
            window.protocol("WM_DELETE_WINDOW", my_function)

def my_function():
    global flag
    curr_file_path = os.getcwd()
    if flag == 1:
        window.destroy()
        print(curr_file_path)
        im = []
        ax = []
        fig = plt.figure(figsize=(9, 9))
        for file in os.listdir(curr_file_path):
            im.append(Image.open(file))
        for i in range(len(im)):
            img = im[i]
            ax.append(fig.add_subplot(3, 3, i + 1))
            plt.imshow(img)
        plt.show()
    else:
        window.destroy()

window = tk.Tk()
window.geometry('900x600')
window.resizable(height=True, width=True)
window.title('Test App')
fn = tk.StringVar()
filepath = tk.Entry(window, text=fn,width=60,font=('arial',12))
filepath.grid(row=0,column=1)
lbl = tk.Label(window,text='Upload Image Path: ').grid(row=0,column=0)
btn1 = tk.Button(window,text='Upload',bg='brown',fg='white',relief='raised',font=('arial',12),command=openFile).grid(row=0,column=2)
btn3 = tk.Button(window, text='Crop', state='disabled',bg='brown', fg='white', relief='raised', font=('arial', 12),command=startCrop)
btn4 = tk.Button(window, text='Save',bg='brown', state='disabled',fg='white', relief='raised', font=('arial', 12),command=saveFiles)
btn3.grid(row=0, column=3)
btn4.grid(row=0, column=4)
window.mainloop()

