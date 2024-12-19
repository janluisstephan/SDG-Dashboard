



x = 50


root = x/2
a = x/root
iteration = 0

while abs(a - root) >.00001:
    root = (root + a)/2
    a = x/root
    iteration = iteration + 1

print(root)
print(iteration)
