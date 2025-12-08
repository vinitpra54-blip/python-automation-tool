from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import time
import datetime
import yaml
import requests
import os 
from src.excel.excelResult import ExcelLibary

from dotenv import load_dotenv
base_dir = Path(__file__).resolve().parent.parent
dotenv_path = base_dir / '.env'
load_dotenv(dotenv_path=dotenv_path)

class Services:

    def __init__(self):
        self.excel = ExcelLibary()
        

    def findDupList(self,List_A,List_B):
        set_a = set(List_A)
        set_b = set(List_B)

        duplicate_set = set_a & set_b
        duplicate_list = list(duplicate_set)

        return duplicate_list
    
    def getCipher(self,encrypted, k):

        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lengthAlphabet  = len(alphabet) 
        decrypted_string = ""

        for char in encrypted:
        
            if 'A' <= char <= 'Z':

                original_index = alphabet.find(char)
                # print("original_index",original_index)
                decrypted_index = (original_index - k) % lengthAlphabet
                # decrypted_index ( 21- 2) %26
                decrypted_char = alphabet[decrypted_index] 
                # print("decrypted_char",decrypted_char)

                decrypted_string += decrypted_char
            else:
                decrypted_string += char

        return decrypted_string

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
        expectedData = self.get_ymal('src/config/tcWebLogin.yaml')
        listwriteFile=[]
        testResult = None
        for index in range(len(expectedData['Data'])):
            try:
                chrome_options = Options()
                chrome_options.add_argument("--incognito")
                driver = webdriver.Chrome(options=chrome_options)

                driver.get('http://the-internet.herokuapp.com/login')
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
                driver.find_element(By.XPATH, "//input[@id='username']").send_keys(expectedData['Data'][index]['userName'])
                driver.find_element(By.XPATH, "//input[@id='password']").send_keys(expectedData['Data'][index]['passWord'])
                fileSnapshot = self.generateFilename("step before click submit button",index)
                driver.save_screenshot(fileSnapshot)

                driver.find_element(By.XPATH, "//button[@type='submit']").click()
                time.sleep(2)

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

                elif contentSubheader == 'Your password is invalid!':
                    testResult = "Pass"

                elif contentSubheader == 'Your username is invalid!':
                    testResult = "Pass"

                else:
                    testResult = "Fail"

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
            except Exception as e :
                print(f"Error : {e}")
                listTestCase = [
                                    [
                                        expectedData['TestCaseName'][index]
                                        ,expectedData['Obective'][index]
                                        ,expectedData['TestStep'][index]
                                        ,expectedData['ExpectedResult'][index]
                                        ,e
                                        ,timestamp
                                    ]
                                ]
                listwriteFile.append(listTestCase)

            driver.quit()

        return listwriteFile

    def validateAPIData(self):
        listwriteFile=[]
        testResult = None
        api_key = os.getenv("api_key")
        print("api_key",api_key)

        expectedData = self.get_ymal('src/config/tcApi.yaml')
        for index in range(len(expectedData['Data'])):

            userId = expectedData['Data'][index]['id']
            header = {"x-api-key": api_key }
            response = requests.get(f'https://reqres.in/api/users/{userId}', headers=header)
           
            responseCode = response.status_code
            dataResponse = response.json()

            if responseCode == 200 : 
                dataResponse = dataResponse['data']
                if dataResponse == expectedData['Data'][index]:
                    testResult = 'Pass'
                else:
                    testResult = 'Fail'
            elif responseCode == 404 :
                    if dataResponse == {} :
                        testResult = 'Pass'
                    else:
                        testResult = 'Fail'
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
    
    def coverPage(self):
        listCoverPage = []
        expectedData = self.get_ymal('src/config/converPage.yaml')

        timestamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")

        for index in range(len(expectedData['CoverPage'])):
            testBy = expectedData['CoverPage'][index]['TestBy']
            TestEnv = expectedData['CoverPage'][index]['TestEnv']

            coverPageList = [
                    timestamp
                    ,testBy
                    ,TestEnv
            ]

        listCoverPage.append(coverPageList)

        return listCoverPage
    
def main():
    obj = Services()

    # resultFindDup = obj.findDupList([1,2,3,5,6,8,9],[3,2,1,5,6,0])

if __name__ == '__main__':
    main()
