##############################################################################
#
# An example of creating a chart with Pandas and XlsxWriter.
#
# Copyright 2013, John McNamara, jmcnamara@cpan.org
#

import random
import pandas as pd

Altitudes = [0,4000,6000,10000,14000,18000]
Mach = [0.1,0.3,0.5,0.7,0.9,1.1,1.3,1.5,1.7,1.9]

num_Mach = len(Mach)
num_Altitude = len(Altitudes)

xls = pd.ExcelFile("DragPolarResults2.xlsx")


# Create a Pandas Excel writer using XlsxWriter as the engine.
excel_file = 'DragPolarResults2.xlsx'


writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

# Access the XlsxWriter workbook and worksheet objects from the dataframe.
workbook = writer.book

for sheet_name in pd.ExcelFile(excel_file).sheet_names:
    df = pd.read_excel(xls, sheet_name)
    df.drop(df[df['AoA'] != 4].index, inplace = True)
    df = df.sort_values(by=['Mach'])
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    worksheet = writer.sheets[sheet_name]

    # Create a chart object.
    chart = workbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
    
    # Configure the series of the chart from the dataframe data.
    max_row = len(df)
    for i in range(5,6):
        col = i + 1
        for j in range(0,num_Mach):
            chart.add_series({
                'name':       [sheet_name, 1+j*num_Altitude, 2],
                'categories': [sheet_name, 1, 0, max_row, 0],
                'values':     [sheet_name, 1+num_Altitude*j, col, num_Mach+num_Altitude*j, col],
                'marker':     {'type': 'circle', 'size': 7},
            })
    
    # Configure the chart axes.
    chart.set_x_axis({'name': 'Altitude [m]'})
    chart.set_y_axis({'name': 'CL [-]',
                      'major_gridlines': {'visible': False}})
    
    chart2 = workbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
    max_row = len(df)
    for i in range(6,7):
        col = i + 1
        for j in range(0,num_Mach):   
            chart2.add_series({
                'name':       [sheet_name, 1+j*num_Altitude, 2],
                'categories': [sheet_name, 1, 0, max_row, 0],
                'values':     [sheet_name, 1+num_Altitude*j, col, num_Mach+num_Altitude*j, col],
                'marker':     {'type': 'circle', 'size': 7},
            })
        
    # Configure the chart axes.
    chart2.set_x_axis({'name': 'Altitude [m]'})
    chart2.set_y_axis({'name': 'CD [-]',
                      'major_gridlines': {'visible': False}})

    chart3 = workbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
    max_row = len(df)
    for i in range(7,8):
        col = i + 1
        for j in range(0,num_Mach):   
            chart3.add_series({
                'name':       [sheet_name, 1+j*num_Altitude, 2],
                'categories': [sheet_name, 1, 0, max_row, 0],
                'values':     [sheet_name, 1+num_Altitude*j, col, num_Mach+num_Altitude*j, col],
                'marker':     {'type': 'circle', 'size': 7},
            })
        
    # Configure the chart axes.
    chart3.set_x_axis({'name': 'Altitude [m]'})
    chart3.set_y_axis({'name': 'L/D [-]',
                      'major_gridlines': {'visible': False}})
    
    # Insert the chart into the worksheet.
    worksheet.insert_chart('M2', chart)
    worksheet.insert_chart('V2', chart2)
    worksheet.insert_chart('R20', chart3)



# Close the Pandas Excel writer and output the Excel file.
writer.save()