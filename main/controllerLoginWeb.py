import os 
import sys
import datetime
import time

from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
base_dir = Path(__file__).resolve().parent.parent
dotenv_path = base_dir / '.env'
load_dotenv(dotenv_path=dotenv_path)

from src.service.services import Services 
from src.excel.excelResult import ExcelLibary

class loginWebController:
    def __init__(self):
        self.objServices = Services()
        self.objexcelResult = ExcelLibary()
        self.direct = os.getcwd()
        self.folerName = 'TestResultLoginWeb'
        self.fileName = 'Test_Automation_Results.xlsx'
        self.report_dir = os.path.join(self.direct, self.folerName)
        self.filePath = os.path.join(self.report_dir, self.fileName)
    
    def runTest(self):
        listCoverPage = self.objServices.coverPage()
        listResultOfWeb = self.objServices.validateLogInWeb()
        listResultOfApi = self.objServices.validateAPIData()

        # self.objexcelResult.saveTestResult(listResult,self.filePath,listCoverPage)
        self.objexcelResult.writeExcel(self.filePath 
                                       ,listCoverPage
                                       ,listResultOfWeb
                                       ,listResultOfApi)


def main():
    controller = loginWebController()
    controller.runTest()


if __name__ == '__main__':
    main()