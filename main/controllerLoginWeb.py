import os 
import sys
import datetime
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.service.services import Services 
from src.excel.excelResult import ExcelLibary

class LoginWebController:
    def __init__(self):
        self.objServices = Services()
        self.objexcelResult = ExcelLibary()
        self.filePath = '../TestResultLoginWeb/Test_Automation_Results.xlsx'
    
    def runTest(self):
        listResult = self.objServices.validateLogInWeb()
        self.objexcelResult.saveTestResult(listResult,self.filePath)

def main():
    controller = LoginWebController()
    controller.runTest()


if __name__ == '__main__':
    main()