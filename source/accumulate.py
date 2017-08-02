import os
import re
from collections import OrderedDict

import numpy as np
from scipy import stats

os.chdir(os.getenv("HOME"))
print(os.getcwd())

# path of output arff file = arff_path
arff_path = 'PycharmProjects/arff_scripts/arff_results/end_result2.arff'
out_file = open(arff_path, 'w+')

# dir in which we have mfcc's of all audio files
search_path = 'PycharmProjects/arff_scripts/csv_samples/bark_honk/'
# os.chdir(search_path)

arff_base_path = 'PycharmProjects/arff_scripts/assimilated_arff_base.txt'

with open(arff_base_path, 'r+') as arff_base:
    out_file.write(arff_base.read())

# mfcc_0 = {}

subdirs = [x[0] for x in os.walk(search_path)]

classes = [n.split('/')[-1] for n in subdirs if n != search_path]

for c in classes[:-1]:
    out_file.write(c + ", ")
out_file.write(classes[-1] + "}\n\n@data\n")

for subdir in subdirs:
    files = os.walk(subdir).__next__()[2]
    if len(files) > 0 and subdir != search_path:
        for fi in files:
            f = open(subdir + '/' + fi, 'r')
            file_name_pattern = r'^anonymous-(\d+)(-...)(.*)\.csv'
            file_type = re.sub(file_name_pattern, r'\1\2', fi)
            print("file_type=%s" % file_type)
            # file_class = classes_map[file_type]  # classify by nominal rather than numeric?
            text = f.read()
            # data = text[text.index("\n"):]

            all_data = text.split("\n")[1:-1]
            data_list = []

            for line in all_data:
                data_list.append([float(n) for n in line.split(';')[3:]])  # ignore first three elements

            frame_times = [float(line.split(';')[1]) for line in all_data if len(line) > 2]

            # mfcc_0_all = [float(line.split(';')[2]) for line in all_data if len(line) > 2]
            # mfcc_0[fi] = np.average(mfcc_0_all)

            for i in range(12):
                mfcc = [n[i] for n in data_list if len(n) != 0]

                mfcc_data = OrderedDict()
                mfcc_data["max"] = max(mfcc)
                mfcc_data["min"] = min(mfcc)
                mfcc_data["range"] = mfcc_data["max"] - mfcc_data["min"]
                mfcc_data["maxPos"] = mfcc.index(mfcc_data["max"])
                mfcc_data["minPos"] = mfcc.index(mfcc_data["min"])
                mfcc_data["amean"] = np.average(mfcc)
                mfcc_data["stddev"] = np.std(mfcc)

                np_mfcc_arr = np.array(mfcc)
                mfcc_data["skewness"] = stats.stats.skew(np_mfcc_arr)
                mfcc_data["kurtosis"] = stats.stats.kurtosis(np_mfcc_arr)
                mfcc_data["quartile1"] = np.percentile(mfcc, 25)
                mfcc_data["quartile2"] = np.percentile(mfcc, 50)
                mfcc_data["quartile3"] = np.percentile(mfcc, 75)
                mfcc_data["iqr1-2"] = mfcc_data["quartile2"] - mfcc_data["quartile1"]
                mfcc_data["iqr2-3"] = mfcc_data["quartile3"] - mfcc_data["quartile2"]
                mfcc_data["iqr1-3"] = mfcc_data["quartile3"] - mfcc_data["quartile1"]

                out_file.write(",".join([str(i[1]) for i in mfcc_data.items()])+",")

            out_file.write(subdir.split("/")[-1] + "\n")  # subdir is the same as the class

            f.close()

out_file.close()
