// Jenkinsfile
pipeline {
    // กำหนดให้รันบน Jenkins Agent ใดก็ได้
    agent any 

    stages {
        stage('Checkout Code') {
            steps {
                // ดึงโค้ดล่าสุดจาก Branch main
                // (ถ้าใช้ Credentials ต้องตั้งค่าใน Job Configuration)
                git branch: 'main', url: 'https://github.com/vinitpra54-blip/python-automation-tool.git'
            }
        }
        
        stage('Prepare Environment') {
            steps {
                // 1. สร้าง Virtual Environment (venv) โดยใช้ Path เต็มของ Python
                // (ใช้ bat สำหรับ Windows)
                // %PYTHON_HOME% คือ Path ที่คุณกำหนดใน Manage Jenkins -> Configure System
                bat '"%PYTHON_HOME%\\python.exe" -m venv venv'
                
                // 2. ติดตั้ง Dependencies ใน venv
                // ใช้ 'call' เพื่อเรียก activate.bat และใช้ '&' เพื่อรันคำสั่งต่อกัน
                bat 'call venv\\Scripts\\activate.bat & pip install -r requirements.txt'
            }
        }
        
        stage('Run All Controllers') {
            steps {
                // 3. รัน Controller ทั้ง 3 ตัวจาก Root Directory (python-automation)
                
                echo 'Starting Web Login Controller...'
                // รัน controllerLoginWeb.py
                bat 'call venv\\Scripts\\activate.bat & python main\\controllerLoginWeb.py'
                
                echo 'Starting API Controller...'
                // รัน controllerApi.py
                bat 'call venv\\Scripts\\activate.bat & python main\\controllerApi.py'
                
                echo 'Starting List Duplication Controller...'
                // รัน controllerListDup.py
                bat 'call venv\\Scripts\\activate.bat & python main\\controllerListDup.py'
            }
        }
        
        stage('Archive Results') {
            steps {
                // 4. เก็บไฟล์ Excel ผลลัพธ์เป็น Artifacts
                // (สมมติว่าไฟล์ผลลัพธ์อยู่ที่ TestResult/Test_Automation_Results.xlsx)
                archiveArtifacts artifacts: 'TestResult/Test_Automation_Results.xlsx', fingerprint: true
            }
        }
    }
}