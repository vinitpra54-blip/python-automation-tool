from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time
import datetime
import yaml
import requests

from src.excel.excelResult import ExcelLibary

class Services:

    def __init__(self):
        self.excel = ExcelLibary()

    def findDupList(self,List_A,List_B):
        set_a = set(List_A)
        set_b = set(List_B)

        duplicate_set = set_a & set_b
        duplicate_list = list(duplicate_set)

        return duplicate_list
    
    def get_ymal(self,pathName):
        with open(pathName,'r') as f:
            self.data = yaml.load(f,Loader=yaml.SafeLoader)
            return self.data
    
    def createFolderSnapshot(self,index): 
        index = index + 1
        outputPath = Path(f'screenshots tc_{index}')
        if not outputPath.exists():
            outputPath.mkdir(parents=True, exist_ok=True)
            
        return outputPath

    def generateFilename(self,prefix,index):
        outputPath = self.createFolderSnapshot(index)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fileName = f"{prefix}_{timestamp}.png"
        fullPath = outputPath/fileName

        return str(fullPath)
    
    def validateLogInWeb(self):
        expectedData = self.get_ymal('../python-automation/src/config/tcWebLogin.yaml')
        listwriteFile=[]
        for index in range(len(expectedData['Data'])):

            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
            driver.get('http://the-internet.herokuapp.com/login')
            
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
            driver.find_element(By.XPATH, "//input[@id='username']").send_keys(expectedData['Data'][index]['userName'])
            driver.find_element(By.XPATH, "//input[@id='password']").send_keys(expectedData['Data'][index]['passWord'])
            fileSnapshot = self.generateFilename("step before click submit button",index)
            driver.save_screenshot(fileSnapshot)

            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(3)
            fileSnapshot = self.generateFilename("step click submit button",index)
            driver.save_screenshot(fileSnapshot)
            contentSubheader = driver.find_element(By.XPATH,"//div[@id='flash']").text.strip().replace('×', '').strip()

            if contentSubheader == 'You logged into a secure area!':
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//a[@class='button secondary radius']")))
                driver.find_element(By.XPATH,"//a[@class='button secondary radius']").click()

                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
                fileSnapshot = self.generateFilename("step click logout button",index)
                driver.save_screenshot(fileSnapshot)

            testResult = "Pass"
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            listTestCase = [
                                [
                                    expectedData['TestCaseName'][index]
                                    ,expectedData['Obective'][index]
                                    ,expectedData['TestStep'][index]
                                    ,expectedData['ExpectedResult'][index]
                                    ,testResult
                                    ,timestamp
                                ]
                            ]
            listwriteFile.append(listTestCase)
            driver.quit()

        return listwriteFile
    

    def validateAPIData(self):
        listwriteFile=[]
        expectedData = self.get_ymal('../python-automation/src/config/tcApi.yaml')
        
        for index in range(len(expectedData['Data'])):
            userId = expectedData['Data'][index]['ID']
            response = requests.get(f'https://reqres.in/api/users/{userId}')
           
            responseCode = response.status_code
            dataResponse = response.json()

            if responseCode == 200 : 
                if dataResponse == expectedData['Data']:
                    testResult = 'Pass'
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    listTestCase = [
                                [
                                    expectedData['TestCaseName'][index]
                                    ,expectedData['Obective'][index]
                                    ,expectedData['TestStep'][index]
                                    ,expectedData['ExpectedResult'][index]
                                    ,testResult
                                    ,timestamp
                                ]
                            ]
                                  
                    listwriteFile.append(listTestCase)
                else:
                    testResult = 'Fail'
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    listTestCase = [
                                [
                                    expectedData['TestCaseName'][index]
                                    ,expectedData['Obective'][index]
                                    ,expectedData['TestStep'][index]
                                    ,expectedData['ExpectedResult'][index]
                                    ,testResult
                                    ,timestamp
                                ]
                            ]
                    listwriteFile.append(listTestCase)
                    
            else : 
                testResult = 'Fail'
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                listTestCase = [
                                [
                                    expectedData['TestCaseName'][index]
                                    ,expectedData['Obective'][index]
                                    ,expectedData['TestStep'][index]
                                    ,expectedData['ExpectedResult'][index]
                                    ,testResult
                                    ,timestamp
                                ]
                            ]
                listwriteFile.append(listTestCase)
                
        return listwriteFile 
    
    def writeExcelResult(self,listwriteFile,filePath):
        excelx = self.excel.saveTestResult(listwriteFile,filePath)
        return excelx
    
def main():
    obj = Services()

    # resultFindDup = obj.findDupList([1,2,3,5,6,8,9],[3,2,1,5,6,0])

if __name__ == '__main__':
    main()


