#import packages
import pandas as pd
import datetime
import gc

#load the csv file 
chunksize=100000
i = 1

mylist = []

for chunk in pd.read_csv(r'H:\Python_files\small_table_four.csv', header=0, chunksize=chunksize, error_bad_lines=False, low_memory=False):
    mylist.append(chunk)
    df = pd.concat(mylist, axis=0)

#delete all the '|' from the columns and seperate the headers
    col_list = [x.split('|') for x in df.columns.values]

#The first header is actually a list that contains all 57 headers. 
#Add 56 more empty columns.
    col_list = col_list[0]
    df = pd.concat([df, pd.DataFrame(columns=list('ABCDEGHIKLMNOPQRSTUVWXYZ123456789abcdefghiklmnopqrstuvwx'))])

#Now, after creating a list of correct headers (col_list), we will make real changes 
#directly to the table.
#Rename the 56 headers with their correct names.
    df.columns = col_list

#Now, work with the rows. Same steps.
    raw_row_list = df.values.tolist()
    row_list = []


    for row in raw_row_list:
        for value in row:
            if type(value) == str: 
                value = value.split('|')
                row_list.append(value)


#Replace all the original rows with new ones
    df = df[0:0]
    new_df = df.append(pd.DataFrame(row_list, columns=col_list))

#set 'TRANS_ID' as the index of the table
    new_df.set_index('TRANS_ID', inplace=True, drop=True)

#Sort the values based on the 'SETL_DT'
    new_df['SETL_DT'] = pd.to_datetime(new_df['SETL_DT'])
    new_df['year_of_SETL_DT'] = new_df['SETL_DT'].dt.year

#Create new dataframes for each year of settle date
    new_df_2k5 = new_df[new_df['year_of_SETL_DT'] == 2005]
    new_df_2k6 = new_df[new_df['year_of_SETL_DT'] == 2006]
    new_df_2k7 = new_df[new_df['year_of_SETL_DT'] == 2007]
    new_df_2k8 = new_df[new_df['year_of_SETL_DT'] == 2008]
    new_df_2k9 = new_df[new_df['year_of_SETL_DT'] == 2009]
    new_df_2k10 = new_df[new_df['year_of_SETL_DT'] == 2010]
    new_df_2k11 = new_df[new_df['year_of_SETL_DT'] == 2011]
    new_df_2k12 = new_df[new_df['year_of_SETL_DT'] == 2012]
    new_df_2k13 = new_df[new_df['year_of_SETL_DT'] == 2013]

#Export new csv files
    string_i = str(i)
    new_df_2k5.to_csv(r'H:\Python_files\till 2013\2005_test_table_%s.csv' %string_i)
    new_df_2k6.to_csv(r'H:\Python_files\till 2013\2006_test_table_%s.csv' %string_i)
    new_df_2k7.to_csv(r'H:\Python_files\till 2013\2007_test_table_%s.csv' %string_i)
    new_df_2k8.to_csv(r'H:\Python_files\till 2013\2008_test_table_%s.csv' %string_i)
    new_df_2k9.to_csv(r'H:\Python_files\till 2013\2009_test_table_%s.csv' %string_i)
    new_df_2k10.to_csv(r'H:\Python_files\till 2013\2010_test_table_%s.csv' %string_i)
    new_df_2k11.to_csv(r'H:\Python_files\till 2013\2011_test_table_%s.csv' %string_i)
    new_df_2k12.to_csv(r'H:\Python_files\till 2013\2012_test_table_%s.csv' %string_i)
    new_df_2k13.to_csv(r'H:\Python_files\till 2013\2013_test_table_%s.csv' %string_i)

    i += 1

del mylist
gc.collect()



