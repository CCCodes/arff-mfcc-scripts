import sys
import os
import glob
import re

sys.path.append('/home/caitlinchou/opensmile-2.3.0/config/')
search_path = 'sound_samples/dog_barks'
# os.chdir(search_path)
print(os.getcwd())
i = 0
list_of_files = []
for root, dir, files in os.walk('sound_samples/dog_barks'):
    print(files)
    for f in files:
        if re.match(r'.*\.wav', f):
            list_of_files.append(root + '/' + f)

print("# Files: %d" % len(list_of_files))
os.chdir('/home/caitlinchou/Documents/')

create_dir = '/home/caitlinchou/Documents/csv_samples/'
if os.path.exists(create_dir) != 1:
    os.mkdir(create_dir)

print(os.getcwd())
for i in list_of_files:
    name1 = re.sub(r'(sound_samples/dog_barks/)(.*)(\.wav)', r'\2', i)
    name1 = re.sub(r'/', '', name1)
    print("i=%s" % i)
    print("name1=%s" % name1)
    os.system(
        'SMILExtract -C ../opensmile-2.3.0/config/MFCC12_0_D_A.conf -I ' + i + ' -csvoutput ' + create_dir + '/' + name1 + '.csv')
