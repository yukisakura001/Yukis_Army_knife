# GUI
try:
   ctypes.windll.user32.SetProcessDPIAware()
   ctypes.windll.shcore.SetProcessDpiAwareness(True)
except AttributeError:
    pass

if os.path.exists(os.getcwd()+"/temp1"):
    shutil.rmtree(os.getcwd()+"/temp1", ignore_errors=True)
make_folder(os.getcwd()+"/config")
if not os.path.exists(os.getcwd()+"/config/style.txt"):
    with open(os.getcwd()+"/config/style.txt", "w") as file:
        file.write("0")
with open(os.getcwd()+"/config/style.txt", "r") as file:
    style_setting = file.read()

if not os.path.exists(os.getcwd()+"/config/adv_setting.json"):
    data={"width_num":4,
          "front_screen":1,
          "multi_window":0,
          "auto_update_chack":0,
          "show_center":0,
          "intermediate_screen":1,
          "hide_mainwindow":0,
          "launcher_width":2,
          "launcher_height":5,}
    with open(os.getcwd()+"/config/adv_setting.json", "w") as file:
        json.dump(data, file)
with open(os.getcwd()+"/config/adv_setting.json", "r") as file:
    adv_setting =json.load(file)
if "width_num" in adv_setting:
    main_frame_width=adv_setting["width_num"]
else:
    main_frame_width=4
if "front_screen" in adv_setting:
    front_screen=adv_setting["front_screen"]
else:
    front_screen=1
if "multi_window" in adv_setting:
    multi_window=adv_setting["multi_window"]
else:
    multi_window=0
if "auto_update_chack" in adv_setting:
    auto_update_chack=adv_setting["auto_update_chack"]
else:
    auto_update_chack=0
if "show_center" in adv_setting:
    show_center=adv_setting["show_center"]
else:
    show_center=0
if "intermediate_screen" in adv_setting:
    intermediate_screen=adv_setting["intermediate_screen"]
else:
    intermediate_screen=1
if "hide_mainwindow" in adv_setting:
    hide_mainwindow=adv_setting["hide_mainwindow"]
else:
    hide_mainwindow=0
if "launcher_width" in adv_setting:
    launcher_width=adv_setting["launcher_width"]
else:
    launcher_width=2
if "launcher_height" in adv_setting:
    launcher_height=adv_setting["launcher_height"]
else:
    launcher_height=5

if multi_window==0:
    WindowName = "Yuki's army knife"
    WindowHandle = win32gui.FindWindow(None, WindowName)
    if 0 != WindowHandle:
        root=Tk()
        root.withdraw()
        messagebox.showerror("エラー","すでに起動しています")
        sys.exit()

main_checkbox_name="表示ショトカ無効"
main_show_shrotcut=0

if not os.path.exists(os.getcwd()+"/config/del_func.txt"):
    with open(os.getcwd()+"/config/del_func.txt", "w") as file:
        file.write("")
with open(os.getcwd()+"/config/del_func.txt", "r") as file:
    del_func = file.read().split("\n")[:-1]


root = Tk()
s = ttk.Style()
if style_setting.strip()=="modern":
    s.theme_use("adapta")
elif style_setting.strip()=="dark":
    s.theme_use("black")
elif style_setting.strip()=="digital":
    s.theme_use("aquativo")
elif style_setting.strip()=="natural":
    s.theme_use("clearlooks")
elif style_setting.strip()=="systematic":
    s.theme_use("elegance")
elif style_setting.strip()=="keramik":
    s.theme_use("keramik")
elif style_setting.strip()=="wood-like":
    s.theme_use("kroc")
elif style_setting.strip()=="plastik":
    s.theme_use("plastik")
elif style_setting.strip()=="radiance":
    s.theme_use("radiance")
elif style_setting.strip()=="XPblue":
    s.theme_use("winxpblue")
elif style_setting.strip()=="sand":
    s.theme_use("scidsand")
elif style_setting.strip()=="classic":
    s.theme_use("clam")
elif style_setting.strip()=="modern_dark":
    sv_ttk.set_theme("dark")
elif style_setting.strip()=="modern_light":
    sv_ttk.set_theme("light")
s.configure("TNotebook", tabposition='n')

root.resizable(False, False)
root.title("Yuki's army knife")
photo = my_icon.get_photo_image4icon()
root.iconphoto(True, photo)
root.bind("<Escape>", esc_key_pressed)
ws=root.winfo_screenwidth()
hs=root.winfo_screenheight()
x=(ws/2)-250
y=(hs/2)-300
root.geometry('+%d+%d'%(x,y))
window_front=IntVar()


def _bind_runtime_to_common_tools():
    from yaki.app import common as _common
    from yaki.features import tools as _tools
    import yaki.widgets as _widgets
    _bind = {
        "root": root,
        "window_front": window_front,
        "main_show_shrotcut": main_show_shrotcut,
        "main_checkbox_name": main_checkbox_name,
        "hide_mainwindow": hide_mainwindow,
        "front_screen": front_screen,
        "multi_window": multi_window,
        "auto_update_chack": auto_update_chack,
        "main_frame_width": main_frame_width,
        "del_func": del_func,
        "style_setting": style_setting,
        "adv_setting": adv_setting,
    }
    for _mod in (_common, _tools, _widgets):
        _mod.__dict__.update(_bind)

_bind_runtime_to_common_tools()
set_frame1(0)
from yaki.runtime import sync_shell_to_all

sync_shell_to_all()
root.withdraw()
# ウィンドウ最小化
#root.bind("<Unmap>", on_minimize)
# 起動
task_area=threading.Thread(target=taskarea,daemon=True)
task_area.start()
listener_def=None
listener_window_t=threading.Thread(target=listener_window,daemon=True)
listener_window_t.start()

if front_screen==1:
    root.attributes("-topmost", True)

if auto_update_chack==1:
    root.after(1,check_new_ver)

# app_global_setting
mause_highlight_hwnd=0

root.mainloop()
