#-----------------------------import------------------------------------------#
#-----------------------------------------------------------------------------#
import pandas as pd

from collections import defaultdict


#-----------------------------estimators--------------------------------------#
#-----------------------------------------------------------------------------#
def next_event_estimator_naive(data_frame):
    temporary_indexes = []
    for j in range (0, data_frame.shape[0]):
        temporary_indexes.append(j)
    data_frame["actual_indexes"] = temporary_indexes
    
    df_BPI_sorted = data_frame
    df_BPI_sorted = data_frame.sort_values(by=["case concept:name", "event time:timestamp"], ascending = True).reset_index()
    
    traces = []
    last_trace = []
    for j in range (0, df_BPI_sorted.shape[0] - 1):
        if df_BPI_sorted["case concept:name"][j] == df_BPI_sorted["case concept:name"][j + 1]:
            last_trace.append(df_BPI_sorted["event concept:name"][j])
        else:
            last_trace.append(df_BPI_sorted["event concept:name"][j])
            traces.append(last_trace)
            last_trace = []   
    
    
    N = find_longest_trace(data_frame)
    
    common_events = []
    for i in range (0, N):
        common_events.append(find_most_common_activity_at_position_i(df_BPI_sorted, traces, i))
    
    event_predictions = []
    index = 0
    for j in range (0, df_BPI_sorted.shape[0] - 1):
        if df_BPI_sorted["case concept:name"][j] == df_BPI_sorted["case concept:name"][j + 1]:
            event_predictions.append(common_events[index])
            index += 1
        else:
            event_predictions.append(common_events[index])
            index = 0
    event_predictions.append(common_events[index])
    df_BPI_sorted["Next Predicted Event"] = event_predictions
    
    data_frame = df_BPI_sorted.sort_values(by=["actual_indexes"], ascending = True).reset_index()
    data_frame = data_frame.drop("actual_indexes", axis = 1)
    
    return data_frame
        

#-----------------------------auxiliary---------------------------------------#
#-----------------------------------------------------------------------------#
def find_longest_trace(data_frame):
    concept_names = data_frame["case concept:name"].tolist()
    concept_name_dictionary = defaultdict(int)
    for name in concept_names:
        concept_name_dictionary[name] += 1
    longest_trace = max(concept_name_dictionary.values())
    
    return longest_trace

def find_most_common_activity_at_position_i(df_BPI_sorted, traces, i):
    event_at_position_i = defaultdict(int)
    for trace in traces:
        if (i < len(trace)):
            event_at_position_i[trace[i]] += 1
    
    most_common = max(event_at_position_i.keys())
    
    return most_common

def do_predictions():
    training_file_path = '12689204\BPI_Challenge_2012.XE\BPI_Challenge_2012.XE-training.csv'
    df_BPI = pd.read_csv(training_file_path, sep=',')
    df_BPI = next_event_estimator_naive(df_BPI)
    df_BPI = df_BPI.drop("level_0", axis = 1)
    df_BPI = df_BPI.drop("index", axis = 1)
    
    df_BPI.to_csv("event_log_with_predictions.csv", index=False)

#-----------------------------main--------------------------------------------#
#-----------------------------------------------------------------------------#

do_predictions()
