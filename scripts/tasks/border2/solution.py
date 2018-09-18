a = int(input())
b = int(input())
c = a - b * 2

s = ['#' * a] * b
m = ['#' * b + ' ' * c + '#' * b] * c

print('\n'.join(s + m + s))