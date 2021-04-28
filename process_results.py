import pandas as pd, os, time, base64, pysftp, glob, datetime, pathlib
import matplotlib.pyplot as plt
from scipy.stats import zscore
from dateutil import tz
from itertools import islice
from dotenv import load_dotenv

print("This script will process the results from Ibex farm and display them/save them to a file"
      "in the 'results' directory")

# Assigning env variables for SFTP url, username, and password based on ENV variables
load_dotenv(dotenv_path='.env')

# Load all .env variables
results_location = str(os.environ.get('RESULTS_LOCATION'))
results_processed_location = str(os.environ.get('RESULTS_PROCESSED_LOCATION'))

response_7 = 0
response_6 = 0
response_5 = 0
response_4 = 0
response_3 = 0
response_2 = 0
response_1 = 0
ratings = {}

print('Condition A:')
with open(results_location) as f:
    for line in f:
        if 'cond=a' in line:
            # print(line)
            value_line = ''.join(islice(f, 1))
            if 'NULL,7,NULL' in value_line:
                response_7 += 1
            if 'NULL,6,NULL' in value_line:
                response_6 += 1
            if 'NULL,5,NULL' in value_line:
                response_5 += 1
            if 'NULL,4,NULL' in value_line:
                response_4 += 1
            if 'NULL,3,NULL' in value_line:
                response_3 += 1
            if 'NULL,2,NULL' in value_line:
                response_2 += 1
            if 'NULL,1,NULL' in value_line:
                response_1 += 1

f.close()
ratings = {'7': response_7,
           '6': response_6,
           '5': response_5,
           '4': response_4,
           '3': response_3,
           '2': response_2,
           '1': response_1}

print(ratings)

# data_frame = pd.DataFrame(ratings.items())
data_frame = pd.DataFrame.from_dict(data=ratings, orient='index', dtype=int)

# Create raw chart
fig, ax = plt.subplots()
labels = ['1', '2', '3', '4', '5', '6', '7']
response_sum = [ratings['1'], ratings['2'], ratings['3'], ratings['4'], ratings['5'], ratings['6'], ratings['7']]
ax.bar(labels, response_sum, label='Responses')
ax.set_ylabel('Frequency')
ax.set_xlabel('Responses (unnatural to perfectly natural)')
ax.set_title('Likert Scores for Condition A - Italian Native Speakers')
plt.ylim([0, 210])
plt.savefig('./results/condition_a_italian.png')

# Create z-scored chart
z_scored_data_frame = data_frame.apply(zscore)
fig, ax = plt.subplots()
labels = ['1', '2', '3', '4', '5', '6', '7']
z_scores = [z_scored_data_frame.iloc[6][0], z_scored_data_frame.iloc[5][0], z_scored_data_frame.iloc[4][0],
            z_scored_data_frame.iloc[3][0], z_scored_data_frame.iloc[2][0], z_scored_data_frame.iloc[1][0],
            z_scored_data_frame.iloc[0][0]]
rounded_z_scores = [round(num, 2) for num in z_scores[::-1]]
print(rounded_z_scores)
ax.bar(labels, z_scores, label='Z-Scores')
ax.set_ylabel('Z-Score')
ax.set_xlabel('Responses (unnatural to perfectly natural)')
ax.set_title('Z-Scores for Condition A - Italian Native Speakers')
plt.ylim([-2.45, 2.45])
plt.savefig('./results/z_scores_condition_a_italian.png')

response_7 = 0
response_6 = 0
response_5 = 0
response_4 = 0
response_3 = 0
response_2 = 0
response_1 = 0
ratings = {}

print('Condition B:')
with open(results_location) as f:
    for line in f:
        if 'cond=b' in line:
            # print(line)
            value_line = ''.join(islice(f, 1))
            if 'NULL,7,NULL' in value_line:
                response_7 += 1
            if 'NULL,6,NULL' in value_line:
                response_6 += 1
            if 'NULL,5,NULL' in value_line:
                response_5 += 1
            if 'NULL,4,NULL' in value_line:
                response_4 += 1
            if 'NULL,3,NULL' in value_line:
                response_3 += 1
            if 'NULL,2,NULL' in value_line:
                response_2 += 1
            if 'NULL,1,NULL' in value_line:
                response_1 += 1

f.close()
ratings = {'7': response_7,
           '6': response_6,
           '5': response_5,
           '4': response_4,
           '3': response_3,
           '2': response_2,
           '1': response_1}

print(ratings)

# data_frame = pd.DataFrame(ratings.items())
data_frame = pd.DataFrame.from_dict(data=ratings, orient='index', dtype=int)
fig, ax = plt.subplots()
labels = ['1', '2', '3', '4', '5', '6', '7']
response_sum = [ratings['1'], ratings['2'], ratings['3'], ratings['4'], ratings['5'], ratings['6'], ratings['7']]
ax.bar(labels, response_sum, label='Responses')
ax.set_ylabel('Frequency')
ax.set_xlabel('Responses (unnatural to perfectly natural)')
ax.set_title('Likert Scores for Condition B - Italian Native Speakers')
plt.ylim([0, 210])
plt.savefig('./results/condition_b_italian.png')

# Create z-scored chart
z_scored_data_frame = data_frame.apply(zscore)
fig, ax = plt.subplots()
labels = ['1', '2', '3', '4', '5', '6', '7']
z_scores = [z_scored_data_frame.iloc[6][0], z_scored_data_frame.iloc[5][0], z_scored_data_frame.iloc[4][0],
            z_scored_data_frame.iloc[3][0], z_scored_data_frame.iloc[2][0], z_scored_data_frame.iloc[1][0],
            z_scored_data_frame.iloc[0][0]]
rounded_z_scores = [round(num, 2) for num in z_scores[::-1]]
print(rounded_z_scores)
ax.bar(labels, z_scores, label='Z-Scores')
ax.set_ylabel('Z-Score')
ax.set_xlabel('Responses (unnatural to perfectly natural)')
ax.set_title('Z-Scores for Condition B - Italian Native Speakers')
plt.ylim([-2.45, 2.45])
plt.savefig('./results/z_scores_condition_b_italian.png')

response_7 = 0
response_6 = 0
response_5 = 0
response_4 = 0
response_3 = 0
response_2 = 0
response_1 = 0
ratings = {}

print('Condition C:')
with open(results_location) as f:
    for line in f:
        if 'cond=c' in line:
            # print(line)
            value_line = ''.join(islice(f, 1))
            if 'NULL,7,NULL' in value_line:
                response_7 += 1
            if 'NULL,6,NULL' in value_line:
                response_6 += 1
            if 'NULL,5,NULL' in value_line:
                response_5 += 1
            if 'NULL,4,NULL' in value_line:
                response_4 += 1
            if 'NULL,3,NULL' in value_line:
                response_3 += 1
            if 'NULL,2,NULL' in value_line:
                response_2 += 1
            if 'NULL,1,NULL' in value_line:
                response_1 += 1

f.close()
ratings = {'7': response_7,
           '6': response_6,
           '5': response_5,
           '4': response_4,
           '3': response_3,
           '2': response_2,
           '1': response_1}

print(ratings)

# data_frame = pd.DataFrame(ratings.items())
data_frame = pd.DataFrame.from_dict(data=ratings, orient='index', dtype=int)
fig, ax = plt.subplots()
labels = ['1', '2', '3', '4', '5', '6', '7']
response_sum = [ratings['1'], ratings['2'], ratings['3'], ratings['4'], ratings['5'], ratings['6'], ratings['7']]
ax.bar(labels, response_sum, label='Responses')
ax.set_ylabel('Frequency')
ax.set_xlabel('Responses (unnatural to perfectly natural)')
ax.set_title('Likert Scores for Condition C - Italian Native Speakers')
plt.ylim([0, 210])
plt.savefig('./results/condition_c_italian.png')

# Create z-scored chart
z_scored_data_frame = data_frame.apply(zscore)
fig, ax = plt.subplots()
labels = ['1', '2', '3', '4', '5', '6', '7']
z_scores = [z_scored_data_frame.iloc[6][0], z_scored_data_frame.iloc[5][0], z_scored_data_frame.iloc[4][0],
            z_scored_data_frame.iloc[3][0], z_scored_data_frame.iloc[2][0], z_scored_data_frame.iloc[1][0],
            z_scored_data_frame.iloc[0][0]]
rounded_z_scores = [round(num, 2) for num in z_scores[::-1]]
print(rounded_z_scores)
ax.bar(labels, z_scores, label='Z-Scores')
ax.set_ylabel('Z-Score')
ax.set_xlabel('Responses (unnatural to perfectly natural)')
ax.set_title('Z-Scores for Condition C - Italian Native Speakers')
plt.ylim([-2.45, 2.45])
plt.savefig('./results/z_scores_condition_c_italian.png')

response_7 = 0
response_6 = 0
response_5 = 0
response_4 = 0
response_3 = 0
response_2 = 0
response_1 = 0
ratings = {}

print('Condition D:')
with open(results_location) as f:
    for line in f:
        if 'cond=d' in line:
            # print(line)
            value_line = ''.join(islice(f, 1))
            if 'NULL,7,NULL' in value_line:
                response_7 += 1
            if 'NULL,6,NULL' in value_line:
                response_6 += 1
            if 'NULL,5,NULL' in value_line:
                response_5 += 1
            if 'NULL,4,NULL' in value_line:
                response_4 += 1
            if 'NULL,3,NULL' in value_line:
                response_3 += 1
            if 'NULL,2,NULL' in value_line:
                response_2 += 1
            if 'NULL,1,NULL' in value_line:
                response_1 += 1

f.close()
ratings = {'7': response_7,
           '6': response_6,
           '5': response_5,
           '4': response_4,
           '3': response_3,
           '2': response_2,
           '1': response_1}

print(ratings)

# data_frame = pd.DataFrame(ratings.items())
data_frame = pd.DataFrame.from_dict(data=ratings, orient='index', dtype=int)
fig, ax = plt.subplots()
labels = ['1', '2', '3', '4', '5', '6', '7']
response_sum = [ratings['1'], ratings['2'], ratings['3'], ratings['4'], ratings['5'], ratings['6'], ratings['7']]
ax.bar(labels, response_sum, label='Responses')
ax.set_ylabel('Frequency')
ax.set_xlabel('Responses (unnatural to perfectly natural)')
ax.set_title('Likert Scores for Condition D - Italian Native Speakers')
plt.ylim([0, 210])
plt.savefig('./results/condition_d_italian.png')

# Create z-scored chart
z_scored_data_frame = data_frame.apply(zscore)
fig, ax = plt.subplots()
labels = ['1', '2', '3', '4', '5', '6', '7']
z_scores = [z_scored_data_frame.iloc[6][0], z_scored_data_frame.iloc[5][0], z_scored_data_frame.iloc[4][0],
            z_scored_data_frame.iloc[3][0], z_scored_data_frame.iloc[2][0], z_scored_data_frame.iloc[1][0],
            z_scored_data_frame.iloc[0][0]]
rounded_z_scores = [round(num, 2) for num in z_scores[::-1]]
print(rounded_z_scores)
ax.bar(labels, z_scores, label='Z-Scores')
ax.set_ylabel('Z-Score')
ax.set_xlabel('Responses (unnatural to perfectly natural)')
ax.set_title('Z-Scores for Condition D - Italian Native Speakers')
plt.ylim([-2.45, 2.45])
plt.savefig('./results/z_scores_condition_d_italian.png')

response_7 = 0
response_6 = 0
response_5 = 0
response_4 = 0
response_3 = 0
response_2 = 0
response_1 = 0
ratings = {}

print('Condition E:')
with open(results_location) as f:
    for line in f:
        if 'cond=e' in line:
            # print(line)
            value_line = ''.join(islice(f, 1))
            if 'NULL,7,NULL' in value_line:
                response_7 += 1
            if 'NULL,6,NULL' in value_line:
                response_6 += 1
            if 'NULL,5,NULL' in value_line:
                response_5 += 1
            if 'NULL,4,NULL' in value_line:
                response_4 += 1
            if 'NULL,3,NULL' in value_line:
                response_3 += 1
            if 'NULL,2,NULL' in value_line:
                response_2 += 1
            if 'NULL,1,NULL' in value_line:
                response_1 += 1

f.close()
ratings = {'7': response_7,
           '6': response_6,
           '5': response_5,
           '4': response_4,
           '3': response_3,
           '2': response_2,
           '1': response_1}

print(ratings)

# data_frame = pd.DataFrame(ratings.items())
data_frame = pd.DataFrame.from_dict(data=ratings, orient='index', dtype=int)
fig, ax = plt.subplots()
labels = ['1', '2', '3', '4', '5', '6', '7']
response_sum = [ratings['1'], ratings['2'], ratings['3'], ratings['4'], ratings['5'], ratings['6'], ratings['7']]
ax.bar(labels, response_sum, label='Responses')
ax.set_ylabel('Frequency')
ax.set_xlabel('Responses (unnatural to perfectly natural)')
ax.set_title('Likert Scores for Condition E - Italian Native Speakers')
plt.ylim([0, 210])
plt.savefig('./results/condition_e_italian.png')

# Create z-scored chart
z_scored_data_frame = data_frame.apply(zscore)
fig, ax = plt.subplots()
labels = ['1', '2', '3', '4', '5', '6', '7']
z_scores = [z_scored_data_frame.iloc[6][0], z_scored_data_frame.iloc[5][0], z_scored_data_frame.iloc[4][0],
            z_scored_data_frame.iloc[3][0], z_scored_data_frame.iloc[2][0], z_scored_data_frame.iloc[1][0],
            z_scored_data_frame.iloc[0][0]]
rounded_z_scores = [round(num, 2) for num in z_scores[::-1]]
print(rounded_z_scores)
ax.bar(labels, z_scores, label='Z-Scores')
ax.set_ylabel('Z-Score')
ax.set_xlabel('Responses (unnatural to perfectly natural)')
ax.set_title('Z-Scores for Condition E - Italian Native Speakers')
plt.ylim([-2.45, 2.45])
plt.savefig('./results/z_scores_condition_e_italian.png')

response_7 = 0
response_6 = 0
response_5 = 0
response_4 = 0
response_3 = 0
response_2 = 0
response_1 = 0
ratings = {}

print('Condition F:')
with open(results_location) as f:
    for line in f:
        if 'cond=f' in line:
            # print(line)
            value_line = ''.join(islice(f, 1))
            if 'NULL,7,NULL' in value_line:
                response_7 += 1
            if 'NULL,6,NULL' in value_line:
                response_6 += 1
            if 'NULL,5,NULL' in value_line:
                response_5 += 1
            if 'NULL,4,NULL' in value_line:
                response_4 += 1
            if 'NULL,3,NULL' in value_line:
                response_3 += 1
            if 'NULL,2,NULL' in value_line:
                response_2 += 1
            if 'NULL,1,NULL' in value_line:
                response_1 += 1

f.close()
ratings = {'7': response_7,
           '6': response_6,
           '5': response_5,
           '4': response_4,
           '3': response_3,
           '2': response_2,
           '1': response_1}

print(ratings)

# data_frame = pd.DataFrame(ratings.items())
data_frame = pd.DataFrame.from_dict(data=ratings, orient='index', dtype=int)
fig, ax = plt.subplots()
labels = ['1', '2', '3', '4', '5', '6', '7']
response_sum = [ratings['1'], ratings['2'], ratings['3'], ratings['4'], ratings['5'], ratings['6'], ratings['7']]
ax.bar(labels, response_sum, label='Responses')
ax.set_ylabel('Frequency')
ax.set_xlabel('Responses (unnatural to perfectly natural)')
ax.set_title('Likert Scores for Condition F - Italian Native Speakers')
plt.ylim([0, 210])
plt.savefig('./results/condition_f_italian.png')

# Create z-scored chart
z_scored_data_frame = data_frame.apply(zscore)
fig, ax = plt.subplots()
labels = ['1', '2', '3', '4', '5', '6', '7']
z_scores = [z_scored_data_frame.iloc[6][0], z_scored_data_frame.iloc[5][0], z_scored_data_frame.iloc[4][0],
            z_scored_data_frame.iloc[3][0], z_scored_data_frame.iloc[2][0], z_scored_data_frame.iloc[1][0],
            z_scored_data_frame.iloc[0][0]]
rounded_z_scores = [round(num, 2) for num in z_scores[::-1]]
print(rounded_z_scores)
ax.bar(labels, z_scores, label='Z-Scores')
ax.set_ylabel('Z-Score')
ax.set_xlabel('Responses (unnatural to perfectly natural)')
ax.set_title('Z-Scores for Condition F - Italian Native Speakers')
plt.ylim([-2.45, 2.45])
plt.savefig('./results/z_scores_condition_f_italian.png')

response_7 = 0
response_6 = 0
response_5 = 0
response_4 = 0
response_3 = 0
response_2 = 0
response_1 = 0
ratings = {}

print('Condition G:')
with open(results_location) as f:
    for line in f:
        if 'cond=g' in line:
            # print(line)
            value_line = ''.join(islice(f, 1))
            if 'NULL,7,NULL' in value_line:
                response_7 += 1
            if 'NULL,6,NULL' in value_line:
                response_6 += 1
            if 'NULL,5,NULL' in value_line:
                response_5 += 1
            if 'NULL,4,NULL' in value_line:
                response_4 += 1
            if 'NULL,3,NULL' in value_line:
                response_3 += 1
            if 'NULL,2,NULL' in value_line:
                response_2 += 1
            if 'NULL,1,NULL' in value_line:
                response_1 += 1

f.close()
ratings = {'7': response_7,
           '6': response_6,
           '5': response_5,
           '4': response_4,
           '3': response_3,
           '2': response_2,
           '1': response_1}

print(ratings)

# data_frame = pd.DataFrame(ratings.items())
data_frame = pd.DataFrame.from_dict(data=ratings, orient='index', dtype=int)
fig, ax = plt.subplots()
labels = ['1', '2', '3', '4', '5', '6', '7']
response_sum = [ratings['1'], ratings['2'], ratings['3'], ratings['4'], ratings['5'], ratings['6'], ratings['7']]
ax.bar(labels, response_sum, label='Responses')
ax.set_ylabel('Frequency')
ax.set_xlabel('Responses (unnatural to perfectly natural)')
ax.set_title('Likert Scores for Condition G - Italian Native Speakers')
plt.ylim([0, 210])
plt.savefig('./results/condition_g_italian.png')

# Create z-scored chart
z_scored_data_frame = data_frame.apply(zscore)
fig, ax = plt.subplots()
labels = ['1', '2', '3', '4', '5', '6', '7']
z_scores = [z_scored_data_frame.iloc[6][0], z_scored_data_frame.iloc[5][0], z_scored_data_frame.iloc[4][0],
            z_scored_data_frame.iloc[3][0], z_scored_data_frame.iloc[2][0], z_scored_data_frame.iloc[1][0],
            z_scored_data_frame.iloc[0][0]]
rounded_z_scores = [round(num, 2) for num in z_scores[::-1]]
print(rounded_z_scores)
ax.bar(labels, z_scores, label='Z-Scores')
ax.set_ylabel('Z-Score')
ax.set_xlabel('Responses (unnatural to perfectly natural)')
ax.set_title('Z-Scores for Condition G - Italian Native Speakers')
plt.ylim([-2.45, 2.45])
plt.savefig('./results/z_scores_condition_g_italian.png')

response_7 = 0
response_6 = 0
response_5 = 0
response_4 = 0
response_3 = 0
response_2 = 0
response_1 = 0
ratings = {}

print('Condition H:')
with open(results_location) as f:
    for line in f:
        if 'cond=h' in line:
            # print(line)
            value_line = ''.join(islice(f, 1))
            if 'NULL,7,NULL' in value_line:
                response_7 += 1
            if 'NULL,6,NULL' in value_line:
                response_6 += 1
            if 'NULL,5,NULL' in value_line:
                response_5 += 1
            if 'NULL,4,NULL' in value_line:
                response_4 += 1
            if 'NULL,3,NULL' in value_line:
                response_3 += 1
            if 'NULL,2,NULL' in value_line:
                response_2 += 1
            if 'NULL,1,NULL' in value_line:
                response_1 += 1

f.close()
ratings = {'7': response_7,
           '6': response_6,
           '5': response_5,
           '4': response_4,
           '3': response_3,
           '2': response_2,
           '1': response_1}

print(ratings)

# data_frame = pd.DataFrame(ratings.items())
data_frame = pd.DataFrame.from_dict(data=ratings, orient='index', dtype=int)
fig, ax = plt.subplots()
labels = ['1', '2', '3', '4', '5', '6', '7']
response_sum = [ratings['1'], ratings['2'], ratings['3'], ratings['4'], ratings['5'], ratings['6'], ratings['7']]
ax.bar(labels, response_sum, label='Responses')
ax.set_ylabel('Frequency')
ax.set_xlabel('Responses (unnatural to perfectly natural)')
ax.set_title('Likert Scores for Condition H - Italian Native Speakers')
plt.ylim([0, 210])
plt.savefig('./results/condition_h_italian.png')

# Create z-scored chart
z_scored_data_frame = data_frame.apply(zscore)
fig, ax = plt.subplots()
labels = ['1', '2', '3', '4', '5', '6', '7']
z_scores = [z_scored_data_frame.iloc[6][0], z_scored_data_frame.iloc[5][0], z_scored_data_frame.iloc[4][0],
            z_scored_data_frame.iloc[3][0], z_scored_data_frame.iloc[2][0], z_scored_data_frame.iloc[1][0],
            z_scored_data_frame.iloc[0][0]]
rounded_z_scores = [round(num, 2) for num in z_scores[::-1]]
print(rounded_z_scores)
ax.bar(labels, z_scores, label='Z-Scores')
ax.set_ylabel('Z-Score')
ax.set_xlabel('Responses (unnatural to perfectly natural)')
ax.set_title('Z-Scores for Condition H - Italian Native Speakers')
plt.ylim([-2.45, 2.45])
plt.savefig('./results/z_scores_condition_h_italian.png')


print("Done.")
