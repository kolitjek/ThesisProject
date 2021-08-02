import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def create_graph(data, legend, axis, path):

	for _data in data:
		sns.kdeplot(_data, shade=True)
	# sns.kdeplot(lstmconv2d, shade=True)
	sns.kdeplot(xlabel='common xlabel', ylabel='common ylabel')
	plt.xlabel(axis[0], fontsize=18)
	plt.ylabel(axis[1], fontsize=16)
	plt.legend(legend, prop={'size': 16}, loc='upper right')

	plt.savefig(path)
	plt.clf()


def create_line_graph(x, y, axis, label, path, ylim = None):
	for i in range(0, len(x)):
		plt.plot(x[i], y[i], label= label[i])
	plt.xlabel(axis[0], fontsize=18)
	plt.ylabel(axis[1], fontsize=16)

	if ylim is not None:
		plt.ylim(0, ylim)

	plt.legend()
	plt.savefig(path)
	plt.clf()

def create_displot(data, path):
	sns.displot(data=data, x="Values" )
	#plt.legend()
	plt.savefig(path)
	plt.clf()



def create_box_plot(labels, data, axis, path):
	# Random test data
	labels_one_list = [item[0] for item in labels]
	fig, ax = plt.subplots()
	ax.boxplot(data)
	ax.set_xticklabels(labels_one_list)
	plt.xlabel(axis[0], fontsize=18)
	plt.ylabel(axis[1], fontsize=16)

	plt.savefig(path)
	plt.clf()


