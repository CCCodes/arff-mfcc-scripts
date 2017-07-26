import os
import re
from collections import OrderedDict

import numpy as np
from scipy import stats

os.chdir(os.getenv("HOME"))
print(os.getcwd())

# path of output arff file = arff_path
arff_path = 'PycharmProjects/arff_scripts/arff_results/end_result.arff'
out_file = open(arff_path, 'w+')

# dir in which we have mfcc's of all audio files
search_path = 'PycharmProjects/arff_scripts/arff_samples/'
# os.chdir(search_path)

arff_base_path = 'PycharmProjects/arff_scripts/assimilated_arff_base.txt'

with open(arff_base_path, 'r+') as arff_base:
    out_file.write(arff_base.read())

# mapping of speaker names/audio file convention for every speaker to speaker number
# which becomes an attribute of an instance in arff file
speakers = {"puppy.arff": 1, "german-shephard-daniel_simon.arff": 2, "doberman-pincher_daniel-simion.arff": 3,
            "small-dog-barking_daniel-simion.arff": 4}


for root, dir, files in os.walk(search_path):

    for fi in files:
        f = open(root + '/' + fi, 'r')
        file_name_pattern = r'^anonymous-(\d+)(-...)(.*)\.arff'
        file_type = re.sub(file_name_pattern, r'\1\2', fi)
        print("file_type=%s" % file_type)
        speaker_no = speakers[file_type]  # classify by nominal rather than numeric?
        text = f.read()
        data = text[text.index("@data") + 6:]  # 6 characters in @data\n

        all_data = data.split('\n')
        data_list = []

        for line in all_data:
            data_list.append([float(n) for n in line.split(',')[3:]])  # ignore first three elements

        frame_times = [float(line.split(',')[1]) for line in all_data if len(line) > 2]

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

        out_file.write(str(speaker_no)+"\n")

        f.close()

out_file.close()
