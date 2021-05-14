def show(matrix):
    for p in range(len(matrix)):
        print(matrix[p])

def Gen2D(length):
    name = [[0 for j in range(length)] for i in range(length)]
    return(name)
    
Matrix = Gen2D(12)
show(Matrix)