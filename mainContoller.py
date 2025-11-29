import os 
import sys
import datetime
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from main.controllerApi import apiController
from main.controllerLoginWeb import loginWebController
from main.controllerListDup import listDupController
from main.controllerCipher import cipherController

class mainController:
    def __init__(self):
        self.objApiController = apiController()
        self.objLoginWebController = loginWebController()
        self.objListDupController = listDupController()
        self.objCipherController = cipherController()
        
    def runTest(self):
        self.objApiController.runTest()
        self.objLoginWebController.runTest()
        self.objListDupController.runTest()
        self.objCipherController.runTest()

def main():
    controller = mainController()
    controller.runTest()


if __name__ == '__main__':
    main()