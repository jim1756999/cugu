
import random
import tkinter as tk
from tkinter import messagebox


# DEV_MODE开关，True时显示答案
DEV_MODE = True
# 容差范围，可调整
TOLERANCE = 10
round_count = 0

def generate_color():
    # 生成随机的RGB颜色值
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b

def display_color_debug(r, g, b):
    # 显示颜色给用户
    print(f"RGB颜色值为：({r}, {g}, {b})")

def display_color_block(r, g, b):
    # 使用ANSI转义码显示颜色块
    color_block = f"\033[48;2;{r};{g};{b}m    \033[0m"
    print(color_block)

def validate_guess(guess, r, g, b):
    # 验证用户的猜测
    if guess[0] == r and guess[1] == g and guess[2] == b:
        return True
    else:
        return False


# 图形界面实现
class ColourGuesserGUI:
    def __init__(self, master):
        self.master = master
        master.title("RGB 颜色猜测游戏")
        self.round_count = 0
        self.wrong_count = 0
        self.color = None

        self.info_label = tk.Label(master, text="请根据下方色块猜测RGB值（0-255）")
        self.info_label.pack(pady=5)

        self.canvas = tk.Canvas(master, width=120, height=60)
        self.canvas.pack(pady=5)

        entry_frame = tk.Frame(master)
        entry_frame.pack(pady=5)
        tk.Label(entry_frame, text="R:").grid(row=0, column=0)
        self.r_entry = tk.Entry(entry_frame, width=5)
        self.r_entry.grid(row=0, column=1)
        tk.Label(entry_frame, text="G:").grid(row=0, column=2)
        self.g_entry = tk.Entry(entry_frame, width=5)
        self.g_entry.grid(row=0, column=3)
        tk.Label(entry_frame, text="B:").grid(row=0, column=4)
        self.b_entry = tk.Entry(entry_frame, width=5)
        self.b_entry.grid(row=0, column=5)


        self.submit_btn = tk.Button(master, text="提交猜测", command=self.submit_guess)
        self.submit_btn.pack(pady=5)

        # 绑定回车事件到三个输入框
        self.r_entry.bind('<Return>', lambda event: self.submit_guess())
        self.g_entry.bind('<Return>', lambda event: self.submit_guess())
        self.b_entry.bind('<Return>', lambda event: self.submit_guess())

        self.result_label = tk.Label(master, text="")
        self.result_label.pack(pady=5)

        self.next_btn = tk.Button(master, text="下一轮", command=self.next_round, state=tk.DISABLED)
        self.next_btn.pack(pady=5)

        self.end_btn = tk.Button(master, text="结束游戏", command=self.end_game)
        self.end_btn.pack(pady=5)

        self.next_round()

    def show_color(self, r, g, b):
        self.canvas.delete("all")
        color_hex = f"#{r:02x}{g:02x}{b:02x}"
        self.canvas.create_rectangle(10, 10, 110, 50, fill=color_hex, outline="black")

        # DEV_MODE下显示RGB答案
        if DEV_MODE:
            self.info_label.config(text=f"请根据下方色块猜测RGB值（0-255）  [答案: {r}, {g}, {b}]")
        else:
            self.info_label.config(text="请根据下方色块猜测RGB值（0-255）")

    def next_round(self):
        self.round_count += 1
        self.wrong_count = 0
        self.color = generate_color()
        self.show_color(*self.color)
        self.r_entry.delete(0, tk.END)
        self.g_entry.delete(0, tk.END)
        self.b_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.submit_btn.config(state=tk.NORMAL)
        self.next_btn.config(state=tk.DISABLED)

    def submit_guess(self):
        try:
            r = int(self.r_entry.get())
            g = int(self.g_entry.get())
            b = int(self.b_entry.get())
            user_guess = (r, g, b)
            if not all(0 <= x <= 255 for x in user_guess):
                raise ValueError
        except Exception:
            messagebox.showerror("输入错误", "请输入0-255之间的整数")
            return

        diff = sum(abs(user_guess[i] - self.color[i]) for i in range(3))
        guess_score = max(0, 100 - diff)
        self.result_label.config(text=f"本次猜测与真实颜色的差距分数：{guess_score}")

        if validate_guess(user_guess, *self.color):
            self.result_label.config(text=f"恭喜，你猜对了！本轮你共猜错了{self.wrong_count}次。\n本次猜测与真实颜色的差距分数：{guess_score}")
            self.submit_btn.config(state=tk.DISABLED)
            self.next_btn.config(state=tk.NORMAL)
        else:
            self.wrong_count += 1
            hints = []
            if user_guess[0] < self.color[0]:
                hints.append("R 偏小")
            elif user_guess[0] > self.color[0]:
                hints.append("R 偏大")
            if user_guess[1] < self.color[1]:
                hints.append("G 偏小")
            elif user_guess[1] > self.color[1]:
                hints.append("G 偏大")
            if user_guess[2] < self.color[2]:
                hints.append("B 偏小")
            elif user_guess[2] > self.color[2]:
                hints.append("B 偏大")
            hint_text = "提示：" + "，".join(hints)
            # 判断是否在正负TOLERANCE范围内
            if all(abs(user_guess[i] - self.color[i]) <= TOLERANCE for i in range(3)):
                self.result_label.config(text=f"你的猜测非常接近，已自动判定为正确！\n正确答案为：R={self.color[0]}, G={self.color[1]}, B={self.color[2]}\n本轮你共猜错了{self.wrong_count}次。\n本次猜测与真实颜色的差距分数：{guess_score}")
                self.submit_btn.config(state=tk.DISABLED)
                self.next_btn.config(state=tk.NORMAL)
            else:
                self.result_label.config(text=f"很抱歉，你猜错了，请继续尝试。\n{hint_text}\n本次猜测与真实颜色的差距分数：{guess_score}")

    def end_game(self):
        messagebox.showinfo("游戏结束", f"游戏结束！你进行了{self.round_count}轮游戏。")
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ColourGuesserGUI(root)
    root.mainloop()
