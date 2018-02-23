# -*-coding: utf-8-*-

def w1(func):
    def inner():
        # 验证1
        # 验证2
        # 验证3
        return func()

    return inner


@w1
def f1():
    print 'f1'


if __name__ == '__main__':
    f1()