from aiThesis.load_data import load_win_rate, warrior_base_path,hunter_base_path,hunter_filtered_path, warrior_filtered_path, mcts_single, mcts_sequence, \
	priest_base_path, priest_filtered_path,druid_base_path,druid_filtered_path
import sys
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import pandas as pd

sys.path.append("")
itrs = ["1", "10", "25", "50", "100", "200", "300", "400", "500", "800"]
mcts_type_si = 'Si'
mcts_type_se = 'Se'

def main():
	#internal_itr_evaluation()
	model_vs_model_evaluation()

def model_vs_model_evaluation():
	'''
	w_vs_w_single_action = prepare_win_rate_analysis(load_win_rate(warrior_base_path, mcts_single),
													 load_win_rate(warrior_filtered_path, mcts_single), mcts_type_si)
	w_vs_w_sequential_actions = prepare_win_rate_analysis(load_win_rate(warrior_base_path, mcts_sequence),
														  load_win_rate(warrior_filtered_path, mcts_sequence),
														  mcts_type_se)

	full_analysis_basemodels(w_vs_w_single_action,w_vs_w_sequential_actions, 'Warrior')
	h_vs_h_single_action = prepare_win_rate_analysis(load_win_rate(hunter_base_path, mcts_single),
													 load_win_rate(hunter_filtered_path, mcts_single), mcts_type_si)
	h_vs_h_sequential_actions = prepare_win_rate_analysis(load_win_rate(hunter_base_path, mcts_sequence),
														  load_win_rate(hunter_filtered_path, mcts_sequence),
														  mcts_type_se)
	full_analysis_basemodels(h_vs_h_single_action,h_vs_h_sequential_actions, 'Hunter')
	p_vs_p_single_action = prepare_win_rate_analysis(load_win_rate(priest_base_path, mcts_single),
													 load_win_rate(priest_filtered_path, mcts_single), mcts_type_si)
	p_vs_p_sequential_action = prepare_win_rate_analysis(load_win_rate(priest_base_path, mcts_sequence),
														 load_win_rate(priest_filtered_path, mcts_sequence),
														 mcts_type_se)
	full_analysis_basemodels(p_vs_p_single_action, p_vs_p_sequential_action, 'Priest')
	'''
	d_vs_d_single_action = prepare_win_rate_analysis(load_win_rate(druid_base_path, mcts_single),
													 load_win_rate(druid_filtered_path, mcts_single), mcts_type_si)

	d_vs_d_sequential_action = prepare_win_rate_analysis(load_win_rate(druid_base_path, mcts_sequence),
														 load_win_rate(druid_filtered_path, mcts_sequence),
														 mcts_type_se)

	full_analysis_basemodels(d_vs_d_single_action, d_vs_d_sequential_action, 'Druid')
	'''

	'''
	plt.show()


def internal_itr_evaluation ():
	'''
		w_vs_w_single_action = prepare_win_rate_analysis(load_win_rate(warrior_base_path, mcts_single),
														 load_win_rate(warrior_filtered_path, mcts_single), mcts_type_si)
		w_vs_w_sequential_actions = prepare_win_rate_analysis(load_win_rate(warrior_base_path,mcts_sequence),
															  load_win_rate(warrior_filtered_path,mcts_sequence),mcts_type_se)
		full_analysis(w_vs_w_single_action,w_vs_w_sequential_actions,'Warrior')
		'''
	h_vs_h_single_action = prepare_win_rate_analysis(load_win_rate(hunter_base_path, mcts_single),
													 load_win_rate(hunter_filtered_path, mcts_single), mcts_type_si)
	h_vs_h_sequential_actions = prepare_win_rate_analysis(load_win_rate(hunter_base_path, mcts_sequence),
														  load_win_rate(hunter_filtered_path, mcts_sequence),
														  mcts_type_se)

	full_analysis(h_vs_h_single_action, h_vs_h_sequential_actions, 'Hunter')

	'''
	p_vs_p_single_action = prepare_win_rate_analysis(load_win_rate(priest_base_path, mcts_single),
													 load_win_rate(priest_filtered_path, mcts_single), mcts_type_si)
	p_vs_p_sequential_action = prepare_win_rate_analysis(load_win_rate(priest_base_path, mcts_sequence),
														 load_win_rate(priest_filtered_path, mcts_sequence), mcts_type_se)

	full_analysis(p_vs_p_single_action,p_vs_p_sequential_action,'Priest')
	'''
	'''

	d_vs_d_single_action = prepare_win_rate_analysis(load_win_rate(druid_base_path,mcts_single),
													 load_win_rate(druid_filtered_path,mcts_single),mcts_type_si)

	d_vs_d_sequential_action = prepare_win_rate_analysis(load_win_rate(druid_base_path, mcts_sequence),
													 load_win_rate(druid_filtered_path, mcts_sequence), mcts_type_se)
	full_analysis(d_vs_d_single_action,d_vs_d_sequential_action,'Druid')
	'''
	plt.show()

def full_analysis_basemodels(data_single, data_sequential, hero_type):
	segmented_base_models = prepare_win_rate_and_segment_basemodels(data_single, data_sequential)

	print(segmented_base_models)
	chi_results = calculate_chi_statistic(segmented_base_models)

	create_table([itrs[i] for i in range(len(itrs))], ['dof', 'chi2', 'p', 'Reject H0'],
				 chi_results,
				 'Chi Squared results for base models, ' + hero_type)

def full_analysis(data_single, data_sequential, hero_type):
	data_type_list = ['MCTS_SiN', 'MCTS_SiP', 'MCTS_SeN', 'MCTS_SeP']
	#data_type_list = ['MCTS_SiN', 'MCTS_SiF']

	merged_data = data_single
	merged_data = merged_data.merge(data_sequential)
	merged_data.plot(x='Iterations', y=data_type_list, kind='line')

	#data_single.plot(x='Iterations', y=data_type_list, kind='line')
	plt.title(hero_type + ' win rate')
	plt.legend(fontsize="x-large")
	plt.ylabel('Wins')
	plt.ylim(ymax=100, ymin=0)


	'''

	create_table(data_type_list, [itrs[i] for i in range(len(itrs))],
				 [data_single[data_type_list[0]].tolist(),
				  data_single[data_type_list[1]].tolist()],
				 'Win rate (baseline and filtered), ' + hero_type)
	chi2_results = calculate_chi_statistic(segmented_data_single)

	create_table([itrs[i] for i in range(len(itrs))], ['dof', 'chi2', 'p', 'Reject H0'],
				 chi2_results,
				 'Chi Squared results (per iteration), MCTS_Si, ' + hero_type)
	plt.show()
	'''

	segmented_data_single = segment_data(data_single, mcts_type_si)
	segmented_data_sequence = segment_data(data_sequential, mcts_type_se)
	#print(segmented_data_single)
	#print(segmented_data_sequence)
	#print(data_single.head())

	create_table(data_type_list, [itrs[i] for i in range(len(itrs))],
				 [data_single[data_type_list[0]].tolist(),
				  data_single[data_type_list[1]].tolist(),
				  data_sequential[data_type_list[2]].tolist(),
				  data_sequential[data_type_list[3]].tolist()],
				 'Win rate (baseline and filtered), ' + hero_type)

	chi2_results = calculate_chi_statistic(segmented_data_single)

	print(len(chi2_results))
	create_table([itrs[i] for i in range(len(itrs))], ['dof', 'chi2', 'p','Reject H0'],
				 chi2_results,
				 'Chi Squared results (per iteration), single ' + hero_type)

	chi2_results = calculate_chi_statistic(segmented_data_sequence)
	create_table([itrs[i] for i in range(len(itrs))], ['dof', 'chi2', 'p','Reject H0'],
				 chi2_results,
				 'Chi Squared results (per iteration), sequence, ' + hero_type)
	print(len(chi2_results))

	'''
	'''


def prepare_win_rate_analysis(baseline_data, filtered_data, type):
	baseline_data = baseline_data.rename(columns={'Unnamed: 0': 'Iterations', 'win rate': 'MCTS_' + type+'N'},
										 inplace=False)
	filtered_data = filtered_data.rename(columns={'Unnamed: 0': 'Iterations', 'win rate': 'MCTS_' + type+'P'},
										 inplace=False)
	filtered_data_extracted = filtered_data['MCTS_' + type+'P' ]
	merged_table = baseline_data
	return merged_table.join(filtered_data_extracted)

def prepare_win_rate_and_segment_basemodels(single_data, sequential_data):

	w_vs_w_single_action_normal = single_data[['MCTS_SiN']]
	w_vs_w_sequential_actions_normal = sequential_data[['MCTS_SeN']]
	base_models_df = w_vs_w_single_action_normal
	base_models_df['MCTS_SeN'] = w_vs_w_sequential_actions_normal['MCTS_SeN']

	return segment_data_basemodels(base_models_df)


def segment_data(data, data_type):
	data_table = [[[0 for k in range(2)] for j in range(2)] for i in range(len(data))]
	total_samples = 100
	count = 0
	#print(data.head())
	for index, row in data.iterrows():
		if  row['MCTS_' + data_type+'N'] >= 50 and row['MCTS_' + data_type+'P'] >= 50:
			data_table[count][0][0] = row['MCTS_' + data_type+'N']
			data_table[count][0][1] = total_samples - row['MCTS_' + data_type+'N']
			data_table[count][1][0] = row['MCTS_' + data_type+'P']
			data_table[count][1][1] = total_samples - row['MCTS_' + data_type+'P']

		count += 1

	#print(len(data_table))

	return data_table

def segment_data_basemodels(data):
	data_table = [[[0 for k in range(2)] for j in range(2)] for i in range(len(data))]
	total_samples = 100
	count = 0
	print(data.head(10))
	for index, row in data.iterrows():
		if row['MCTS_' + 'SiN'] >= 50 and row['MCTS_' + 'SeN'] >= 50:
			data_table[count][0][0] = row['MCTS_' + 'SiN']
			data_table[count][0][1] = total_samples - row['MCTS_' + 'SiN']
			data_table[count][1][0] = row['MCTS_' + 'SeN']
			data_table[count][1][1] = total_samples - row['MCTS_' + 'SeN']

		count += 1

	# print(len(data_table))

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
		chi2, p, dof, expected = chi2_contingency(data_sample,correction=True)
		#print(expected)
		results = [dof, round(chi2, 4), round(p, 4), True if p < 0.05 else False]
		collected_results.append(results)
		count += 1

	return collected_results


if __name__ == "__main__":
	main()
