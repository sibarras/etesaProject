from openpyxl import load_workbook
import openpyxl
class ExcelHandler:
    def __init__(self, file_name):
        self.file_name = file_name
        self.wb = load_workbook(file_name)
    
    def loadWorksheet(self, worksheet_name):
        self.ws = self.wb[worksheet_name]
