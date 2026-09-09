import numpy as np

#training data
x=np.array([1,2,3,4,5],dtype=float)
y=np.array([20,40,60,80,100],dtype=float)

#initial parameters
w=0.0
b=0.0

learning_rate=0.001
epochs=1000

for epoch in range(epochs):

    #prediction
    y_pred=w*x+b

    #calculate error
    error=y_pred-y

    #mean squared error
    loss=np.mean(error **2)

    #calculate gradients
    dw=np.mean(2*x*error)
    db=np.mean(2*error)

    #update parameters
    w=w-learning_rate*dw
    b=b-learning_rate*db

    if epoch%100==0:
        print(
            f"epoch : {epoch},"
            f"loss : {loss:.4f},"
            f"w : {w:.4f},"
            f"b : {w:.4f}"
        )


print("\nFinal parameters:")
print("w =", w)
print("b =", b)

# Test the model
hours = 6
prediction = w * hours + b

print(f"\nPredicted score for {hours} hours: {prediction:.2f}")