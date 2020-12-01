from openpyxl import load_workbook
import openpyxl
from excel_to_pdf import excel_to_pdf

class ExcelHandler:
    def __init__(self, file_name:str):
        self.file_name = file_name
        self.wb = load_workbook(file_name)
    
    def loadWorksheet(self, worksheet_name:str):
        self.ws = self.wb[worksheet_name]
    
    def save_document(self, output_filename:str, PATH:str):
        self.wb.save(PATH + '{}.xlsx'.format(output_filename))

    def excel_to_pdf(self, file_name:str, path:str):
        excel_to_pdf(file_name, path)

