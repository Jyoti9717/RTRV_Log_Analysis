# required Librery
import pandas as pd
from module_functions import *
from datetime import datetime


def eng_log (args,elp_date,elp_time):
    elp_dt = datetime.strptime(elp_date,"%Y-%m-%d")
    elp_date = datetime.strftime(elp_dt,"%m:%d:%Y")
    with open(args, encoding='cp437') as load_file:
        file_content = load_file.read()
    #Convert file content to list
    li = file_content.split('\n')
    # Node name mentioned after 2 index next to  2nd(means last) occurance of the key "RTRV-SHELF:::"
    node_indx = [idx for idx,val in enumerate(li) if 'RTRV-SHELF:::' in val][-1]+2
    node_Name = li[node_indx][4:-19]
    # Engin start index - Engin Log recording starts from 4th index next to the first occurance of the  key ""diag svc log dengplog (P)" in val"
    start_indx = [idx for idx,val in enumerate(li) if "diag svc log dengplog (P)" in val][0]+4
    # Engin end indx  -  Engin Log end recording index is 3index before last occurance of the key "The end of the log."
    End_indx = [idx for idx,val in enumerate(li) if "The end of the log." in val][-1]-3
    # list of all engine recorded logs
    Engine_logs = li[start_indx:End_indx]
    # index of each engine
    Engine_idx = [idx for idx,val in enumerate(Engine_logs) if 'Engine' in val]
    #Get Engine Point Name
    Engine_Point_Name = [val[3:-13].replace(' ','_') for idx,val in enumerate (Engine_logs) if 'Engine' in val]
    #Split Engine_logs by Engine_point_name
    Engine_logs = str(Engine_logs).split('The end of the log.')
    Engine_logs= [str(i).split('#') for i in Engine_logs]
    # removing '** Engine 1 Point Log **' from each list
    [i.pop(0) for i in Engine_logs]
    # removing " \', \'' " from the end of element and each line of each element of the Engine_logs
    for i in range(len(Engine_logs)):
        for j in range(len(Engine_logs[i])):
            Engine_logs[i][j]=Engine_logs[i][j][ :-4]
    # #remove "\', \'\'," from last line of each list
    for i in range(len(Engine_logs)):
        Engine_logs[i][-1] = Engine_logs[i][-1][:-8]
    #concatinating Node_name,Engine_Name with each logs
    for i in range(len(Engine_logs)):
        for j in range(len(Engine_logs[i])):
            Engine_logs[i][j]=(node_Name+','+Engine_Point_Name[i]+", " + Engine_logs[i][j])
    Engine_logs_tbl = [Engine_logs[i][j] for i in range(len(Engine_logs)) for j in range(len(Engine_logs[i])) if elp_date in Engine_logs[i][j] and elp_time in Engine_logs[i][j]]
    # spliting strings into list element
    Engine_logs_tbl = [str(Engine_logs_tbl[i]).split(',') for i in range(len(Engine_logs_tbl))]
    # Creating DataFrame
    col_name = ['Node_Name', 'Engine', 'TM', 'Val', 'Pt', "Time"]
    Engine_logs_tbl = pd.DataFrame(Engine_logs_tbl, columns=col_name)
    return Engine_logs_tbl


