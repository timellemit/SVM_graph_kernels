import numpy as np
# import matplotlib.pyplot as plt
from sklearn import svm
from toy_molecules_SVM import make_data, graphlet_descriptions

min_nodes = 5
pos_examples, neg_examples, test_examples = make_data(num_pos_examples = 4, 
        num_neg_examples = 3, num_test_examples = 2, num_nodes = 6)

train_desc_vectors = graphlet_descriptions(pos_examples + neg_examples,
    pos_examples + neg_examples, min_nodes)[1]
test_desc_vectors = graphlet_descriptions(test_examples, 
    pos_examples + neg_examples, min_nodes)[1]                                        
X_train, X_test = np.array(train_desc_vectors), np.array(test_desc_vectors)
Y = np.array([1,1,1,1,-1,-1,-1])

# def my_kernel(x, y):
#     """
#     We create a custom kernel:
# 
#                  (2  0)
#     k(x, y) = x  (    ) y.T
#                  (0  1)
#     """
#     M = np.array([[2, 0], [0, 1.0]])
#     return np.dot(np.dot(x, M), y.T)


# we create an instance of SVM and fit out data.
clf = svm.SVC(kernel='rbf')
clf.fit(X_train, Y)
print clf.predict(X_test)