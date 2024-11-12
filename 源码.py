"""
作者：CJS
时间：20241017
Q裙：914580966
Only For Test
DESIGNED BY CJS
"""


import tkinter as tk
from tkinter import messagebox
import ctypes
from ctypes import wintypes
import sys
import pymem
import math


def get_window_info(window_title):
    hwnd = ctypes.windll.user32.FindWindowW(None, window_title)
    if hwnd == 0:
        messagebox.showerror("错误", "句柄未找到请重新打开程序")
        return 0, 0, 0, 0, None
    rect = wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
    width = rect.right - rect.left
    height = rect.bottom - rect.top
    x = rect.left
    y = rect.top
    return width, height, x, y, hwnd


def toggle_execution1():
    if execution_enabled1.get():
        try:
            Game = pymem.Pymem('csgo.exe')
        except:
            messagebox.showerror("错误", "你TM都没有打开程序，开毛线？？")
            sys.exit(1)

        def Get_moduladdr(dll):
            modules = list(Game.list_modules())
            for module in modules:
                if module.name == dll:
                    return module.lpBaseOfDll
            return None

        Char_Modlue1 = Get_moduladdr("server.dll")
        Char_Modlue2 = Get_moduladdr("client.dll")
        if Char_Modlue1 is None or Char_Modlue2 is None:
            messagebox.showerror("错误", "基址获取失败，请重新打开游戏")
            sys.exit(1)

        def calculate_screen_coordinates(enemy_x, enemy_y, enemy_z, matrix, window_width, window_height):
            cs_x = (matrix[0] * enemy_x + matrix[4] * enemy_y + matrix[8] * enemy_z + matrix[12])
            cs_y = (matrix[1] * enemy_x + matrix[5] * enemy_y + matrix[9] * enemy_z + matrix[13])
            cs_w = (matrix[3] * enemy_x + matrix[7] * enemy_y + matrix[11] * enemy_z + matrix[15])

            if cs_w > 0.001:
                ndc_x = cs_x / cs_w
                ndc_y = cs_y / cs_w

                screen_x = int((ndc_x) * (window_width / 2) + (window_width / 2))
                screen_y = int(-(ndc_y) * (window_height / 2) + (window_height / 2))

                return screen_x, screen_y
            else:
                return None, None

        def Det_hp_camp_xyz(addr):
            hp = Game.read_int(addr + 0x230)
            camp = Game.read_int(addr + 0x318)
            x = Game.read_float(addr + 0x2E4 - 0x8)
            y = Game.read_float(addr + 0x2E4 - 0x4)
            z = Game.read_float(addr + 0x2E4) + 69
            return hp, camp, x, y, z

        def draw_text(canvas, text, x, y):
            canvas.create_text(x, y, text=text, fill='red', font=("Arial", 10))

        def update_window_position():
            width, height, x, y, hwnd = get_window_info('Counter-Strike: Global Offensive')

            if hwnd:
                root.geometry(f'{width}x{height}+{x}+{y}')
                canvas.config(width=width, height=height)  # 更新canvas大小

                # 更新矩阵
                matrix_base_address = Game.read_int(Char_Modlue2 + 0x212B60)
                matrix_addr = matrix_base_address + 0x190
                matrix = [Game.read_float(matrix_addr + (i * 16)) for i in range(4)]
                matrix_y = [Game.read_float(matrix_addr + (i * 16) + 4) for i in range(4)]
                matrix_z = [Game.read_float(matrix_addr + (i * 16) + 8) for i in range(4)]
                matrix_w = [Game.read_float(matrix_addr + (i * 16) + 12) for i in range(4)]

                global combined_matrix
                combined_matrix = matrix + matrix_y + matrix_z + matrix_w  # 更新全局矩阵

            root.after(10, update_window_position)  # 每10毫秒调用一次

        def update_and_draw_dots():
            canvas.delete("all")  # 清除画布
            width, height, _, _, _ = get_window_info('Counter-Strike: Global Offensive')

            for i in range(9):  # 假设最多读取9个敌人
                enemy_addr = Game.read_int(Char_Modlue1 + 0xA7E72C + 0x18 * i)
                if enemy_addr:  # 确保地址有效
                    hp, camp, enemy_x, enemy_y, enemy_z = Det_hp_camp_xyz(enemy_addr)
                    screen_x, screen_y = calculate_screen_coordinates(enemy_x, enemy_y, enemy_z, combined_matrix, width, height)
                    screen_x1, screen_y1 = calculate_screen_coordinates(enemy_x, enemy_y - 30, enemy_z , combined_matrix,
                                                                       width, height)
                    screen_x2, screen_y2 = calculate_screen_coordinates(enemy_x, enemy_y + 30, enemy_z - 69 , combined_matrix, width,
                                                                        height)

                    My_addr = Game.read_int(Char_Modlue1 + 0xA7E714)
                    Camp = Det_hp_camp_xyz(My_addr)[1]
                    My_x = Det_hp_camp_xyz(My_addr)[2]
                    My_y = Det_hp_camp_xyz(My_addr)[3]
                    if camp != Camp:
                        if hp > 0:
                            if screen_x is not None and screen_y is not None:
                                if screen_x1 is not None and screen_y1 is not None:
                                        if screen_x2 is not None and screen_y2 is not None:
                                            num = ( enemy_x - My_x ) ** 2  + ( enemy_y - My_y ) ** 2
                                            dis = int(math.sqrt(num))
                                            draw_text(canvas, f'血量{hp}  距离{dis}', screen_x - 40, screen_y )  # 绘制血量文本

            root.after(10, update_and_draw_dots)  # 每100毫秒更新一次

        root = tk.Tk()
        root.attributes('-transparentcolor', 'white')  # 设置窗口背景为透明
        root.resizable(0, 0)
        root.attributes('-topmost', True)
        root.overrideredirect(True)

        canvas = tk.Canvas(root, width=200, height=200, bg='white', highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)  # 让Canvas填充整个Tkinter窗口

        # 启动更新和绘制
        update_window_position()
        update_and_draw_dots()

        root.mainloop()
    else:
        messagebox.showinfo(title='注意',message='想关闭只能通过下方的一键关闭')

def toggle_execution2():
    if execution_enabled2.get():
        try:
            Game = pymem.Pymem('csgo.exe')
        except:
            # window = tk.Tk()
            # window.withdraw()
            messagebox.showerror("错误", "你TM都没有打开程序，开毛线？？")
            sys.exit(1)

        def Get_moduladdr(dll):
            modules = list(Game.list_modules())
            for module in modules:
                if module.name == dll:
                    return module.lpBaseOfDll
            return None

        Char_Modlue1 = Get_moduladdr("server.dll")
        Char_Modlue2 = Get_moduladdr("client.dll")
        if Char_Modlue1 is None or Char_Modlue2 is None:
            # window = tk.Tk()
            # window.withdraw()
            messagebox.showerror("错误", "基址获取失败，请重新打开游戏")
            sys.exit(1)

        def calculate_screen_coordinates(enemy_x, enemy_y, enemy_z, matrix, window_width, window_height):
            cs_x = (matrix[0] * enemy_x + matrix[4] * enemy_y + matrix[8] * enemy_z + matrix[12])
            cs_y = (matrix[1] * enemy_x + matrix[5] * enemy_y + matrix[9] * enemy_z + matrix[13])
            cs_w = (matrix[3] * enemy_x + matrix[7] * enemy_y + matrix[11] * enemy_z + matrix[15])

            if cs_w > 0.001:
                ndc_x = cs_x / cs_w
                ndc_y = cs_y / cs_w

                screen_x = int((ndc_x) * (window_width / 2) + (window_width / 2))
                screen_y = int(-(ndc_y) * (window_height / 2) + (window_height / 2))

                return screen_x, screen_y
            else:
                return None, None

        def Det_hp_camp_xyz(addr):
            hp = Game.read_int(addr + 0x230)
            camp = Game.read_int(addr + 0x318)
            x = Game.read_float(addr + 0x2E4 - 0x8)
            y = Game.read_float(addr + 0x2E4 - 0x4)
            z = Game.read_float(addr + 0x2E4) + 69
            return hp, camp, x, y, z

        def draw_red_rectangle(canvas, x1, y1, x2, y2):
            canvas.create_rectangle(x1, y1, x2, y2, outline="red", fill="")

        def update_window_position():
            width, height, x, y, hwnd = get_window_info('Counter-Strike: Global Offensive')

            if hwnd:
                root.geometry(f'{width}x{height}+{x}+{y}')
                canvas.config(width=width, height=height)  # 更新canvas大小

                # 更新矩阵
                matrix_base_address = Game.read_int(Char_Modlue2 + 0x212B60)
                matrix_addr = matrix_base_address + 0x190
                matrix = [Game.read_float(matrix_addr + (i * 16)) for i in range(4)]
                matrix_y = [Game.read_float(matrix_addr + (i * 16) + 4) for i in range(4)]
                matrix_z = [Game.read_float(matrix_addr + (i * 16) + 8) for i in range(4)]
                matrix_w = [Game.read_float(matrix_addr + (i * 16) + 12) for i in range(4)]

                global combined_matrix
                combined_matrix = matrix + matrix_y + matrix_z + matrix_w  # 更新全局矩阵

            root.after(100, update_window_position)  # 每100毫秒调用一次

        def update_and_draw_dots():
            canvas.delete("all")  # 清除画布
            width, height, _, _, _ = get_window_info('Counter-Strike: Global Offensive')

            for i in range(9):  # 假设读取9个敌人
                enemy_addr = Game.read_int(Char_Modlue1 + 0xA7E72C + 0x18 * i)
                if enemy_addr:  # 确保地址有效
                    hp, camp, enemy_x, enemy_y, enemy_z = Det_hp_camp_xyz(enemy_addr)
                    screen_x, screen_y = calculate_screen_coordinates(enemy_x, enemy_y, enemy_z, combined_matrix, width,
                                                                      height)
                    screen_x1, screen_y1 = calculate_screen_coordinates(enemy_x, enemy_y - 30, enemy_z, combined_matrix,
                                                                        width, height)
                    screen_x2, screen_y2 = calculate_screen_coordinates(enemy_x, enemy_y + 30, enemy_z - 69,
                                                                        combined_matrix, width,
                                                                        height)

                    My_addr = Game.read_int(Char_Modlue1 + 0xA7E714)
                    Camp = Det_hp_camp_xyz(My_addr)[1]
                    My_x = Det_hp_camp_xyz(My_addr)[2]
                    My_y = Det_hp_camp_xyz(My_addr)[3]
                    if camp != Camp:
                        if hp > 0 and screen_x is not None and screen_y is not None and screen_x1 is not None and screen_y1 is not None:
                            if screen_x2 is not None and screen_y2 is not None:
                                num = (enemy_x - My_x) ** 2 + (enemy_y - My_y) ** 2
                                dis = int(math.sqrt(num))
                                draw_red_rectangle(canvas, screen_x1, screen_y1, screen_x2, screen_y2)

            root.after(10, update_and_draw_dots)  # 每100毫秒更新一次

        root = tk.Tk()
        root.attributes('-transparentcolor', 'white')  # 设置窗口背景为透明
        root.resizable(0, 0)
        root.attributes('-topmost', True)
        root.overrideredirect(True)

        canvas = tk.Canvas(root, width=200, height=200, bg='white', highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)  # 让Canvas填充整个Tkinter窗口

        # 启动更新和绘制
        update_window_position()
        update_and_draw_dots()

        root.mainloop()
    else:
        messagebox.showinfo(title='注意',message='想关闭只能通过下方的一键关闭')



def toggle_execution3():
    sys.exit(1)


window = tk.Tk()
window.title("CSGO测试")
window.resizable(0, 0)
window.geometry("300x150")

lab = tk.Label(window, text='需要什么功能点击即可')
lab.pack(anchor='n', side='left')

# 状态标志
execution_enabled1 = tk.BooleanVar(value=False)
execution_enabled2 = tk.BooleanVar(value=False)
execution_enabled3 = tk.BooleanVar(value=False)

checkbutton1 = tk.Checkbutton(window, text="距离血量", variable=execution_enabled1, command=toggle_execution1)
checkbutton1.pack()

checkbutton2 = tk.Checkbutton(window, text="方框透视", variable=execution_enabled2, command=toggle_execution2)
checkbutton2.pack()

checkbutton3 = tk.Checkbutton(window, text="一键关闭", variable=execution_enabled3, command=toggle_execution3)
checkbutton3.pack()


# 运行 Tkinter 主循环
window.mainloop()


























