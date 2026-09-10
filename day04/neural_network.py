import numpy as np


#Activation function
def relu(x):
    return np.maximum(0,x)

#Training data
X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
], dtype=float)

# AND gate
y = np.array([
    [0],
    [0],
    [0],
    [1]
], dtype=float)

#initialize weights and bias
np.random.seed(42)

w1=np.random.randn(2,5)
b1=np.zeros((1,5))

w2=np.random.randn(5,1)
b2=np.zeros((1,1))

learning_rate=0.1
epochs=1000

#Training
for epoch in range (epochs):
    #Forward propagation
    z1=X @ w1 + b1
    a1=relu(z1)

    z2= a1 @ w2 +b2
    prediction=z2

    #loss
    loss=np.mean((prediction-y)** 2)


    #Back Propagation
    dz2=2*(prediction-y)/len(X)

    dw2=a1.T @dz2
    db2=np.sum(dz2,axis=0, keepdims=True)

    da1=dz2 @ w2.T
    dz1=da1 *(z1>0)

    dw1=X.T @dz1
    db1=np.sum(dz1,axis=0,keepdims=True)

    #Update parameters
    w2-=learning_rate*dw2
    b2-=learning_rate*db2

    w1-=learning_rate*dw1
    b1-=learning_rate*db1

    if epoch % 1000 == 0:
        print(f"Epoch: {epoch}, Loss: {loss:.6f}")

#Final prediction
print("\nFinal predictions:")

z1 = X @ w1 + b1
a1 = relu(z1)

z2 = a1 @ w2 + b2

for inputs, prediction in zip(X, z2):
    print(f"{inputs} -> {prediction[0]:.4f}")