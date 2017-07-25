import sys
import os
import glob
import re
from collections import OrderedDict
import statistics

os.chdir(os.getenv("HOME"))
print(os.getcwd())

# path of output arff file = arff_path
arff_path = 'Documents/arff_results/end_result.arff'
out_file = open(arff_path, 'w+')

# dir in which we have mfcc's of all audio files
search_path = 'Documents/arff_samples/'
# os.chdir(search_path)

arff_base_path = 'Documents/assimilated_arff_base.txt'

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
        # pattern=re.compile(r'^(.*@data)(.*)$',re.S)
        # data=re.sub(pattern,r'\2',text)
        data = text[text.index("@data") + 6:]  # 6 characters in @data\n

        data_list = []

        for line in data.split('\n'):
            # print("linelength=%d" % line)
            data_list.append([float(n) for n in line.split(',')[3:]])  # ignore first three elements

        for i in range(12):
            print(i)
            mfcc = [n[i] for n in data_list if len(n) != 0]
            mfcc_data = OrderedDict({
                "max": max(mfcc),
                "min": min(mfcc),
                "range": max(mfcc) - min(mfcc),
                "maxPos": mfcc.index(max(mfcc)),
                "minPos": mfcc.index(min(mfcc)),
                "amean": statistics.mean(mfcc),
                "linregc1": "",
                "linregc2": "",
                "linregerrA": "",
                "linregerrQ": "",
                "stddev": "",
                "skewness": "",
                "kurtosis": "",
                "quartile1": "",
                "quartile2": "",
                "quartile3": "",
                "iqr1-2": "",
                "iqr2-3": "",
                "iqr1-3": "",
            })
            print(mfcc_data)

        # data=data.split(',')
        # data=','.join(data[40:268])
        # out_file.write(data+","+str(speaker_no)+'\n')
        f.close()
        break

out_file.close()
