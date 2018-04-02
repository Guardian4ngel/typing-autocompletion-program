# typing-autocompletion-program

This is a program that conduct IOS-style typing autocompletion. I train and test the program using a large data set consisting of several gigabytes of movie reviews, it typically can save one third of buttons one needed to press in order to type a file. 

In the repository 
1. functions.py: functions used to train model and make predictions
2. parameters.py: specifying which review and how many lines from it will be used to train the model
3. runner.py,grader.py: the runner script to run everything

Use command "python grader.py python -u runner.py" and runner.py will train and predict in the same time. This repository DOESN'T contain test and training data. 

The better performence will be achieved by reading more training samples, however the memory consumption will be high. The margin tend to diminishes if you have already used 3GB of memories.

About methodology:

My program based on the data structure "trie" (https://en.wikipedia.org/wiki/Trie), which reads every word and store them in a tree like structure. Each node of tree corresponds to a prefix and different words share same nodes until they have different prefixes. 
In order to exploit not only the frequency of words, but the relation between neighbouring words. I add not only single words but also expressions made by two neighbouring words to the trie (except if they are separated by punctuation).

In each node, I store the following information: the total number of words/two-word-expressions of training data that has the prefix represented by the node; the top 3 most frequent complete words/two-word-expressions that have this prefix; the count of top 3 most frequent complete words/expressions.

When predicting, given a partially sentence, in general two predictions can be made by trie: one can predict the rest by considering only the current uncomplete word, or considering the (previous complete word)+' '+(current uncomplete word). My trie will return the top three prediction for both (if there exist any), and one can compute their percentage and pick the top three most frequent as the final prediction.
