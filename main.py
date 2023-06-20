import random

# 初始化积分和游戏轮数为0
score = 0
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

def play_game():
    # 引用全局的积分和游戏轮数变量
    global score, round_count

    while True:
        # 游戏轮数加一
        round_count += 1
        
        # 生成随机颜色并显示色块
        color = generate_color()
        display_color_block(*color)

        # 游戏主循环
        while True:
            user_guess = input("请输入你的猜测（格式为R, G, B）：")
            user_guess = tuple(map(int, user_guess.split(',')))

            if validate_guess(user_guess, *color):
                print("恭喜，你猜对了！")
                # 猜对颜色后增加分数
                score += 10
                break
            else:
                print("很抱歉，你猜错了，请继续尝试。")
                # 猜错颜色后减少分数
                score -= 5

        choice = input("是否开始新的一轮游戏？（输入 'Y' 继续，输入其他任意键结束）：")
        if choice.upper() != "Y":
            break

# 启动游戏
play_game()

# 游戏结束后，根据得分和游戏轮数提供反馈
if score >= 50:
    print("恭喜你，你的得分很高！")
elif score >= 20:
    print("你的得分不错！继续努力！")
else:
    print("你的得分还有提升空间，加油！")

# 打印游戏轮数
print("游戏结束！你进行了", round_count, "轮游戏。")
