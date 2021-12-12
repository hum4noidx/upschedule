# import xlrd
#
# rb = xlrd.open_workbook('d:/schedule.xlsx')
# sheet = rb.sheet_by_index(0)
# for rownum in range(sheet.nrows):
#     row = sheet.row_values(rownum)
#     for c_el in row:
#         print(c_el)
import pandas as pd

schedule1 = pd.read_excel('d:/schedule.xlsx', index_col='День недели', sheet_name='10',
                          usecols=['День недели', '№Урока', '10мед', 'Кабинет'])

print(schedule1)
