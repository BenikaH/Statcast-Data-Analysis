import numpy as np
import csv
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

data_file = 'SP_OUTPUT.csv'
target_file = 'TARGET_OUTPUT.csv'

data = np.loadtxt(data_file, delimiter=',')
target_data = np.loadtxt(target_file, delimiter=',')

N = len(target_data)

target_rank = target_data[:,2]
target_percentile = target_rank/N

targets = np.zeros((N))
for i in range(N):
	if target_percentile[i] <= .25:
		targets[i] = 0
	elif target_percentile[i] <= .75:
		targets[i] = 1
	elif target_percentile[i] <= 1:
		targets[i] = 2
	else:
		targets[i] = 3

regression_targets = target_data[:,1]

avg = np.mean(data, axis=0)

stdev = np.std(data, axis=0)

data_scaled = np.subtract(data, avg)

data_scaled = np.divide(data_scaled, stdev)

A_VALS = [.001, .01, .1, 1, 5, 10]
for a in A_VALS:
	print("Alpha value: ",a)
	for r in range(5):
		print("Randomization State: ",r)
		X_train, X_test, y_train, y_test = train_test_split(data_scaled, targets, random_state=r)

		PITCHER_NN = MLPClassifier(solver='lbfgs', random_state=0, hidden_layer_sizes=[10,10], alpha = a).fit(X_train, y_train)
		print("Neural Network")
		print("Model Group Predictions: {}".format(PITCHER_NN.predict(X_test)))
		print("    Actual Group Values: {}".format(y_test))
		print("Training set accuracy: {:.2f}".format(PITCHER_NN.score(X_train, y_train)))
		print("Test set accuracy: {:.2f}".format(PITCHER_NN.score(X_test, y_test)))
	print("--------------------------")
