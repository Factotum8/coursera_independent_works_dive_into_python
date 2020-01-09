import sys

depth = int(sys.argv[1])
print(*[' ' * (depth - i) + '#' * i  for i in range(1, depth + 1)], sep='\n')