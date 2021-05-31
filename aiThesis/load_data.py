import pandas as pd
import pathlib


totalPath = str(pathlib.Path(__file__).parent.absolute())

druid_base_path = "\\data\\base\\DRUID_vs_DRUID\\"
hunter_base_path = "\\data\\base\\HUNTER_vs_HUNTER\\"
warrior_base_path = "\\data\\base\\WARRIOR_vs_WARRIOR\\"
priest_base_path = "\\data\\base\\PRIEST_vs_PRIEST\\"

druid_imp_path = "\\data\\imp\\DRUID_vs_DRUID\\"
hunter_imp_path = "\\data\\imp\\HUNTER_vs_HUNTER\\"
warrior_imp_path = "\\data\\imp\\WARRIOR_vs_WARRIOR\\"
priest_imp_path = "\\data\\imp\\PRIEST_vs_PRIEST\\"

#fixme be aware of raw unexplored children has two underscores between iterations and date

date_and_type_of_file = "__04_29_21.csv"
iterations = ["1", "10", "25", "50", "100", "200", "300", "400", "500", "800", "1000"]


def load_single_file(name_of_file_with_iterations, class_and_version):
	pd.read_csv(totalPath + class_and_version + name_of_file_with_iterations + date_and_type_of_file)

def load_all_files_of_type(name_of_file_without_iterations, class_and_version):
	data = []
	for iteration in iterations:
		data.append(pd.read_csv(totalPath + class_and_version + name_of_file_without_iterations +"_itr_" + iteration + date_and_type_of_file))
	return data
