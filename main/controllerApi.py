import os 
import sys
import datetime
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.service.services import Services 
from src.excel.excelResult import ExcelLibary

class apiController:
    def __init__(self):
        self.objServices = Services()
        self.objexcelResult = ExcelLibary()
        self.direct = os.getcwd()
        self.folerName = 'TestResultApi'
        self.fileName = 'Test_Automation_Results.xlsx'
        self.report_dir = os.path.join(self.direct, self.folerName)
        self.filePath = os.path.join(self.report_dir, self.fileName)

    def runTest(self):
        listResult = self.objServices.validateAPIData()
        self.objexcelResult.saveTestResult(listResult,self.filePath)

def main():
    controller = apiController()
    controller.runTest()


if __name__ == '__main__':
    main()