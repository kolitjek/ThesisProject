from aiThesis.load_data import load_win_rate, warrior_base_path, warrior_filtered_path, mcts_single, mcts_sequence, \
	priest_base_path, priest_filtered_path
import sys
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import pandas as pd

sys.path.append("")
itrs = ["1", "10", "25", "50", "100", "200", "300", "400", "500", "800", "1000"]


def main():
	# w_vs_w_single_action = prepare_win_rate_analysis(load_win_rate(warrior_base_path,mcts_single),load_win_rate(warrior_filtered_path,mcts_single))
	# full_analysis(w_vs_w_single_action,"Warrior single action")

	p_vs_p_single_action = prepare_win_rate_analysis(load_win_rate(priest_base_path, mcts_single),
													 load_win_rate(priest_filtered_path, mcts_single), 'single')
	p_vs_p_sequential_action = prepare_win_rate_analysis(load_win_rate(priest_base_path, mcts_sequence),
														 load_win_rate(priest_filtered_path, mcts_sequence), 'sequence')

	full_analysis(p_vs_p_single_action, p_vs_p_sequential_action, "Priest")
	plt.show()


def full_analysis(data_single, data_sequential, hero_type):
	data_type_list = ['Baseline_single', 'Filtered_single', 'Baseline_sequence', 'Filtered_sequence']
	merged_data = data_single
	merged_data = merged_data.merge(data_sequential)
	merged_data.plot(x='Iterations', y=data_type_list, kind='line')
	plt.title(hero_type + ' win rate')
	plt.ylabel('Wins')
	plt.ylim(ymax=100, ymin=0)

	segmented_data_single = segment_data(data_single, 'single')
	segmented_data_sequence = segment_data(data_sequential, 'sequence')
	print(segmented_data_single)
	print(segmented_data_sequence)

	create_table(data_type_list, [itrs[i] for i in range(len(itrs))],
				 [data_single['Baseline_single'].tolist(),
				  data_single['Filtered_single'].tolist(),
				  data_sequential['Baseline_sequence'].tolist(),
				  data_sequential['Filtered_sequence'].tolist()],
				 'Win rate (baseline and filtered), ' + hero_type)

	chi2_results = calculate_chi_statistic(segmented_data_single)
	create_table([itrs[i] for i in range(len(itrs))], ['dof', 'chi2', 'p'],
				 chi2_results,
				 'Chi Squared results (per iteration), single ' + hero_type)

	chi2_results = calculate_chi_statistic(segmented_data_sequence)
	create_table([itrs[i] for i in range(len(itrs))], ['dof', 'chi2', 'p'],
				 chi2_results,
				 'Chi Squared results (per iteration), sequence, ' + hero_type)



def prepare_win_rate_analysis(baseline_data, filtered_data, type):
	baseline_data = baseline_data.rename(columns={'Unnamed: 0': 'Iterations', 'win rate': 'Baseline_' + type},
										 inplace=False)
	filtered_data = filtered_data.rename(columns={'Unnamed: 0': 'Iterations', 'win rate': 'Filtered_' + type},
										 inplace=False)
	filtered_data_extracted = filtered_data['Filtered_' + type]
	merged_table = baseline_data
	return merged_table.join(filtered_data_extracted)


def segment_data(data, data_type):
	data_table = [[[0 for k in range(2)] for j in range(2)] for i in range(len(data))]
	total_samples = 100
	count = 0
	for index, row in data.iterrows():
		data_table[count][0][0] = row['Baseline_' + data_type]
		data_table[count][0][1] = total_samples - row['Baseline_' + data_type]
		data_table[count][1][0] = row['Filtered_' + data_type]
		data_table[count][1][1] = total_samples - row['Filtered_' + data_type]
		count += 1
	return data_table


def create_table(x_axis, y_axis, data, label):
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

	ax.set_title(label, fontweight="bold")


def calculate_chi_statistic(data):
	count = 0
	collected_results = []

	for data_sample in data:
		chi2, p, dof, expected = chi2_contingency(data_sample)
		results = [dof, round(chi2, 2), round(p, 2)]
		collected_results.append(results)
		count += 1

	return collected_results


if __name__ == "__main__":
	main()
