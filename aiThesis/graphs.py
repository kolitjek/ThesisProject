import seaborn as sns

import matplotlib.pyplot as plt


def create_graph(data, legend, axis):

	for _data in data:
		sns.kdeplot(_data, shade=True)
	# sns.kdeplot(lstmconv2d, shade=True)
	sns.kdeplot(xlabel='common xlabel', ylabel='common ylabel')
	plt.xlabel(axis[0], fontsize=18)
	plt.ylabel(axis[1], fontsize=16)
	plt.legend(legend, prop={'size': 16}, loc='upper right')

	plt.show()
