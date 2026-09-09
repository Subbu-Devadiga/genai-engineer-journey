import numpy as np
from sklearn.linear_model import LinearRegression

model=LinearRegression()
x = np.array([1, 2, 3, 4, 5, 6], dtype=float).reshape(-1,1)

y = np.array([
    3.5,
    5.0,
    6.5,
    8.0,
    10.0,
    12.0
], dtype=float)

model.fit(x,y)

print("weight:",model.coef_[0])
print("Bias:",model.intercept_)

experience=np.array([[7]])
prediction=model.predict(experience)

print("predicted salary :",prediction[0])

