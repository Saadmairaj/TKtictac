import platform

import tkinter as tk
import tkmacosx as tkm

# from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from TkExtra import Canvas, grid
from PIL import Image, ImageTk


class TitleBar(Canvas):
    def __init__(self, parent, title=None, fullscreen=True, Resize=False):
        Canvas.__init__(self, parent)
        self.parent = parent

        self['bg'] = self._white = tkm.ColorVar(value='white')
        self._black = tkm.ColorVar(value='black')

        grid(self, 1, 50)
        parent.wm_overrideredirect(1)
        if platform.system() == 'Darwin':
            parent.wm_overrideredirect(0)
            parent.createcommand(
                'tk::mac::ReopenApplication', parent.deiconify)

        self.configure(height=25, highlightthickness=0)
        self.grid_propagate(0)

        self._title = tk.Label(
            self, text=title, fg=self._black, bg=self._white)
        self._title.grid(row=0, columnspan=51, column=0, pady=(3, 0))

        self.sep1 = ttk.Separator(self, orient='horizontal')
        self.sep1.grid(row=1, columnspan=51, column=0, stick='nsew')

        self._dragw_window()

        self._window_protocols(fullscreen)
        # if not fullscreen:
        #     self._window_protocols()
        # else:
        #     self._window_protocols(True)

        if Resize:
            self.grip = ttk.Sizegrip(self.parent)
            self.grip.place(relx=1.0, rely=1.0, anchor="se")
            self.grip.bind("<B1-Motion>", self.on_motion)

        self._settings()

    def _settings(self):
        try:
            self.pack_configure(side='top', fill='x')
        except:
            self.grid_configure(sticky='nsew')
        else:
            return

    # Need fixes
    def on_motion(self, evt=None):
        self.update_idletasks()
        self.parent.update_idletasks()
        self._box.update_idletasks()
        self.update_idletasks()
        x1 = self.winfo_pointerx()
        y1 = self.winfo_pointery()
        x0 = self.winfo_rootx()
        y0 = self.winfo_rooty()
        self.parent.geometry("%sx%s" % ((x1-x0), (y1-y0)))
        return

    # Need fixes
    def Resize(self, evt):
        # if evt.x<self.parent.winfo_width() and evt.y<self.parent.winfo_height():
        if evt.x >= self.parent.winfo_width()-5 and evt.y >= self.parent.winfo_height()-5:
            self.on_motion()
        elif evt.x >= self.parent.winfo_width()-5:
            self.on_motion()
        elif evt.y >= self.parent.winfo_height()-5:
            self.on_motion()
        else:
            self.parent.config(cursor="")
        # else:self.parent.config(cursor="")

    # Need fixes
    def resize_arrow(self, evt):
        if evt.x < self.parent.winfo_width() and evt.y < self.parent.winfo_height():
            if evt.x >= self.parent.winfo_width()-5 and evt.y >= self.parent.winfo_height()-5:
                self.parent.config(cursor="bottom_right_corner")
            elif evt.x >= self.parent.winfo_width()-5:
                self.parent.config(cursor="sb_h_double_arrow")
            elif evt.y >= self.parent.winfo_height()-5:
                self.parent.config(cursor="sb_v_double_arrow")
            else:
                self.parent.config(cursor="")
        else:
            self.parent.config(cursor="")

    def _window_protocols(self, fullscreen=False):
        # All thte bind functions.
        def enter_close(evt):
            self._box.itemconfig("close", fill="#7e7e7e")
            self._box.itemconfig("closehigh", state="normal")

        def leave_close(evt):
            self._box.itemconfig("close", fill=self._black)
            self._box.itemconfig("closehigh", state="hidden")

        def enter_mini(evt):
            self._box.itemconfig("minimise", fill="#7e7e7e")
            self._box.itemconfig("minihigh", state="normal")

        def leave_mini(evt):
            self._box.itemconfig("minimise", fill=self._black)
            self._box.itemconfig("minihigh", state="hidden")

        def click_mini(evt):
            leave_mini(None)
            self.after(1, self.parent.withdraw)

        def enter_full(evt):
            self._box.itemconfig("fulls", fill="#7e7e7e")
            self._box.itemconfig("fullshigh", state="normal")

        def leave_full(evt):
            self._box.itemconfig("fulls", fill=self._black)
            self._box.itemconfig("fullshigh", state="hidden")

        def click_full(evt):
            if self.fullscreen:
                self.parent.attributes("-fullscreen", False)
                self.fullscreen = False
            else:
                self.parent.attributes("-fullscreen", True)
                self.fullscreen = True

        w = 80 if fullscreen else 60
        x = 70 if fullscreen else 50

        # Initialise canvas
        self._box = Canvas(self, width=w+10, height=27,
                           highlightthickness=0, bg=self._white)
        self._box.grid(row=0, column=50)

        self._box.create_roundsqaure(5, 3, w, 17, 8, tags="box", style='arc')
        self._box.create_circle(
            19.5, 11.5, 7, fill='#80b4f4', width=0, state="hidden", tags="minihigh")
        self._box.create_circle(
            x, 11.5, 7, fill='#80b4f4', width=0, state="hidden", tags="closehigh")
        self._box.create_text(
            20, 11, text="-", font=Font(weight="bold"), fill=self._black, tags="minimise")
        self._box.create_text(x-4, 11, text="×", font=Font(weight="bold"),
                              fill=self._black, tags="close", anchor='w')

        if fullscreen:
            self._box.create_circle(
                45, 11.5, 7, fill='#80b4f4', width=0, state="hidden", tags="fullshigh")
            self._box.create_text(45, 11, text="☐", font=Font(
                weight="bold"), fill=self._black, tags="fulls")
            self._box.tag_bind("fulls", "<Enter>", enter_full)
            self._box.tag_bind("fulls", "<Leave>", leave_full)
            self._box.tag_bind("fulls", "<Button-1>", click_full)

        # All tag binds.
        self._box.tag_bind("minimise", "<Enter>", enter_mini)
        self._box.tag_bind("minimise", "<Leave>", leave_mini)
        self._box.tag_bind("minimise", "<ButtonRelease-1>", click_mini)
        self._box.tag_bind("close", "<ButtonRelease-1>",
                           lambda e: self.parent.quit())
        self._box.tag_bind("close", "<Enter>", enter_close)
        self._box.tag_bind("close", "<Leave>", leave_close)

    def _dragw_window(self):
        self._offsetx = 0
        self._offsety = 0

        def setgeo(evt):
            self.parent.update_idletasks()
            x = self.winfo_pointerx() - self._offsetx
            y = self.winfo_pointery() - self._offsety
            self.parent.geometry('+{x}+{y}'.format(x=x, y=y))

        def offset(evt):
            self._offsetx = evt.x
            self._offsety = evt.y

        self.bind('<Button-1>', offset)
        self.bind('<B1-Motion>', setgeo)

    def icon(self, file):
        im = Image.open(file)
        im_temp = im.resize((20, 20), Image.ANTIALIAS)
        im_temp = ImageTk.PhotoImage(im_temp)
        self.iconlb = tk.Canvas(self, width=20, height=20, bg=self._white, highlightthickness=0)
        self.iconlb.create_image(0, 0, image=im_temp, anchor='nw')
        self.iconlb.image = im_temp
        self.iconlb.grid(row=0, column=0)
        self.parent.iconphoto(True, ImageTk.PhotoImage(im))

    def title(self, str):
        self._title.config(text=str)

    def dark_mode(self):
        self._white.set('black')
        self._black.set('white')
        self._box.itemconfig("box", outline='white')

    def light_mode(self):
        self._white.set('white')
        self._black.set('black')
        self._box.itemconfig("box", outline='black')


# testing purposes
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x200+100+100")

    TB = TitleBar(root, "Test", True)
    TB.pack()
    TB.dark_mode()
    root.after(1000, TB.light_mode)
    # TB.icon("Icon.icns")

    root.mainloop()
