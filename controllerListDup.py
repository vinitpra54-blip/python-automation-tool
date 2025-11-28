import os 
import sys
import datetime
import time

from src.service.services import Services 

class LoginWebController:
    def __init__(self):
        self.objServices = Services()
    
    def runTest(self):
        listResult = self.objServices.findDupList([1,2,3,5,6,8,9],[3,2,1,5,6,0])
        print("listResult",listResult)

def main():
    controller = LoginWebController()
    controller.runTest()


if __name__ == '__main__':
    main()