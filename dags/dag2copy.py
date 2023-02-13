import numpy as np
import time
from rshift import *
import random



def matrix_multiplication():
    n = 100
    ''' author - chatgpt '''
    # Create two matrices with random integers
    matrix1 = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]
    matrix2 = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]

    # Record start time
    start_time = time.time()

    # Multiply the matrices
    result = [[sum(a*b for a,b in zip(row_a,col_b)) for col_b in zip(*matrix2)] for row_a in matrix1]
    print(sum([sum(row_a) for row_a in result]))
    # Record end time
    end_time = time.time()

    # Print the result
    # for row in result:
    #     print(row)
    print(f"Time taken: {end_time - start_time}  secs")


# Make(qwe) >> Make(uyiui) >> Make(bbvkj)

Make(matrix_multiplication) 