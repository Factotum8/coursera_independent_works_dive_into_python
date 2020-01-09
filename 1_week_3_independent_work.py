import sys
from math import sqrt

a = int(sys.argv[1])
b = int(sys.argv[2])
c = int(sys.argv[3])



print(int((-b + sqrt(b ** 2 - 4 * a * c)) / (2 * a)))
print(int((-b - sqrt(b ** 2 - 4 * a * c)) / (2 * a)))