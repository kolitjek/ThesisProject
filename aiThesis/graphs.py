import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def create_graph(data, legend, axis):

	for _data in data:
		sns.kdeplot(_data, shade=True)
	# sns.kdeplot(lstmconv2d, shade=True)
	sns.kdeplot(xlabel='common xlabel', ylabel='common ylabel')
	plt.xlabel(axis[0], fontsize=18)
	plt.ylabel(axis[1], fontsize=16)
	plt.legend(legend, prop={'size': 16}, loc='upper right')

	plt.show()


def create_line_graph(x, y, axis, label):
	for i in range(0, len(x)):
		plt.plot(x[i], y[i], label= label[i])
	plt.xlabel(axis[0], fontsize=18)
	plt.ylabel(axis[1], fontsize=16)

	plt.legend()
	plt.show()


def create_box_plot(labels, data, axis):
	# Random test data
	labels_one_list = [item[0] for item in labels]
	fig, ax = plt.subplots()
	ax.boxplot(data)
	ax.set_xticklabels(labels_one_list)
	plt.xlabel(axis[0], fontsize=18)
	plt.ylabel(axis[1], fontsize=16)

	plt.show()
	data_0 = ("itr 0", [0,1,2,3,4])
	data_1 = ("itr 1", [5,6,7,8,9])
	data = [data_0 + data_1]
	##write_to_excel(data, "test", "look")
def write_to_excel(data, fileName, observation_type):
	formated_data = [data for data_snippet in data]
	df1 = pd.DataFrame(data[:][1], index=['row 1', 'row 2'],columns=['col 1', 'col 2'])
	df1.to_csv("./data/"+fileName+".csv")
	print(df1)

