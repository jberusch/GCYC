import collections
import numpy as np
from app.indiv_aux import get_longitudinal_data, individual_on_track

# PURPOSE: Create matrix of field data for students in group
# returns a list of dictionaries of each student
def get_group_longitudinal_data(group_rows,col_headers,field,to_ignore=[]):
    res = []

    for student_row in group_rows:
        dat = [student_row[0].value] # 1st index in array for student ID
        res.append(dat.append(get_longitudinal_data(student_row,col_headers,field,to_ignore)))

    return res

# PURPOSE: calculate the % of students in the advisory who are on track
# returns floating point # (e.g. 47.25)
def calc_percent_on_track(group_rows,col_headers):
    part, whole = 0, 0
    for student_row in group_rows:
        if individual_on_track(student_row,col_headers):
            part += 1
        whole += 1
    
    return ((part/float(whole)) * 100)

def get_ids_in_group(group_rows):
    res = []
    for student_row in group_rows:
        res.append(student_row[0].value)
    return res

def build_basic_data(group_rows,col_headers):
    res = []
    for student_row in group_rows:
        tmp_stu = {}
        tmp_stu['id'] = student_row[0].value
        tmp_stu['on_track'] = individual_on_track(student_row,col_headers)
        res.append(tmp_stu)

    return res