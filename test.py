import random

elements = ["0", "1", "2", "3", "4", "5", "6" "7", "8", "9", "a", "b", "c", "d", "e", "f"]
code = "#"
for i in range(0, 6):
    code = code + random.choice(elements)
print(code)