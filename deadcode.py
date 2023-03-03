#new collumn that indexes events within a case

def addEventNumber(df):
    # df['event_number'] = 0  # initialize new column with zeros
    df = df.assign(event_number=0)
    
    # iterate over each unique case
    for case in df['case concept:name'].unique():
        case_df = df[df['case concept:name'] == case].copy()  # subset dataframe for current case
        size = len(case_df)
        case_df['event_number'] = np.arange(size)  # assign incrementing event numbers
        df.update(case_df)  # update original dataframe with new event numbers
    
    return df

df_eventNum = addEventNumber(df_timeDiff)
df_eventNum.to_csv('check_addEventNumber.csv')
df_eventNum.head(10)

# obsolete method; done alternatively in createNaiveTimePredictor
def getLongestTraceLength(df):
    traceLengths = df.groupby('case concept:name').size()  # count number of events for each trace
    longest_trace_length = traceLengths.max()  # get maximum number of events
    return longest_trace_length

longestTrace = getLongestTraceLength(df_event)

def createNaiveTimePredictor(df):
    # group by event number and calculate mean of time_until_next_event
    df_naiveTimePredictor = df.groupby('event_number')['time_until_next_event'].mean().reset_index()
    return df_naiveTimePredictor

naiveTimePredictor = createNaiveTimePredictor(df_eventNum)
naiveTimePredictor.head(30)