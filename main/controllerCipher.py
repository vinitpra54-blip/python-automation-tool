import os 
import sys
import datetime
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.service.services import Services 

class cipherController:
    def __init__(self):
        self.objServices = Services()
    
    def runTest(self):
        Result = self.objServices.getCipher("VTAOG",2)
        print("Result",Result)

def main():
    controller = cipherController()
    controller.runTest()


if __name__ == '__main__':
    main()