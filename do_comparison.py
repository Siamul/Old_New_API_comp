import sys

template_id_map = {}
id_template_map = {}

with open('./enroll_1N.txt', 'r') as templatemapfile:
    for line in templatemapfile:
        lineparts = line.split(' ')
        template_id_map[lineparts[1].split('/')[-1]] = int(lineparts[0])
        id_template_map[int(lineparts[0])] = lineparts[1].split('/')[-1]

with open('./search_1N.txt', 'r') as templatemapfile:
    for line in templatemapfile:
        lineparts = line.split(' ')
        template_id_map[lineparts[1].split('/')[-1]] = int(lineparts[0])
        id_template_map[int(lineparts[0])] = lineparts[1].split('/')[-1]

old_scores_map = {}
filenames_missing = set()
with open(sys.argv[1], 'r') as oldscoresfile:
    for line in oldscoresfile:
        if len(line) > 0:
            lineparts = line.split(' ')
            filename1 = lineparts[0]
            filename2 = '.'.join(lineparts[1].split('.')[:-1])
            score = float(lineparts[2])
            if filename1 in template_id_map:
                id1 = template_id_map[filename1]
            else:
                filenames_missing.add(filename1)
                continue
            if filename2 in template_id_map:
                id2 = template_id_map[filename2]
            else:
                filenames_missing.add(filename2)
                continue
            if id1 < id2:
                old_scores_map[(id1, id2)] = score
            else:
                old_scores_map[(id2, id1)] = score

#print(template_id_map)
#print(old_scores_map)
#print(filenames_missing)

new_scores_map = {}
first_line = True
with open(sys.argv[2], 'r') as newscoresfile:
    for line in newscoresfile:
        if first_line:
            first_line = False
            continue
        if len(line) > 0:
            lineparts = line.split(' ')
            id1 = int(lineparts[0])
            score = float(lineparts[-1])
            if score == -1:
                id2 = int(lineparts[-3])
            else:
                id2 = int(lineparts[-2])
            if id1 < id2:
                new_scores_map[(id1, id2)] = score
            else:
                new_scores_map[(id2, id1)] = score

#print('Scores missing in old: ', new_scores_map.keys() - old_scores_map.keys())
#print('Scores missing in new: ', old_scores_map.keys() - new_scores_map.keys())

common_keys = set(list(old_scores_map.keys())).intersection(set(list(new_scores_map.keys())))

diffs = []
for key in common_keys:
    diffs.append(abs(old_scores_map[key] - new_scores_map[key]))

print(diffs)

import matplotlib.pyplot as plt
plt.hist(diffs, bins=100, color='skyblue', edgecolor='black')
plt.xlabel('Difference in new and old score')
plt.ylabel('Frequency')
plt.savefig(sys.argv[3] + '_histogram.png')

