from aiThesis.load_data import load_win_rate,warrior_base_path,warrior_filtered_path,mcts_single,mcts_sequence,priest_base_path,priest_filtered_path
import sys
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import pandas as pd

sys.path.append("")
itrs = ["1","10","25", "50","100","200","300","400","500","800","1000"]
def main():
	w_vs_w_single_action = prepare_win_rate_analysis(load_win_rate(warrior_base_path,mcts_single),load_win_rate(warrior_filtered_path,mcts_single))
	full_analysis(w_vs_w_single_action,"Warrior single action")

	p_vs_p_single_action = prepare_win_rate_analysis(load_win_rate(priest_base_path, mcts_single),
													 load_win_rate(priest_filtered_path, mcts_single))
	full_analysis(p_vs_p_single_action,"Priest single action")
	plt.show()



def full_analysis(data, plot_title):
	data.plot(x='Iterations', y=['Baseline', 'Filtered'], kind='line')
	plt.title(plot_title)

	segmented_data =segment_data(data)
	create_table(['Baseline', 'Filtered'], [itrs[i] for i in range(len(itrs))],
				 [data['Baseline'].tolist(), data['Filtered'].tolist()],
				 'Win rate (baseline and filtered), ' + plot_title)
	chi2_results = calculate_chi_statistic(segmented_data)
	create_table([itrs[i] for i in range(len(itrs))], ['dof','chi2','p'],
				 chi2_results,
				 'Chi Squared results (per iteration), ' + plot_title)

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

	print(len(x_axis))
	print(len(y_axis))
	print(data)
	print(len(data))
	print(len(data[0]))
	fig, ax = plt.subplots(1)
	ax.set_axis_off()
	table = ax.table(
		cellText=data,
		rowLabels=x_axis,
		colLabels=y_axis,
		rowColours=["lightgray"] * len(data),
		colColours=["lightgray"] * len(data[0]),
		cellLoc='center',
		loc='upper left')

	ax.set_title(label,fontweight="bold")

def calculate_chi_statistic(data):
	count = 0
	collected_results = []

	for data_sample in data:
		chi2, p, dof, expected = chi2_contingency(data_sample)
		results = [dof,round(chi2, 2), round(p, 2)]
		collected_results.append(results)
		count += 1

	return collected_results


if __name__ == "__main__":
	main()

