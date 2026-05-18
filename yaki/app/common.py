from yaki.imports import *

# 共通機能
def hide_parent(event=None):
    root.iconify()  # 親ウィンドウを非表示にする

def show_parent(event=None):
    root.deiconify()  # 親ウィンドウを再表示する



# OpenCV保存
def cv2_write(img,path):
    ext=os.path.splitext(path)[1]
    _,buf = cv2.imencode(ext, img)
    buf.tofile(path)

# OpenCV読込
def cv2_save(path):
    img = cv2.imdecode(
    np.fromfile(path, dtype=np.uint8),cv2.IMREAD_UNCHANGED)
    return img

# Pillow → OpenCV
def pil2cv(image):
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image

# OpenCV → Pillow
def cv2pil(image):
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image


def repaired_position():
    root.update_idletasks()
    ws=root.winfo_screenwidth()
    hs=root.winfo_screenheight()
    ws1=root.winfo_width()
    hs1=root.winfo_height()
    x=(ws/2)-(ws1/2)
    y=(hs/2)-(hs1/2)
    root.geometry('+%d+%d'%(x,y))

def main_frame_delete():
    root.unbind("<MouseWheel>")
    frame1.destroy()

def advanced_setting():
    def adv_setting_update():
        adv_setting["width_num"]=int(entry1.get())
        adv_setting["front_screen"]=var2.get()
        adv_setting["multi_window"]=var3.get()
        adv_setting["auto_update_chack"]=var4.get()
        adv_setting["show_center"]=var5.get()
        adv_setting["intermediate_screen"]=var6.get()
        adv_setting["hide_mainwindow"]=var7.get()
        adv_setting["launcher_width"]=int(entry8.get())
        adv_setting["launcher_height"]=int(entry9.get())

        with open(os.getcwd()+"/config/adv_setting.json", "w") as file:
            json.dump(adv_setting,file)
        messagebox.showinfo(title="保存", message="保存しました。\n再起動されます")
        restart()

    root1=Free_window()
    with open(os.getcwd()+"/config/adv_setting.json", "r") as file:
        adv_setting =json.load(file)
    if "width_num" not in adv_setting:
        adv_setting["width_num"]=4
    if "front_screen" not in adv_setting:
        adv_setting["front_screen"]=1
    if "multi_window" not in adv_setting:
        adv_setting["multi_window"]=0
    if "auto_update_chack" not in adv_setting:
        adv_setting["auto_update_chack"]=0
    if "show_center" not in adv_setting:
        adv_setting["show_center"]=0
    if "intermediate_screen" not in adv_setting:
        adv_setting["intermediate_screen"]=1
    if "hide_mainwindow" not in adv_setting:
        adv_setting["hide_mainwindow"]=0
    if "launcher_width" not in adv_setting:
        adv_setting["launcher_width"]=2
    if "launcher_height" not in adv_setting:
        adv_setting["launcher_height"]=5


    root1.title("高度な設定")
    root1.attributes("-topmost", True)

    label1=Label(root1,text="横幅数：")
    entry1=Spinbox(root1,width=10,from_=1,to=10,increment=1)
    entry1.delete(0,"end")
    entry1.insert(END,adv_setting["width_num"])
    label1.grid(row=0,column=0)
    entry1.grid(row=0,column=1)

    var2=IntVar()
    var2.set(adv_setting["front_screen"])
    label2=Label(root1,text="常時最前面に固定：")
    check2=Checkbutton(root1,variable=var2,onvalue=1,offvalue=0)
    label2.grid(row=1,column=0)
    check2.grid(row=1,column=1)

    var3=IntVar()
    var3.set(adv_setting["multi_window"])
    label3=Label(root1,text="複数起動を許可するか：")
    check3=Checkbutton(root1,variable=var3,onvalue=1,offvalue=0)
    label3.grid(row=2,column=0)
    check3.grid(row=2,column=1)

    var4=IntVar()
    var4.set(adv_setting["auto_update_chack"])
    label4=Label(root1,text="起動時に自動的に更新チェックをするか：")
    check4=Checkbutton(root1,variable=var4,onvalue=1,offvalue=0)
    label4.grid(row=3,column=0)
    check4.grid(row=3,column=1)

    var5=IntVar()
    var5.set(adv_setting["show_center"])
    label5=Label(root1,text="表示時に中央に表示するか：")
    check5=Checkbutton(root1,variable=var5,onvalue=1,offvalue=0)
    label5.grid(row=4,column=0)
    check5.grid(row=4,column=1)

    var6=IntVar()
    var6.set(adv_setting["intermediate_screen"])
    label6=Label(root1,text="一部機能で中間画面を表示するか：")
    check6=Checkbutton(root1,variable=var6,onvalue=0,offvalue=1)
    label6.grid(row=5,column=0)
    check6.grid(row=5,column=1)

    var7=IntVar()
    var7.set(adv_setting["hide_mainwindow"])
    label7=Label(root1,text="サブ画面アクティブ時にメイン画面を隠す：")
    check7=Checkbutton(root1,variable=var7,onvalue=1,offvalue=0)
    label7.grid(row=6,column=0)
    check7.grid(row=6,column=1)

    label8=Label(root1,text="ランチャーの行：")
    entry8=Spinbox(root1,width=10,from_=1,to=10,increment=1)
    entry8.delete(0,"end")
    entry8.insert(END,adv_setting["launcher_width"])
    label8.grid(row=7,column=0)
    entry8.grid(row=7,column=1)

    label9=Label(root1,text="ランチャーの列：")
    entry9=Spinbox(root1,width=10,from_=1,to=10,increment=1)
    entry9.delete(0,"end")
    entry9.insert(END,adv_setting["launcher_height"])
    label9.grid(row=8,column=0)
    entry9.grid(row=8,column=1)


    button=ttk.Button(root1,text="保存",command=adv_setting_update)
    button.grid(row=9,column=0,columnspan=2)



def rgbToHex(rgb):
    return "#%02x%02x%02x" % rgb

def home_page():
    root1=Free_window()
    root1.title("ホームページ一覧")
    root1.attributes("-topmost", True)
    ws=root1.winfo_screenwidth()
    hs=root1.winfo_screenheight()
    x=(ws/2)-250
    y=(hs/2)-300
    root1.geometry('+%d+%d'%(x,y))
    button1=ttk.Button(root1,text="配布ページ(最新VerDL・更新情報)",width=40,command=lambda:webbrowser.open("https://github.com/yukisakura001/Yukis_Army_knife/releases"))
    button2=ttk.Button(root1,text="Github(ソースコード・歴代VerDL)",width=40,command=lambda:webbrowser.open("https://github.com/yukisakura001/Yukis_Army_knife"))
    button3=ttk.Button(root1,text="Twitter(更新情報)",width=40,command=lambda:webbrowser.open("https://twitter.com/yukisakura001"))
    button4=ttk.Button(root1,text="Youtube",width=40,command=lambda:webbrowser.open("https://www.youtube.com/@yukisakura_pc"))
    button5=ttk.Button(root1,text="ブログ",width=40,command=lambda:webbrowser.open("https://yukisakura001.github.io/"))

    button1.grid(row=0,column=1)
    button2.grid(row=1,column=1)
    button3.grid(row=2,column=1)
    button4.grid(row=3,column=1)
    button5.grid(row=4,column=1)


def restart():
    subprocess.Popen(["Yukis_Army_knife.exe"])
    stop_tkinter()

def del_func_set():

    def click_close():

        messagebox.showinfo(title="終了", message="再起動したあとに\n非表示になります。")
        root1.destroy()
        restart()

    def list_delete():
        nonlocal task_setting
        try:
            select_num = listbox.curselection()
            func_delete_name=listbox.get(select_num[0])
            func_delete_num=button_function_list.index(func_delete_name)+1
        except:
            return
        res=messagebox.askquestion(title="削除確認", message="この機能をメイン画面に\n表示しますか？")
        if res != "yes":
            return
        task_setting=task_setting.replace(str(func_delete_num)+"\n","")
        with open(os.getcwd()+"/config/del_func.txt", "w") as file:
            file.write(task_setting)
        var=select_num_get()
        listbox.config(listvariable=var)
        listbox.update()

    def swap_lines(text, line1, line2):
        lines = text.split('\n')

        try:
            lines[line1], lines[line2] = lines[line2], lines[line1]
        except IndexError:
            messagebox.showinfo(title="エラー", message="選択した行が見つかりませんでした。")

        new_text = '\n'.join(lines)

        return new_text


    def select_num_get():
        select_num=[]
        for i in task_setting.split("\n")[:-1]:
            select_num.append(button_function_list[int(i)-1])
        return StringVar(value=select_num)

    def set_task_function(func_name):
        nonlocal task_setting
        try:
            func_num=button_function_list.index(func_name)+1
            task_setting=task_setting+str(func_num)+"\n"
            with open(os.getcwd()+"/config/del_func.txt", "w") as file:
                file.write(task_setting)
            var=select_num_get()
            listbox.config(listvariable=var)
            listbox.update()
        except:
            messagebox.showinfo(title="エラー", message="機能が見つかりませんでした。/nもう一度入力を確かめてください。")
            return

    def showMenu(event):
        try:
            x, y = event.x, event.y
            index = listbox.nearest(y)
            if index != -1:
                listbox.selection_clear(0, END)  # 一旦すべての選択を解除
                listbox.selection_set(index)  # 指定されたアイテムを選択
            pmenu.post(event.x_root, event.y_root)

        except:
            return

    def move_up():
        nonlocal task_setting
        # 指定した行とその上の行を入れ替える
        try:
            select_num = listbox.curselection()
        except:
            return
        if select_num[0]==0:
            return
        task_setting=swap_lines(task_setting,select_num[0],select_num[0]-1)
        with open(os.getcwd()+"/config/del_func.txt", "w") as file:
            file.write(task_setting)
        var=select_num_get()
        listbox.config(listvariable=var)
        listbox.update()

    def move_down():
        nonlocal task_setting
        # 指定した行とその下の行を入れ替える
        try:
            select_num = listbox.curselection()
        except:
            return
        if select_num[0]==len(task_setting.split("\n"))-2:
            return
        task_setting=swap_lines(task_setting,select_num[0],select_num[0]+1)
        with open(os.getcwd()+"/config/del_func.txt", "w") as file:
            file.write(task_setting)
        var=select_num_get()
        listbox.config(listvariable=var)
        listbox.update()

    if not os.path.exists(os.getcwd()+"/config/del_func.txt"):
        with open(os.getcwd()+"/config/del_func.txt", "w") as file:
            file.write("")
    with open(os.getcwd()+"/config/del_func.txt", "r") as file:
        task_setting = file.read()
    root1=Free_window()
    root1.title("非表示を設定")
    root1.attributes("-topmost", True)

    var=select_num_get()

    label1=Label(root1,text="非表示にする機能を登録してください。")
    searchbox=Searchbox(root1,width=30,values=button_function_list)
    button1=ttk.Button(root1,text="登録",command=lambda:set_task_function(searchbox.get()))
    listbox=Listbox(root1,width=30,height=10,listvariable=var)

    listbox.bind("<Button-3>", showMenu)
    root1.protocol("WM_DELETE_WINDOW", click_close)
    pmenu = Menu(root1, tearoff=0)
    pmenu.add_command(label="削除", command=list_delete)
    pmenu.add_command(label="上に移動",command=move_up)
    pmenu.add_command(label="下に移動",command=move_down)

    label1.pack()
    searchbox.pack()
    button1.pack()
    listbox.pack(fill="both",expand=True)

def check_window_existence(window_name):
    for window in root.winfo_children():
        if isinstance(window, Toplevel) and window.wm_title() == window_name:
            return True
    return False


def button_task_icon():

    def click_close():

        messagebox.showinfo(title="終了", message="再起動したあとに\nタスクトレイに表示されます。")
        root1.destroy()
        restart()

    def list_delete():
        nonlocal task_setting
        try:
            select_num = listbox.curselection()
            func_delete_name=listbox.get(select_num[0])
            func_delete_num=button_function_list.index(func_delete_name)+1
        except:
            return
        res=messagebox.askquestion(title="削除確認", message="この機能をタスクトレイから\n削除しますか？")
        if res != "yes":
            return
        task_setting=task_setting.replace(str(func_delete_num)+"\n","")
        with open(os.getcwd()+"/config/task_button.txt", "w") as file:
            file.write(task_setting)
        var=select_num_get()
        listbox.config(listvariable=var)
        listbox.update()

    def swap_lines(text, line1, line2):
        lines = text.split('\n')

        try:
            lines[line1], lines[line2] = lines[line2], lines[line1]
        except IndexError:
            messagebox.showinfo(title="エラー", message="選択した行が見つかりませんでした。")

        new_text = '\n'.join(lines)

        return new_text


    def select_num_get():
        select_num=[]
        for i in task_setting.split("\n")[:-1]:
            select_num.append(button_function_list[int(i)-1])
        return StringVar(value=select_num)

    def set_task_function(func_name):
        nonlocal task_setting
        try:
            func_num=button_function_list.index(func_name)+1
            task_setting=task_setting+str(func_num)+"\n"
            with open(os.getcwd()+"/config/task_button.txt", "w") as file:
                file.write(task_setting)
            var=select_num_get()
            listbox.config(listvariable=var)
            listbox.update()
        except:
            messagebox.showinfo(title="エラー", message="機能が見つかりませんでした。/nもう一度入力を確かめてください。")
            return

    def showMenu(event):
        try:
            x, y = event.x, event.y
            index = listbox.nearest(y)
            if index != -1:
                listbox.selection_clear(0, END)  # 一旦すべての選択を解除
                listbox.selection_set(index)  # 指定されたアイテムを選択
            pmenu.post(event.x_root, event.y_root)

        except:
            return

    def move_up():
        nonlocal task_setting
        # 指定した行とその上の行を入れ替える
        try:
            select_num = listbox.curselection()
        except:
            return
        if select_num[0]==0:
            return
        task_setting=swap_lines(task_setting,select_num[0],select_num[0]-1)
        with open(os.getcwd()+"/config/task_button.txt", "w") as file:
            file.write(task_setting)
        var=select_num_get()
        listbox.config(listvariable=var)
        listbox.update()

    def move_down():
        nonlocal task_setting
        # 指定した行とその下の行を入れ替える
        try:
            select_num = listbox.curselection()
        except:
            return
        if select_num[0]==len(task_setting.split("\n"))-2:
            return
        task_setting=swap_lines(task_setting,select_num[0],select_num[0]+1)
        with open(os.getcwd()+"/config/task_button.txt", "w") as file:
            file.write(task_setting)
        var=select_num_get()
        listbox.config(listvariable=var)
        listbox.update()

    if not os.path.exists(os.getcwd()+"/config/task_button.txt"):
        with open(os.getcwd()+"/config/task_button.txt", "w") as file:
            file.write("")
    with open(os.getcwd()+"/config/task_button.txt", "r") as file:
        task_setting = file.read()
    root1=Free_window()
    root1.title("トレイを設定")
    root1.attributes("-topmost", True)

    var=select_num_get()

    label1=Label(root1,text="タスクトレイに表示する機能を登録してください。")
    searchbox=Searchbox(root1,width=30,values=button_function_list)
    button1=ttk.Button(root1,text="登録",command=lambda:set_task_function(searchbox.get()))
    listbox=Listbox(root1,width=30,height=10,listvariable=var)

    listbox.bind("<Button-3>", showMenu)
    root1.protocol("WM_DELETE_WINDOW", click_close)
    pmenu = Menu(root1, tearoff=0)
    pmenu.add_command(label="削除", command=list_delete)
    pmenu.add_command(label="上に移動",command=move_up)
    pmenu.add_command(label="下に移動",command=move_down)

    label1.pack()
    searchbox.pack()
    button1.pack()
    listbox.pack(fill="both",expand=True)


def launcher_screen():
    # launch_dict={"1":[0,"名前","データ"],}
    if not os.path.exists(os.getcwd()+"/config/launch.json"):
        with open(os.getcwd()+"/config/launch.json", "w",encoding="utf-8") as file:
            file.write("{}")
    with open(os.getcwd()+"/config/launch.json", "r",encoding="utf-8") as f:
        set_launch = json.load(f)
    width_l=launcher_width
    height_l=launcher_height
    root_l=Toplevel()
    root_l.title("YAkランチャー")
    root_l.attributes("-topmost", True)
    frame_main_l=ttk.Frame(root_l)
    frame_main_l.pack(expand=True,fill="both")

    class SHFILEINFO(ctypes.Structure):
        _fields_ = [("hIcon", ctypes.wintypes.HICON),
                    ("iIcon", ctypes.c_int),
                    ("dwAttributes", ctypes.c_ulong),
                    ("szDisplayName", ctypes.wintypes.WCHAR * 260),
                    ("szTypeName", ctypes.wintypes.WCHAR * 80)]

    SHGFI_ICON = 0x000000100
    SHGFI_USEFILEATTRIBUTES = 0x000000010
    FILE_ATTRIBUTE_NORMAL = 0x00000080

    shell32 = ctypes.WinDLL('shell32')
    shell32.SHGetFileInfoW.argtypes = [ctypes.wintypes.LPCWSTR, ctypes.wintypes.DWORD, ctypes.POINTER(SHFILEINFO), ctypes.wintypes.UINT, ctypes.wintypes.UINT]
    shell32.SHGetFileInfoW.restype = ctypes.wintypes.HANDLE

    def get_folder_icon(folder_path):
        shinfo = SHFILEINFO()
        retval = shell32.SHGetFileInfoW(
            folder_path, 0, ctypes.byref(shinfo),
            ctypes.sizeof(shinfo), SHGFI_ICON
        )
        if retval:
            return shinfo.hIcon
        else:
            return None

    def get_icon(ext):
        shinfo = SHFILEINFO()
        retval = shell32.SHGetFileInfoW(
            ext, FILE_ATTRIBUTE_NORMAL, ctypes.byref(shinfo),
            ctypes.sizeof(shinfo), SHGFI_ICON | SHGFI_USEFILEATTRIBUTES
        )
        if retval:
            return shinfo.hIcon
        else:
            return None

    def icon_to_image(icon, size=(32, 32)):
        hdc = ctypes.windll.user32.GetDC(0)
        hbmp = ctypes.windll.gdi32.CreateCompatibleBitmap(hdc, size[0], size[1])

        hmemdc = ctypes.windll.gdi32.CreateCompatibleDC(hdc)
        ctypes.windll.gdi32.SelectObject(hmemdc, hbmp)
        ctypes.windll.user32.DrawIconEx(hmemdc, 0, 0, icon, size[0], size[1], 0, None, 0x0003)
        ctypes.windll.user32.DestroyIcon(icon)
        ctypes.windll.gdi32.DeleteDC(hmemdc)

        bitmap_bits = ctypes.create_string_buffer(size[0] * size[1] * 4)

        # GetBitmapBitsを呼び出してバッファにビットを格納
        ctypes.windll.gdi32.GetBitmapBits(hbmp, ctypes.sizeof(bitmap_bits), bitmap_bits)

        # PILで画像を作成
        image = Image.frombuffer(
            'RGBA',
            size,
            bitmap_bits,
            'raw',
            'BGRA',
            0,
            1
        )
        ctypes.windll.gdi32.DeleteObject(hbmp)
        ctypes.windll.user32.ReleaseDC(0, hdc)
        return image

    def exe_drop(path):
        #try:
            y=path
            if os.path.isdir(y):
                icon=get_folder_icon("")
            else:
                icon = get_icon(y) #""でドライブアイコン
            if icon:
                img = icon_to_image(icon)
                return img

    def get_url_title(url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string
        except:
            title=None
        return title


    def save_launch():
        with open(os.getcwd()+"/config/launch.json", "w",encoding="utf-8") as f:
            # jsonファイルに書き込む
            json.dump(set_launch,f,ensure_ascii=False, indent=4)

    def set_screen_launch():
        for i in range(width_l):
            for j in range(height_l):
                if str(i*height_l+j) not in set_launch:
                    locals()["button"+str(i*height_l+j)]=Button(frame_main_l,text="未登録",command=partial(set_func,i*height_l+j),width=150,height=70,bg="lightgray",image=icon_image_transparent,compound=TOP)
                    locals()["button"+str(i*height_l+j)].image=icon_image_transparent
                else:
                    if set_launch[str(i*height_l+j)][0]==0:
                        icon_image_set=icon_image1
                    elif set_launch[str(i*height_l+j)][0]==1:
                        icon_image_set=icon_image_net
                    elif set_launch[str(i*height_l+j)][0]==2:
                        icon_exe_img=exe_drop(set_launch[str(i*height_l+j)][2]).resize((48,48))
                        icon_image_set=ImageTk.PhotoImage(icon_exe_img)
                    elif set_launch[str(i*height_l+j)][0]==3:
                        icon_exe_img=exe_drop(set_launch[str(i*height_l+j)][2]).resize((48,48))
                        icon_image_set=ImageTk.PhotoImage(icon_exe_img)

                    locals()["button"+str(i*height_l+j)]=Button(frame_main_l,text=set_launch[str(i*height_l+j)][1][:12],command=partial(click_l,i*height_l+j),width=150,height=70,bg="lightgray",image=icon_image_set,compound=TOP,font=("Courier", 7))
                    locals()["button"+str(i*height_l+j)].image=icon_image_set
                    ToolTip1=ToolTip(locals()["button"+str(i*height_l+j)],set_launch[str(i*height_l+j)][1])
                    RightClickMenu(locals()["button"+str(i*height_l+j)],[("削除",partial(delete_func,i*height_l+j)),("名前編集",partial(custom_func,i*height_l+j))])
                locals()["button"+str(i*height_l+j)].grid(row=i,column=j)
                locals()["button"+str(i*height_l+j)].drop_target_register(DND_FILES)
                locals()["button"+str(i*height_l+j)].dnd_bind('<<Drop>>',partial(set_func1,i*height_l+j))

    def delete_func(num):
        set_launch.pop(str(num))
        save_launch()
        load_launch(num)

    def custom_func(num):
        def change_name():
            set_launch[str(num)][1]=entry1.get()
            save_launch()
            load_launch(num)
            messagebox.showinfo(title="変更", message="変更しました。")
            root_l1.destroy()

        root_l1=Toplevel()
        root_l1.title("名前の変更")
        root_l1.attributes("-topmost", True)
        entry1=ttk.Entry(root_l1,width=30)
        entry1.insert(END,set_launch[str(num)][1])
        button1=ttk.Button(root_l1,text="変更",command=change_name)
        entry1.pack()
        button1.pack()

    def load_launch(num=1):
        nonlocal set_launch
        with open(os.getcwd()+"/config/launch.json", "r",encoding="utf-8") as f:
            set_launch = json.load(f)
        children=frame_main_l.winfo_children()
        for child in children:
            child.destroy()
        set_screen_launch()


    def set_func1(num,drop):
        nonlocal set_launch
        path=drop.data.replace("{","").replace("}","").replace("\\","/")
        name=os.path.basename(path)
        if os.path.isdir(path):
            set_launch[str(num)]=[3,name,path]
        else:
            set_launch[str(num)]=[2,name,path]
        save_launch()
        load_launch(num)


    def set_func(func_num):
        nonlocal set_launch

        def change_func():
            if var.get()==0:
                entry1.grid_forget()
                combo.grid(row=0,column=0)
            else:
                combo.grid_forget()
                entry1.grid(row=0,column=0)

        def set_yak():
            nonlocal set_launch
            if var.get()==0:
                set_launch[str(func_num)]=[0,combo.get(),""]
                save_launch()
                load_launch(func_num)
            elif var.get()==1:
                title=get_url_title(entry1.get())
                if title==None:
                    title = urlparse(entry1.get())
                set_launch[str(func_num)]=[1,f"{title}",entry1.get()]
                save_launch()
                load_launch(func_num)
            elif var.get()==2:
                name=os.path.basename(entry1.get())
                if os.path.isdir(entry1.get()):
                    set_launch[str(func_num)]=[3,name,entry1.get()]
                else:
                    set_launch[str(func_num)]=[2,name,entry1.get()]
                save_launch()
                load_launch(func_num)
            messagebox.showinfo(title="登録", message="登録しました。")
            root1.destroy()

        root1=Toplevel()
        root1.title("機能の設定")
        root1.attributes("-topmost", True)
        var=IntVar()
        var.set(0)
        frame_main_l1=ttk.Frame(root1)
        frame_main_l1.pack(expand=True,fill="both")
        radio1=ttk.Radiobutton(frame_main_l1,text="Yukis Army knifeの機能を登録",variable=var,value=0,command=change_func)
        radio2=ttk.Radiobutton(frame_main_l1,text="サイトを登録",variable=var,value=1,command=change_func)
        radio3=ttk.Radiobutton(frame_main_l1,text="ファイル・フォルダを登録",variable=var,value=2,command=change_func)
        frame_l=ttk.Frame(root1)
        combo=Searchbox(frame_l,width=30,values=button_function_list)
        button1=ttk.Button(frame_l,text="登録",command=set_yak)
        entry1=ttk.Entry(frame_l,width=30)
        ws1=root1.winfo_width()
        hs1=root1.winfo_height()
        x1=(ws/2)-(ws1/2)
        y1=(hs/2)-(hs1/2)
        root1.geometry('+%d+%d'%(x1,y1))

        radio1.pack()
        radio2.pack()
        radio3.pack()
        frame_l.pack(expand=True,fill="both")
        combo.grid(row=0,column=0)
        button1.grid(row=1,column=0)


    def click_l(func_key):
        try:
            if str(func_key) not in set_launch:
                set_func()
            # 機能のリストにあるなら分岐

            elif set_launch[str(func_key)][0]==0:
                # YAkの機能
                root.deiconify()
                buttonY.invoke()
                dist_button[set_launch[str(func_key)][1]]()
            elif set_launch[str(func_key)][0]==1:
                # URL
                webbrowser.open(set_launch[str(func_key)][2])
            elif set_launch[str(func_key)][0]==2:
                # ファイル
                os.startfile(set_launch[str(func_key)][2])
            elif set_launch[str(func_key)][0]==3:
                # フォルダ
                folder_path=set_launch[str(func_key)][2].replace("/","\\")
                subprocess.run(["explorer.exe", folder_path])
            root_l.destroy()
        except:
            messagebox.showinfo(title="エラー", message="機能が見つかりませんでした。")

    img=Image.open(my_icon.get_img())
    img=img.resize((48,48))
    icon_image1=ImageTk.PhotoImage(img)
    img1 = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    icon_image_transparent=ImageTk.PhotoImage(img1)
    icon_image_net=my_icon.get_photo_web()

    load_launch()
    root.after(100, load_launch)

    #for i in range(width_l):
    #    for j in range(height_l):
    #        if str(i*height_l+j) not in set_launch:
    #            locals()["button"+str(i*height_l+j)]=Button(frame_main_l,text="未登録",command=partial(set_func,i*height_l+j),width=150,height=70,bg="lightgray",image=icon_image_transparent,compound=TOP)
    #            locals()["button"+str(i*height_l+j)].image=icon_image_transparent
    #        else:
    #            if set_launch[str(i*height_l+j)][0]==0:
    #                icon_image_set=icon_image1
    #            elif set_launch[str(i*height_l+j)][0]==1:
    #                icon_image_set=icon_image_net
    #            elif set_launch[str(i*height_l+j)][0]==2:
    #                icon_exe_img=exe_drop(set_launch[str(i*height_l+j)][2]).resize((48,48))
    #                icon_image_set=ImageTk.PhotoImage(icon_exe_img)
    #            elif set_launch[str(i*height_l+j)][0]==3:
    #                icon_exe_img=exe_drop(set_launch[str(i*height_l+j)][2]).resize((48,48))
    #                icon_image_set=ImageTk.PhotoImage(icon_exe_img)
#
    #            locals()["button"+str(i*height_l+j)]=Button(frame_main_l,text=set_launch[str(i*height_l+j)][1][:12],command=partial(click_l,i*height_l+j),width=150,height=70,bg="lightgray",image=icon_image_set,compound=TOP,font=("Courier", 7))
    #            locals()["button"+str(i*height_l+j)].image=icon_image_set
    #            ToolTip1=ToolTip(locals()["button"+str(i*height_l+j)],set_launch[str(i*height_l+j)][1])
    #            RightClickMenu(locals()["button"+str(i*height_l+j)],[("削除",partial(delete_func,i*height_l+j)),("名前編集",partial(custom_func,i*height_l+j))])
    #        locals()["button"+str(i*height_l+j)].grid(row=i,column=j)
    #        locals()["button"+str(i*height_l+j)].drop_target_register(DND_FILES)
    #        locals()["button"+str(i*height_l+j)].dnd_bind('<<Drop>>',partial(set_func1,i*height_l+j))


    root_l.update_idletasks()
    ws=root.winfo_screenwidth()
    hs=root.winfo_screenheight()
    ws2, hs2 = pyautogui.position()
    ws1=root_l.winfo_width()
    hs1=root_l.winfo_height()
    x=(ws/2)-(ws1/2)
    y=(hs/2)-(hs1/2)
    root_l.geometry('+%d+%d'%(x,y))

    #def hide_window(event):
    #    root_l.after(1000, check_mouse_position)
#
    #def check_mouse_position():
    #    if root_l.winfo_pointerxy()[0] < root_l.winfo_x() or root_l.winfo_pointerxy()[0] > root_l.winfo_x() + root_l.winfo_width() \
    #            or root_l.winfo_pointerxy()[1] < root_l.winfo_y() or root_l.winfo_pointerxy()[1] > root_l.winfo_y() + root_l.winfo_height():
    #        root_l.destroy()
    #frame_main_l.bind("<Leave>",hide_window )

def listener_window():
    global main_show_shrotcut,shift
    ctrl=0
    shift=0
    def on_press(key):
        nonlocal ctrl
        global  shift
        if main_show_shrotcut==1:
            return
        if key == keyboard.Key.space and ctrl==1 and shift==1:
            if root.state() == "normal":
                if show_center==1:
                    repaired_position()
                frame_delete()
            else:
                if show_center==1:
                    repaired_position()
                root.deiconify()
                combobox_frame.focus_set()

        if key == keyboard.Key.pause and shift==1:
            if check_window_existence("YAkランチャー"):
                pass
            else:
                launcher_screen()

        if key == keyboard.Key.ctrl_l:
            ctrl=1
        if key == keyboard.Key.shift:
            shift=1

    def on_release(key):
        nonlocal ctrl
        global shift
        if key == keyboard.Key.ctrl_l:
            ctrl=0
        if key == keyboard.Key.shift:
            shift=0

    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener_def:
        listener_def.join()

def check_new_ver():
    url = 'https://www.dropbox.com/scl/fi/5y15joc9artguntvecp7e/version.txt?rlkey=pps35nwsvdzsytn3l2hvrxyit&dl=1'
    response = requests.get(url)
    if float(version) < float(response.text.rstrip()):
        res=messagebox.askquestion(title="バージョン確認", message=f"新規バージョン{response.text.rstrip()}があります。ダウンロードしますか？")
        if res == "yes":
            #webbrowser.open("https://www.dropbox.com/scl/fo/frsya7l4zh14z30fpuk0n/h?rlkey=2jncv45l8jhoe7ezls9iqn51v&dl=0")
            # ユーザー名を取得
            user_name = getpass.getuser()
            # フォルダパスを組み立てる
            folder_path = fr'C:\Users\{user_name}\AppData\Local\Programs\Yukis Army knife'
            current_directory = os.getcwd()
            if current_directory == folder_path:
                def update_soft():
                    urllib.request.urlretrieve(url, save_path)
                    subprocess.Popen(save_path)
                    stop_tkinter()

                # ダウンロードするファイルのURLを指定
                url = "https://www.dropbox.com/scl/fi/del2oxu9w5aq4d4b2aul7/Yukis_Army_knife_Installer.exe?rlkey=zs2w4wjb9kai0m6axku5v46ui&dl=1"
                # ファイルを保存するフォルダとファイル名を指定
                make_folder("temp1")
                save_path = os.getcwd()+"/temp1/Yukis_Army_knife.exe"
                # URLからファイルをダウンロードして指定したフォルダに保存
                messagebox.showinfo("情報","ダウンロード中です。")
                t=threading.Thread(target=update_soft,daemon=True)
                t.start()

            else:
                def update_soft():
                    urllib.request.urlretrieve(url, save_path)
                    messagebox.showinfo("情報","ダウンロードが完了しました。")

                url="https://www.dropbox.com/scl/fi/zxji4x5epgddma25ew48q/Yukis_Army_knife_portable.zip?rlkey=xoqsbfn12hvjbuqv5iq3k8a4w&dl=1"
                save_path = filedialog.asksaveasfilename(initialdir = os.getcwd(),title = "保存場所を選択",filetypes = [("zipファイル","*.zip")],initialfile="Yukis_Army_knife.zip")
                t=threading.Thread(target=update_soft,daemon=True)
                t.start()
                messagebox.showinfo("情報","ダウンロード中です。")


    else:
        messagebox.showinfo("情報","最新バージョンです。")

def startup_reg():
    def create_shortcut(target_path, shortcut_path):
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target_path
        shortcut.WorkingDirectory = os.path.dirname(target_path)
        shortcut.save()

    target_file = os.getcwd()+"/Yukis_Army_knife.exe"
    shortcut_file = os.path.expandvars("%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")+"/Yukis_Army_knife.lnk"

    create_shortcut(target_file, shortcut_file)
    messagebox.showinfo("情報","スタートアップに登録しました。")

def esc_key_pressed(event):
    if event.keysym == "Escape":
        buttonY.invoke()

def check_frame(button):
    parent = button.winfo_parent()
    return parent.split(".")[-1]

def set_theme(theme):
    if theme==0:
        with open(os.getcwd()+"/config/style.txt", "w") as file:
            file.write("0")
            s.theme_use("vista")
    elif theme==1:
        with open(os.getcwd()+"/config/style.txt", "w") as file:
            file.write("modern")
            s.theme_use("adapta")
    elif theme==2:
        with open(os.getcwd()+"/config/style.txt", "w") as file:
            file.write("dark")
            s.theme_use("black")
    elif theme==3:
        with open(os.getcwd()+"/config/style.txt", "w") as file:
            file.write("digital")
        s.theme_use("aquativo")
    elif theme==5:
        with open(os.getcwd()+"/config/style.txt", "w") as file:
            file.write("natural")
        s.theme_use("clearlooks")
    elif theme==6:
        with open(os.getcwd()+"/config/style.txt", "w") as file:
            file.write("systemati")
        s.theme_use("elegance")
    elif theme==7:
        with open(os.getcwd()+"/config/style.txt", "w") as file:
            file.write("keramik")
        s.theme_use("keramik")
    elif theme==8:
        with open(os.getcwd()+"/config/style.txt", "w") as file:
            file.write("wood-like")
        s.theme_use("kroc")
    elif theme==9:
        with open(os.getcwd()+"/config/style.txt", "w") as file:
            file.write("plastik")
        s.theme_use("plastik")
    elif theme==10:
        with open(os.getcwd()+"/config/style.txt", "w") as file:
            file.write("radiance")
        s.theme_use("radiance")
    elif theme==11:
        with open(os.getcwd()+"/config/style.txt", "w") as file:
            file.write("XPblue")
        s.theme_use("winxpblue")
    elif theme==12:
        with open(os.getcwd()+"/config/style.txt", "w") as file:
            file.write("sand")
        s.theme_use("scidsand")
    elif theme==13:
        with open(os.getcwd()+"/config/style.txt", "w") as file:
            file.write("classic")
        s.theme_use("clam")
    elif theme==14:
        with open(os.getcwd()+"/config/style.txt", "w") as file:
            file.write("modern_dark")
        sv_ttk.set_theme("dark")
    elif theme==15:
        with open(os.getcwd()+"/config/style.txt", "w") as file:
            file.write("modern_light")
        sv_ttk.set_theme("light")

    s.configure("TNotebook", tabposition='n')
    if frame1.winfo_exists():
        main_frame_delete()
    else:
        frame.destroy()
    set_frame1(0)


def file_mult(x):
    #input_str = x
    #input_str=input_str+" "
    #result = re.findall(r"(.+?)\.([a-zA-Z0-9]+)\s", input_str)
    #output_list = [f"{item[0]}.{item[1]}" for item in result]
    output_list = re.split(r"\s(?=[A-Za-z]+:)", x)
    return output_list

def main_frame(page_n):
    global frame,buttonY
    frame.destroy()
    set_frame1(page_n)

def frame_delete():
    if buttonY["state"] =="normal":
        buttonY.invoke()
    combobox_frame.delete(0,END)
    root.withdraw()

def stop_tkinter():
    global buttonY
    root.withdraw()
    if os.path.exists(os.getcwd()+"/temp1"):
        shutil.rmtree(os.getcwd()+"/temp1", ignore_errors=True)
    if buttonY["state"] =="normal":
        buttonY.invoke()
    root.destroy()

def execute():
    global window_front,main_show_shrotcut

    #def on_focus_out1(event):
    #    if event.widget == root:
    #        frame_delete()
    #    else:
    #    # ルートウィンドウ以外のウィジェットによるフォーカスアウトは無視
    #        pass
#
    #if window_front.get() == 1:
    #    #root.attributes("-topmost", False)
    #    root.bind("<FocusOut>", on_focus_out1)
    #elif window_front.get() ==0:
    #    #root.attributes("-topmost", True)
    #    root.unbind("<FocusOut>")
    if window_front.get() == 1:
        main_show_shrotcut=1
    elif window_front.get() ==0:
        main_show_shrotcut=0

def make_folder(x):
    if not os.path.exists(x):
        os.makedirs(x)

def delete_folder(x):
    if os.path.exists(x):
        shutil.rmtree(x)

def taskarea():
    global icon,task_menu

    toast = winotify.Notification(
            title="Yukis Army knifeを起動しました",
            msg="タスクトレイにアイコンが表示されています",
            app_id="Yukis_Army_knife",
        )
    toast.show()

    def action_func(icon,item):
        root.deiconify()
        if buttonY["state"] =="normal":
            buttonY.invoke()
        if show_center==1:
            repaired_position()
        dist_button[str(item)]()

    if not os.path.exists(os.getcwd()+"/config/task_button.txt"):
        with open(os.getcwd()+"/config/task_button.txt", "w") as file:
            file.write("")

    img=my_icon.get_img()
    image = Image.open(img)
    func_list=[]
    with open(os.getcwd()+"/config/task_button.txt", "r") as file:
        task_setting = file.read()
    for num,i in enumerate(task_setting.split("\n")[:-1]):
        #print(button_function_list[int(i) - 1])
        item_name = button_function_list[int(i) - 1]
        func_list.append(pystray.MenuItem(item_name, action=action_func))
    func_list.append(pystray.MenuItem('ーーーーーーーーーーー',action=None,enabled=False))
    func_list.append(pystray.MenuItem(text="ウィンドウ表示", action=left_click_action, default=True))
    func_list.append(pystray.MenuItem(text="再起動", action=restart))
    func_list.append(pystray.MenuItem(text="ソフトを終了", action=stop_tkinter))


    task_menu=pystray.Menu(*func_list)

    icon = pystray.Icon(
        name="Yukis_Army_knife",
        icon=image,
        title="Yukis_Army_knife",
        menu=task_menu
    )
    icon.run()

def left_click_action(icon,item):
    global root
    if root.state() == "normal":
        frame_delete()
    else:
        root.deiconify()
        if show_center==1:
            root.geometry('+%d+%d'%(x,y))
        combobox_frame.focus_set()


def setting_folder():
    subprocess.Popen(["explorer", r"config"], shell=True)

