import numpy as np
from sklearn.linear_model import LinearRegression

'''
x=np.array([1,2,3,4,5]).reshape(-1,1)
y=np.array([20,40,60,80,100])

model=LinearRegression()

model.fit(x,y)

print("weight:",model.coef_[0])
print("Bias:",model.intercept_)

hours=np.array([[6]])
prediction=model.predict(hours)

print("Prediction:",prediction[0])

'''


x = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)
y = np.array([20, 40, 60, 80, 100])

model = LinearRegression()

model.fit(x, y)

print("Weight:", model.coef_[0])
print("Bias:", model.intercept_)

hours = np.array([[6]])

prediction = model.predict(hours)

print("Predicted score:", prediction[0])