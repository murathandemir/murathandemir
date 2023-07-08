import numpy as np

# (1,2,9,8,4,6,3) 1x7

# (1)
# (2)
# (9)
# (8)
# (4)
# (6)
# (3)

# 7x1

def ApplyTranspose(arr):
    newRowCount = len(arr)
    newArr = [newRowCount][1]
    for i in range(newRowCount):
        newArr[i][1] = arr[i]
