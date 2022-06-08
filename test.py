from openpyxl import Workbook

wb = Workbook()
ws = wb.active

ws['A4'] = 4
wb.save("test.xlsx")