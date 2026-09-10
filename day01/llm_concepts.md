1.What is an LLM?

Ans : LLM means large language module to understand and generate human like language. It is trained on large amount of data.



2.What is the difference between an LLM and a traditional software program?

Ans : Traditional software program is set of instruction written by a programmer that follows specific syntax and other conditions. LLM is trained on large data that uses deep learning and neural networks to predict or generate the possible outcomes.



3\. What is a token?

Ans : Token is part of word or chunks of word that system divides into to analyse.



4\. What is a prompt?

Ans : Prompt is input given to tell what it should do or the question we ask what it should answer.



5\. What is an API?

Ans : API stands for Application programming interface, allows communication between different systems and to share other information.



6\. Why shouldn't we put an API key directly inside Python code?

Ans : API Key is a secret, if we use it directly in python there is risk of others might find that key and use it.



7\. What is the difference between:

Model : Is the back end that takes smart decisions

API : Is the one that communicates between application and model and also helps in transferring information.

Application : Is the program that end user interacts with.







What is a token?

Ans : Token is small parts of text, can be a complete word, part of word or punctuations that ai models use to process and generate. Tokens will be assigned with numbers called token ids. Tokenization depends on tokenizer or model.



What is the difference between a token and an embedding?

Token is used to process the texts.

Embedding is vector of numbers represents information or meaning of texts. means this will be used search semantically similar meaning words or sentences.

Token are used just to process the texts where in embedding is to locate  similar meaning words or sentences.







What is an embedding?

Embedding is vector of numbers that represents information/meaning of texts where semantically similar meaning sentences are located close together.



Why are embeddings useful in RAG?

When we want specific information based on query, using key word search might not be that effective because there may be other words that has similar meaning as query. so using of embeddings will help locate semantically similar meaning of words together and produce most effective answer for the query.





What is cosine similarity?

It calculates how similar two vectors are using mathematical calculation.





Suppose I have:



Query:

"How can I reset my password?"



Document A:

"How to change your password"



Document B:

"How to cook pasta"



Why would an embedding-based search probably rank Document A higher?

When it goes through cosine similarity mathematical calculation, Since document A is similar it will get higher rank.









9/9



What is a machine-learning model?

Based on the given set of training data, which discovers relationship or  patterns between data through mathematical calculations and predicts the upcoming data set. It also calculates loss, adjusts it's weights to reduce loss and produce the most probable outcome.







What is a feature?

feature is input variables or attributes of data that models use to predict.



What is a weight?

Is a parameter that controls relationship between input variable. controls how strongly input influences the prediction.





What is a bias?

Bias is a statistical error from model or deviation of predicted output from an actual expected prediction.



What is loss?

Loss is how wrong the model is. Error is the difference between Actual and predicted output. Loss uses mean squared error function to calculate.





Why do we need a loss function?

Loss function is needed to know how good our prediction model is, low loss means good prediction and high loss means bad prediction.





What is gradient descent?

Gradient descent tells you in which direction the slope is moving, so the model should adjust current weight in the direction that should reduce the error





What does the learning rate control?

learning rate controls how large each update is.





Explain the following pipeline:



Training Data

&#x20;    ↓

Prediction

&#x20;    ↓

Loss

&#x20;    ↓

Gradient

&#x20;    ↓

Weight Update



Once you feed training data to prediction model, it goes through mathematical calculation finds relationship or patterns between data and predicts a weight and output, then it calculates error and the loss. After that it calculates gradient to find in which direction the slope is going and accordingly model adjusts weight to reduce error and runs prediction model again.





What happens when you call model.fit(x, y) in a machine-learning library?

when we call model .fit() we are feeding training data into our model so that our model can learn underlying patterns, relationships or rules. Once this step is complete the model is ready to predict on new data.







10/09



What is a neural network?

Neural network is set of algorithms modeled like or to imitate human brain to help machines identify/understand patterns and relationship, process information and make predictions on new set of data or inputs.



What is a neuron?

Neuron performs weighted sum of its inputs, adds a bias and usually applies an activation function to produce an output.



What is a layer?

Layers are organized group of neurons, that process, transform and pass data forward to learn complex patterns and make predictions.



Why do we use activation functions?

We use activation function to introduce non linearity which allows the model to learn complex data



What is ReLU?

ReLU is a mathematical function we use which returns positive input directly and returns zero if it is negative input.





What is forward propagation?

Forward propagation is input data flows forward through layers to produce a final prediction.





What is backpropagation?

Backpropagation is determining which weight contributed to the error and by how much and then calculating gradient in order to minimize loss or prediction error 



What is a gradient in a neural network?

Gradient is direction of steepest increase in the loss.



What happens when we update weights?

When we update weight to the model, Input and weights passes through different layers and model then makes a prediction. Then the model calculates gradient and adjusts its weight to minimize the prediction error and loss. 



Q10 — Important



Explain this complete process:



Input

&#x20;↓

Weighted sum

&#x20;↓

Activation

&#x20;↓

Prediction

&#x20;↓

Loss

&#x20;↓

Backpropagation

&#x20;↓

Gradient

&#x20;↓

Weight update



Once we provide input to our model, the model performs basic calculations and then applies activation function to introduce non linearity. Input passes through multiple layers and model will make prediction. Once the model make prediction loss will be calculated by using difference between prediction and actual value and mean squared error.

Then the backpropagation process starts where the weights contributed to the error and how much will be determined and then gradient will be calculated to determine the direction of the prediction. gradient is direction of steepest increase in the loss and model should move opposite to that. Model updates the weight accordingly to minimize prediction error.





Q11 — Interview challenge



Why can't we simply use a linear function in every layer of a neural network?

Using linear function in every layer of neural network makes entire neural network collapse into a single linear operation. Single linear equation may not capture complex relationships. It destroys the benefits of depth.



