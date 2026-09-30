\# Day 06 - Transformers \& Attention



\## Topics Learned



\- Transformer architecture

\- Attention

\- Self-attention

\- Query, Key and Value

\- Positional information

\- Encoder and decoder

\- Tokenization

\- Pretrained Transformer models

\- Hugging Face Transformers



\## Practical Work



\- Loaded a pretrained Transformer model

\- Performed sentiment classification

\- Tokenized text using a pretrained tokenizer

\- Inspected tokens and token IDs



\## Key Takeaway



Transformers use attention mechanisms to capture relationships between tokens.

They form the architectural foundation of many modern NLP and Generative AI models.





1.What is a Transformer?

A Transformer is a neural network architecture that uses attention mechanisms to model relationships between tokens and is widely used in NLP and modern Generative AI.





2.Why were Transformers introduced?

Older sequence models such as RNN's processed text sequentially, this makes it difficult to efficiently capture relationships between distant words. To resolve this transformers were introduced where transformers attention mechanism allows model to consider relationship between tokens more directly.



3.What is attention?

Attention is determining which other token the model should pay attention to while processing this token. Attention determines how much importance each token should give to other tokens.

Attention computes relevance scores between tokens and uses those scores to create a weighted combination of their representations.



4.What is self-attention?

Self attention determines how much importance each token should give to other tokens. Since Query, Key and Value come from same input sequence it is called self-attention.



5.What are Query, Key and Value?

Query: What information is this token looking for?

Key: What characteristics/information does another token offer for matching?

Value: What information should be contributed if that token is relevant?



6.Why is the Transformer attention mechanism useful?

Attention mechanism calculates how strongly query matches with each key and then uses those scores to combine the values. 



7.Why does a Transformer need positional information?

Some times the position or order of same words alters the entire meaning of a sentence. Transformers process tokens parallelly not in sequential order like RNN's there Transformer need positional information so that model gets information about token position. Positional information allows the model to incorporate order of tokens into its representation. 



8.What is the difference between an encoder and a decoder?

Encoder: builds contextual representations of the input.



Decoder: generates output tokens based on available context.



9.What is BERT?

BERT (Bidirectional Encoder Representations from Transformers) is an encoder-only Transformer model designed to build contextual representations by attending to both left and right context.



10.What is GPT at a high level?

GPT is a family of decoder-only Transformer-based language models that generate text by predicting the next token based on the preceding context.



11.What is a tokenizer?

Tokenizer is a tool that breaks raw text into pieces of text called tokens and assigns them a numbers called token ids so that a machine learning model can process them.



12.What happens when you give text to a pretrained Transformer model?

Input text is first tokenized into tokens and converted into token ids. These ids are mapped to embeddings and combined with positional information. Then representation pass through transformation layers where self attention allows the model to capture relationship between tokens. Feed forward layers further transform representation. Finally the model produces an output appropriate for its task.



13.What is the difference between training a model and using a pretrained model?

Training a model involves optimizing its parameters using data. Training from scratch starts with randomly initialized parameters and requires large amounts of data and compute. A pretrained model has already undergone training and learned useful patterns, so we can use it directly or further fine-tune it for a specific task.



14.Why are Transformers important for Generative AI?

Transformers are important for Generative AI because their attention mechanism allows models to capture relationships between tokens efficiently, while their architecture supports highly parallel computation during training. Decoder-based Transformers can generate text autoregressively by predicting the next token based on previous context.





Training



Transformers can process many tokens in parallel.



Generation



A decoder-only LLM generally generates:



Token 1

&#x20; ↓

Token 2

&#x20; ↓

Token 3

&#x20; ↓

Token 4

...



So don't say:



"GPT generates the whole sentence simultaneously."



It generally generates tokens autoregressively, one new token at a time.





