import pandas as pd
import pathlib


totalPath = str(pathlib.Path(__file__).parent.absolute())
mcts_single = "_single_action"
mcts_sequence= "_sequential_actions"

druid_base_path = "\\data_for_analysis\\base\\DRUID_vs_DRUID"
hunter_base_path = "\\data_for_analysis\\base\\HUNTER_vs_HUNTER"
warrior_base_path = "\\data_for_analysis\\base\\WARRIOR_vs_WARRIOR"
priest_base_path = "\\data_for_analysis\\base\\PRIEST_vs_PRIEST"

druid_filtered_path = "\\data_for_analysis\\filtered\\DRUID_vs_DRUID"
hunter_filtered_path = "\\data_for_analysis\\filtered\\HUNTER_vs_HUNTER"
warrior_filtered_path = "\\data_for_analysis\\filtered\\WARRIOR_vs_WARRIOR"
priest_filtered_path = "\\data_for_analysis\\filtered\\PRIEST_vs_PRIEST"

#fixme be aware of raw unexplored children has two underscores between iterations and date

date_and_type_of_file = "_06_20_21.csv"
iterations = ["1", "10", "25", "50", "100", "200", "300", "400", "500", "800", "1000"]

def load_win_rate(class_and_version, mcts_type):
	return pd.read_csv(totalPath+class_and_version+"_win_rate"+mcts_type+date_and_type_of_file)

def load_single_file(name_of_file_with_iterations, class_and_version):
	pd.read_csv(totalPath + class_and_version + name_of_file_with_iterations + date_and_type_of_file)

def load_all_files_of_type(name_of_file_without_iterations, class_and_version):
	data = []
	for iteration in iterations:
		data.append(pd.read_csv(totalPath + class_and_version + name_of_file_without_iterations +"_itr_" + iteration + date_and_type_of_file))
	return data

def load_all_classes_all_itr_of_type(name_of_file, class_and_version):
	data = []
	classes = ["druid", "hunter", "priest", "hunter"]
	[""]
	for _class in classes:
		for iteration in iterations:
			data.append(pd.read_csv(totalPath + _class + name_of_file +"_itr_" + iteration + date_and_type_of_file))
		return data
