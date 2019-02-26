from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from TkExtra import *
from PIL import Image, ImageTk


class TitleBar(Canvas):
    def __init__(self, parent, title=None, Fullscreen=True, Resize=False):
        Canvas.__init__(self, parent)
        self.parent = parent
        self._White = "white"
        self._Black = "black"
        grid(self, 1,50)
        parent.wm_overrideredirect(1)
        parent.wm_overrideredirect(0)
        parent.createcommand('tk::mac::ReopenApplication', parent.deiconify)
        
        self.configure(height=25, highlightthickness=0)
        self.grid_propagate(0)

        self.Title  = Label(self, text=title)
        self.Title.grid(row=0, columnspan=51, column=0, pady=(3,0))

        self.Sep1=ttk.Separator(self, orient=HORIZONTAL)
        self.Sep1.grid(row=1, columnspan=51, column=0, sticky=N+S+E+W)

        self._Drag_Window()
        
        if not Fullscreen: self._Close_Minimise()
        else: self._Close_Minimise_Fullscreen()

        if Resize:
            self.grip = ttk.Sizegrip(self.parent)
            self.grip.place(relx=1.0, rely=1.0, anchor="se")
            self.grip.bind("<B1-Motion>", self.OnMotion)
        
        self._settings()
    
    def _settings (self):
        try: self.pack_configure(side=TOP, fill=X)
        except: self.grid_configure(sticky=N+S+E+W)
        else: return


    # Need fixes
    def OnMotion(self, evt=None):
        self.update_idletasks()
        self.parent.update_idletasks()
        self.Box.update_idletasks()
        self.update_idletasks()
        x1 = self.winfo_pointerx()
        y1 = self.winfo_pointery()
        x0 = self.winfo_rootx()
        y0 = self.winfo_rooty()
        self.parent.geometry("%sx%s" %((x1-x0),(y1-y0)))
        return

    # Need fixes
    def Resize(self, evt):
        # if evt.x<self.parent.winfo_width() and evt.y<self.parent.winfo_height():
        if evt.x>=self.parent.winfo_width()-5 and evt.y>=self.parent.winfo_height()-5:
            self.OnMotion()
        elif evt.x>=self.parent.winfo_width()-5:
            self.OnMotion()
        elif evt.y>=self.parent.winfo_height()-5:
            self.OnMotion()
        else:self.parent.config(cursor="")
        # else:self.parent.config(cursor="")
   
    # Need fixes
    def Resize_Arrow(self, evt):
        if evt.x<self.parent.winfo_width() and evt.y<self.parent.winfo_height():
            if evt.x>=self.parent.winfo_width()-5 and evt.y>=self.parent.winfo_height()-5:
                self.parent.config(cursor="bottom_right_corner")
            elif evt.x>=self.parent.winfo_width()-5:
                self.parent.config(cursor="sb_h_double_arrow")
            elif evt.y>=self.parent.winfo_height()-5:
                self.parent.config(cursor="sb_v_double_arrow")
            else:self.parent.config(cursor="")
        else:self.parent.config(cursor="")

    def _Close_Minimise(self):
        self.Box = Canvas(self,width=70, height=27, highlightthickness=0)
        self.Box.grid(row=0, column=50)
        self.Box.create_roundsqaure(5, 3, 60, 17, 8, "black", "Lines", "Curves")

        self.Box.create_circle(19.5, 11.5, 7, fill='#80b4f4', width=0, state="hidden", tags="minihigh")
        self.Box.create_circle(51.0, 11.5, 7, fill='#80b4f4', width=0, state="hidden", tags="closehigh")

        self.Box.create_text(20, 9.5, text="-", font=Font(weight="bold"), tags="minimise")
        self.Box.create_text(50, 9.5, text="×", font=Font(weight="bold"), tags="close")

        def Enter_Close(evt):
            self.Box.itemconfig("close", fill="#7e7e7e")
            self.Box.itemconfig("closehigh", state="normal")
        
        def Leave_Close(evt):
            self.Box.itemconfig("close", fill=self._Black)
            self.Box.itemconfig("closehigh", state="hidden")
        
        def Enter_Mini(evt):
            self.Box.itemconfig("minimise", fill="#7e7e7e")
            self.Box.itemconfig("minihigh", state="normal")
        
        def Leave_Mini(evt):
            self.Box.itemconfig("minimise", fill=self._Black)
            self.Box.itemconfig("minihigh", state="hidden")
        
        def Click_Mini(evt):
            Leave_Mini(None)
            self.after(1,self.parent.withdraw)            

        self.Box.tag_bind("minimise", "<Enter>", Enter_Mini)
        self.Box.tag_bind("minimise", "<Leave>", Leave_Mini)
        self.Box.tag_bind("minimise", "<Button-1>", Click_Mini)
        self.Box.tag_bind("close", "<Button-1>", lambda e: self.parent.quit())
        self.Box.tag_bind("close","<Enter>", Enter_Close)
        self.Box.tag_bind("close","<Leave>", Leave_Close)

    def _Close_Minimise_Fullscreen(self):
        self.Fullscreen=False
        self.Box = Canvas(self,width=90, height=27, highlightthickness=0)
        self.Box.grid(row=0, column=50)
        self.Box.create_roundsqaure(5, 3, 80, 17, 8, "black", "Lines", "Curves")

        self.Box.create_circle(19.5, 11.5, 7, fill='#80b4f4', width=0, state="hidden", tags="minihigh")
        self.Box.create_circle(45.0, 11.5, 7, fill='#80b4f4', width=0, state="hidden", tags="fullshigh")
        self.Box.create_circle(70.5, 11.5, 7, fill='#80b4f4', width=0, state="hidden", tags="closehigh")

        self.Box.create_text(20.0, 9.5, text="-", font=Font(weight="bold"), tags="minimise")
        self.Box.create_text(45.0, 9.5, text="☐", font=Font(weight="bold"), tags="fulls")
        self.Box.create_text(70.0, 9.5, text="×", font=Font(weight="bold"), tags="close")

        def Enter_Close(evt):
            self.Box.itemconfig("close", fill="#7e7e7e")
            self.Box.itemconfig("closehigh", state="normal")
        
        def Leave_Close(evt):
            self.Box.itemconfig("close", fill=self._Black)
            self.Box.itemconfig("closehigh", state="hidden")
        
        def Enter_Full(evt):
            self.Box.itemconfig("fulls", fill="#7e7e7e")
            self.Box.itemconfig("fullshigh", state="normal")
        
        def Leave_Full(evt):
            self.Box.itemconfig("fulls", fill=self._Black)
            self.Box.itemconfig("fullshigh", state="hidden")

        def Click_Full(evt):
            if self.Fullscreen:
                self.parent.attributes("-fullscreen", False)
                self.Fullscreen=False
            else:
                self.parent.attributes("-fullscreen", True)
                self.Fullscreen=True

        def Enter_Mini(evt):
            self.Box.itemconfig("minimise", fill="#7e7e7e")
            self.Box.itemconfig("minihigh", state="normal")
        
        def Leave_Mini(evt):
            self.Box.itemconfig("minimise", fill=self._Black)
            self.Box.itemconfig("minihigh", state="hidden")
        
        def Click_Mini(evt):
            Leave_Mini(None)
            self.after(1,self.parent.withdraw)            

        self.Box.tag_bind("minimise", "<Enter>", Enter_Mini)
        self.Box.tag_bind("minimise", "<Leave>", Leave_Mini)
        self.Box.tag_bind("minimise", "<Button-1>", Click_Mini)
        self.Box.tag_bind("fulls", "<Enter>", Enter_Full)
        self.Box.tag_bind("fulls", "<Leave>", Leave_Full)
        self.Box.tag_bind("fulls", "<Button-1>", Click_Full)
        self.Box.tag_bind("close", "<Button-1>", lambda e: self.parent.quit())
        self.Box.tag_bind("close","<Enter>", Enter_Close)
        self.Box.tag_bind("close","<Leave>", Leave_Close)
    
    def _Drag_Window(self):
        self._offsetx = 0
        self._offsety = 0

        def SetGeo(evt):
            self.parent.update_idletasks()
            x = self.winfo_pointerx() - self._offsetx
            y = self.winfo_pointery() - self._offsety
            self.parent.geometry('+{x}+{y}'.format(x=x,y=y))

        def Offset(evt):
            self._offsetx = evt.x
            self._offsety = evt.y

        self.bind('<Button-1>',Offset)
        self.bind('<B1-Motion>',SetGeo)

    def icon(self, file):
        im_temp = Image.open(file)
        im_temp = im_temp.resize((20, 20), Image.ANTIALIAS)
        im_temp = ImageTk.PhotoImage(im_temp)
        self.iconlb = Label(self, image=im_temp)
        self.iconlb.image=im_temp
        self.iconlb.grid(row=0,column=0)
    
    def title(self, str):
        self.Title.config(text=str)

    def dark_mode(self):
        self._Black = "white"
        self.config(bg="black")
        self.Title.config(bg="black",fg="white")
        self.Box.config(bg="black")
        self.Box.itemconfig("Lines", fill="white")
        self.Box.itemconfig("Curves", outline="white")
        self.Box.itemconfig("minimise", fill="white")
        self.Box.itemconfig("fulls", fill="white")
        self.Box.itemconfig("close", fill="white")
    
    def light_mode(self):
        self._Black = "black"
        self.config(bg="white")
        self.Title.config(bg="white",fg="black")
        self.Box.config(bg="white")
        self.Box.itemconfig("Lines", fill="black")
        self.Box.itemconfig("Curves", outline="black")
        self.Box.itemconfig("minimise", fill="black")
        self.Box.itemconfig("fulls", fill="black")
        self.Box.itemconfig("close", fill="black")



# testing purposes
if __name__ == "__main__":
    root = Tk()
    root.geometry("500x200+100+100")

    TB = TitleBar(root, "Test", False)
    TB.pack()
    TB.dark_mode()
    # TB.icon("Icon.icns")

    root.mainloop()