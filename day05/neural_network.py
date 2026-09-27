import torch
import torch.nn as nn
import torch.optim as optim

# Training data
X = torch.tensor([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
], dtype=torch.float32)

y = torch.tensor([
    [0],
    [0],
    [0],
    [1]
], dtype=torch.float32)

#neural network
class simpleNetwork(nn.Module):

    def __init__(self):
        super().__init__()

        self.hidden=nn.Linear(2,16)
        self.output=nn.Linear(16,1)

    def forward(self,x):
        x=torch.relu(self.hidden(x))
        x=self.output(x)
        return x

model=simpleNetwork()

#loss
loss_function=nn.MSELoss()

optimizer=optim.SGD(
    model.parameters(),
    lr=0.1
)
#Training

epochs=5000

for epoch in range(epochs):
    # forward_pass
    predictions=model(X)


    #calaculate loss
    loss=loss_function(predictions,y)

    #clear previous gradients
    optimizer.zero_grad()

    #backpropagation
    loss.backward()

    #update weights
    optimizer.step()

    if epoch % 500 == 0:
        print(
            f"Epoch: {epoch}, "
            f"Loss: {loss.item():.6f}"
        )




# Test
print("\nFinal predictions:")

with torch.no_grad():

    predictions = model(X)

    for inputs, prediction in zip(X, predictions):
        print(
            f"{inputs.numpy()} -> "
            f"{prediction.item():.4f}"
        )