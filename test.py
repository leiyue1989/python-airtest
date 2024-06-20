# -*- encoding=utf8 -*-

def fibonacci(n):
    a = 0
    b = 1
    for _ in range(n):
        yield a
        a, b = b, a + b


for i in fibonacci(11):
    print(i)
