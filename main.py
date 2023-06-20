import random

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

def play_game():
    # 游戏主循环
    while True:
        # display_color_debug(*color)
        user_guess = input("请输入你的猜测（格式为R, G, B）：")
        user_guess = tuple(map(int, user_guess.split(',')))

        if validate_guess(user_guess, *color):
            print("恭喜，你猜对了！")
            break
        else:
            print("很抱歉，你猜错了，请继续尝试。")

# 生成随机颜色并显示色块
color = generate_color()
display_color_block(*color)
# 启动游戏
play_game()
