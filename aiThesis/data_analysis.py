from aiThesis.load_data import load_win_rate,warrior_base_path,warrior_filtered_path,mcts_single,mcts_sequence
import sys
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

sys.path.append("")
itrs = ["1","10","25", "50","100","200","300","400","500","800","1000"]
def main():
	w_vs_w_single_action = prepare_win_rate_analysis(load_win_rate(warrior_base_path,mcts_single),load_win_rate(warrior_filtered_path,mcts_single))
	w_vs_w_single_action_segmented =segment_data(w_vs_w_single_action)
	count = 0

	print(w_vs_w_single_action['Baseline'].tolist())
	'''
	for data_sample in w_vs_w_single_action_segmented:
		print("____________________________")
		print("itr: ", itrs[count])
		print("data: ", data_sample)
		chi2, p, dof, expected = chi2_contingency(data_sample)
		print ("Chi: ", chi2)
		print ("p: ", p)
		print ("dof: ", dof)
		print ("expected: ", expected)
		print("____________________________")



		create_table(['Baseline', 'Filtered'], ['Win', 'Loss'],
					 w_vs_w_single_action_segmented[count],
					 'Win/loss table for ' + itrs[count] + ' iterations (single action filtered)')

		count+=1
	'''
	#print(w_vs_w_single_action.head())

	w_vs_w_single_action.plot(x='Iterations', y=['Baseline','Filtered'], kind='line')
	create_table(['Baseline', 'Filtered'], [itrs[i] for i in range(len(itrs))],
				 [w_vs_w_single_action['Baseline'].tolist(), w_vs_w_single_action['Filtered'].tolist()],
				 'Win rate (baseline and filtered)')
	plt.show()

def prepare_win_rate_analysis (baseline_data, filtered_data):
	baseline_data = baseline_data.rename(columns = {'Unnamed: 0':'Iterations', 'win rate':'Baseline'},inplace=False)
	filtered_data = filtered_data.rename(columns  = {'Unnamed: 0':'Iterations', 'win rate':'Filtered'},inplace=False)
	filtered_data_extracted = filtered_data["Filtered"]
	merged_table = baseline_data
	return merged_table.join(filtered_data_extracted)

def segment_data (data):
	chi_ready_table = [[[0 for k in range(2)] for j in range(2)] for i in range(len(data))]
	total_samples = 100
	count = 0
	for index, row in data.iterrows():
		chi_ready_table[count][0][0] = row['Baseline']
		chi_ready_table[count][0][1] = total_samples - row['Baseline']
		chi_ready_table[count][1][0] = row['Filtered']
		chi_ready_table[count][1][1] = total_samples - row['Filtered']
		count+= 1
	return chi_ready_table

def create_table(x_axis, y_axis, data, label):

	print(x_axis)
	print(y_axis)
	print(data)
	fig, ax = plt.subplots(1)
	ax.set_axis_off()
	table = ax.table(
		cellText=data,
		rowLabels=x_axis,
		colLabels=y_axis,
		rowColours=["lightgray"] * len(data[0]),
		colColours=["lightgray"] * len(data[0]),
		cellLoc='center',
		loc='upper left')

	ax.set_title(label,fontweight="bold")
	plt.show()


if __name__ == "__main__":
	main()

