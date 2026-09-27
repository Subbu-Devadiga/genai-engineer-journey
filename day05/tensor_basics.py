import torch

scalar=torch.tensor(5)

vector=torch.tensor([1,2,3])

matrix=torch.tensor([
    [1,2],
    [3,4]
])

print("scalar : ")
print(scalar)

print("\nVector : ")
print(vector)

print("\nMatrix : ")
print(matrix)

print("\n Shape of vector : ")
print(vector.shape)

print("\nShape of matrix : ")
print(matrix.shape)

print("\n Datatype of matrox :")
print(matrix.dtype)

