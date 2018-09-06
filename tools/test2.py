import time

# 装饰器带参数[权限管理] control: 1/2/3/4
def study_control(control):
    def isstudy(func):  # 传入函数,装饰完返回
        def study(*args, **kwargs):
            if control == 4:
                func(*args, **kwargs)
            else:
                print('小伙子,别睡了,起来学习了...')
        return study
    return isstudy


@study_control(4)
def game():
    time.sleep(1)
    print('不要烦我,我正在玩游戏....')
    time.sleep(2)


@study_control(4)
def run(name):
    time.sleep(1)
    print(name + ':不要烦我,我正在跑步...')
    time.sleep(2)

if __name__ == '__main__':
    # game()

    run('王总')