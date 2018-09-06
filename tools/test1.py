import time

# 计算时间装饰器
def total_time(func):
    def total():
        starttime = time.time()
        func()
        endtime = time.time()
        print(endtime-starttime)
    # 返回函数
    return total


def eat():
    time.sleep(1)
    print('大胃王,正在吃东西....')
    time.sleep(2)


@total_time
def run():
    time.sleep(1)
    print('我正在跑步呢....')
    time.sleep(2)


@total_time
def study():
    time.sleep(2)
    print('我爱学习....')
    time.sleep(2)


if __name__ == '__main__':
    # 问题1: 计算动作时间
    # starttime = time.time()
    # eat()
    # endtime = time.time()
    # print(endtime-starttime)


    # 问题2: 假设100个类似的动作,都要计算时间,怎么办个?
    # 解决: 装饰器
    # run()
    study()