from yaki.imports import *

class ToolTip():
    def __init__(self, widget, text="default tooltip"):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Motion>", self.motion)
        self.widget.bind("<Leave>", self.leave)
        self.id = None
        self.tw = None
    def enter(self, event):
        self.schedule()

    def motion(self, event):
        self.unschedule()
        self.schedule()

    def leave(self, event):
        self.unschedule()
        self.id = self.widget.after(100, self.hideTooltip)

    def schedule(self):
        if self.tw:
            return
        self.unschedule()
        self.id = self.widget.after(100, self.showTooltip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showTooltip(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)
        x, y = self.widget.winfo_pointerxy()
        self.tw = Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.attributes("-topmost", True)
        self.tw.geometry(f"+{x+10}+{y+10}")
        label = Label(self.tw, text=self.text, background="lightyellow",
                         relief="solid", borderwidth=1, justify="left")
        label.pack(ipadx=10)
    def hideTooltip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


class MyListBox(Listbox):
    def __init__(self, master, inlist, **kwargs):
        super().__init__(master, **kwargs)
        self.inlist = inlist
        for i in inlist:
            self.insert(END, i)

    def insert_inlist(self, inlist):
        self.inlist = inlist
        self.delete(0, END)
        for i in inlist:
            self.insert(END, i)

    def pack1(self, **kwargs):
        super().pack(**kwargs)


class ScrolledList(MyListBox):
    def __init__(self, master, **kwargs):
        self.frame=ttk.Frame(master)
        super().__init__(self.frame, **kwargs)
        self.scrollbar = ttk.Scrollbar(self.frame, orient=VERTICAL, command=self.yview)
        self.configure(yscrollcommand=self.scrollbar.set)
        self.pack1(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=LEFT, fill=Y)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

    def place(self, **kwargs):
        self.frame.place(**kwargs)


class RightClickMenu(Menu):
    def __init__(self, master,func,tree_rclick=False,list_rclick=False, **kwargs): # func = [[label,command],[label,command]...]
        def showMenu(e):
            if tree_rclick:
                x, y = e.x, e.y
                item = master.identify_row(y)
                if item:
                    master.selection_set(item)
                    master.focus(item)
                else:
                    # アイテムがない場合は選択を解除する
                    master.selection_remove(master.selection())
            elif list_rclick:
                x, y = e.x, e.y
                item = master.nearest(y)
                #if item:
                #print(item)
                master.select_clear(0, END)
                master.selection_set(item)

            self.post(e.x_root, e.y_root)

        kwargs['tearoff'] = 0
        Menu.__init__(self, master, **kwargs)
        master.bind("<Button-3>", showMenu)

        for i in range(len(func)):
            self.add_command(label=func[i][0], command=func[i][1])


class SortTreeview(ttk.Treeview):
    # columns = [[A,B,C],[D,E,F]...]
    # arrRows = list(string)
    # arrColWidth = list(num)
    # arrColAlignment = list(e,w,center)
    # arrSortType = list(name,num,date,multidecimal,numcomma)

    def __init__(self,master,arrRows,arrColWidth=[],arrColAlignment=[],arrSortType=[],**kwargs):
        kwargs['show'] ="headings"
        self.kwargs=kwargs
        self.master=master
        super().__init__(self.master,**kwargs)
        self.arrlbHeader = kwargs["columns"]
        self.arrRows = arrRows

        if arrColWidth==[]:
            self.width=[100 for i in range(len(self.arrlbHeader))]
        else:
            self.width=arrColWidth

        if arrColAlignment==[]:
            self.alignment=["center" for i in range(len(self.arrlbHeader))]
        else:
            self.alignment=arrColAlignment

        if arrSortType==[]:
            self.sorttype=["name" for i in range(len(self.arrlbHeader))]
        else:
            self.sorttype=arrSortType
        for iCount in range(len(self.arrlbHeader)):
            strHdr = self.arrlbHeader[iCount]
            self.heading(strHdr, text=strHdr.title(), sort_by=self.sorttype[iCount])
            self.column(self.arrlbHeader[iCount], width=self.width[iCount], stretch=True, anchor=self.alignment[iCount])
        for iCount in range(len(self.arrRows)):
            self.insert("", "end", values=self.arrRows[iCount])

    def heading(self, column, sort_by=None, **kwargs):
        if sort_by and not hasattr(kwargs, 'command'):
            func = getattr(self, f"_sort_by_{sort_by}", None)
            if func:
                kwargs['command'] = partial(func, column, False)
        return super().heading(column, **kwargs)

    def _sort(self, column, reverse, data_type, callback):
        l = [(self.set(k, column), k) for k in self.get_children('')]
        l.sort(key=lambda t: data_type(t[0]), reverse=reverse)
        for index, (_, k) in enumerate(l):
            self.move(k, '', index)
        self.heading(column, command=partial(callback, column, not reverse))

    def _sort_by_num(self, column, reverse):
        self._sort(column, reverse, int, self._sort_by_num)

    def _sort_by_name(self, column, reverse):
        self._sort(column, reverse, str, self._sort_by_name)

    def _sort_by_date(self, column, reverse):
        def _str_to_datetime(string):
            return datetime.datetime.strptime(string, "%Y-%m-%d")
        self._sort(column, reverse, _str_to_datetime, self._sort_by_date)

    def _sort_by_multidecimal(self, column, reverse):
        def _multidecimal_to_str(string):
            arrString = string.split(".")
            strNum = ""
            for iValue in arrString:
                strValue = f"{int(iValue):02}"
                strNum = "".join([strNum, str(strValue)])
            strNum = "".join([strNum, "0000000"])
            return int(strNum[:8])
        self._sort(column, reverse, _multidecimal_to_str, self._sort_by_multidecimal)

    def _sort_by_numcomma(self, column, reverse):
        def _numcomma_to_num(string):
            return int(string.replace(",", ""))
        self._sort(column, reverse, _numcomma_to_num, self._sort_by_numcomma)

    def pack1(self, **kwargs):
        super().pack(**kwargs)

    def configure_arr(self, arrRows=[[]]):
        self.arrRows = arrRows
        for item in self.get_children():
            self.delete(item)

        for iCount in range(len(self.arrlbHeader)):
            strHdr = self.arrlbHeader[iCount]
            self.heading(strHdr, text=strHdr.title(), sort_by=self.sorttype[iCount])
            self.column(self.arrlbHeader[iCount], width=self.width[iCount], stretch=True, anchor=self.alignment[iCount])
        for iCount in range(len(self.arrRows)):
            self.insert("", "end", values=self.arrRows[iCount])

class ScrolledTree(SortTreeview):
    def __init__(self, master, **kwargs):
        self.frame=ttk.Frame(master)
        super().__init__(self.frame, **kwargs)
        self.scrollbar = ttk.Scrollbar(self.frame, orient=VERTICAL, command=self.yview)
        self.configure(yscrollcommand=self.scrollbar.set)
        self.pack1(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=LEFT, fill=Y)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

    def place(self, **kwargs):
        self.frame.place(**kwargs)

class Free_window(Toplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Toplevelウィンドウにフォーカスが当たったときに親ウィンドウを非表示にする
        if hide_mainwindow==1:
            self.bind("<FocusIn>", hide_parent)

        # Toplevelウィンドウからフォーカスが外れたときに親ウィンドウを再表示する
        #self.bind("<FocusOut>", show_parent)

    def move_window(self,wiget):
        self.isMouseDown = False

        def mouseDown(event):
            self.isMouseDown = True
            self.origin = (event.x, event.y)

        def mouseRelease(event):
            self.isMouseDown = False

        def mouseMove(event):
            if self.isMouseDown:
                x = self.winfo_x() + (event.x - self.origin[0])
                y = self.winfo_y() + (event.y - self.origin[1])
                self.geometry("+%s+%s" % (x, y))

        wiget.bind("<Button>", mouseDown)
        wiget.bind("<ButtonRelease>", mouseRelease)
        wiget.bind("<Motion>", mouseMove)

class ScrolledText(scrolledtext.ScrolledText):
    def __init__(self, *args, **kwargs):
        kwargs['undo'] = True
        kwargs["font"]=("BIZ UDPGothic",)
        #kwargs["bg"]=rgbToHex((40, 40, 40))
        #kwargs["fg"]=rgbToHex((230, 230, 230))
        #kwargs["insertbackground"]=rgbToHex((255, 255, 255))
        super().__init__(*args, **kwargs)

class Tk(ThemedTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

class Searchbox(ttk.Combobox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        val_list=kwargs["values"]
        list_button=val_list.copy()
        val_list = StringVar()
        self.configure(textvariable=val_list)

        def handle_keypress(event):
            if event.keysym == 'Return':
                self.event_generate('<Down>')
            elif event.keysym == 'Delete':
                self.delete(0,END)

        def on_combobox_key_release(event):
            current_text = val_list.get()
            filtered_list = [item for item in list_button if current_text.lower() in item.lower()]
            self["values"] = filtered_list

        self.bind('<KeyRelease>', on_combobox_key_release)
        self.bind('<KeyPress>', handle_keypress)
