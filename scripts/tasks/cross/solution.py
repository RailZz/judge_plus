s = int(input())
a = [' ' * s + '*' + ' ' * s] * s
m = ['*' * (s * 2 + 1)]
print('\n'.join(a + m + a))