// Jenkinsfile
pipeline {

    agent any 

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/vinitpra54-blip/python-automation-tool.git'
            }
        }
        
        stage('Prepare Environment') {
            steps {
                bat '"%PYTHON_HOME%\\python.exe" -m venv venv'
                bat 'call venv\\Scripts\\activate.bat & pip install -r requirements.txt'
            }
        }
        
        stage('Run All Controllers') {
            steps {
                
                echo 'Starting Web Login Controller...'
                bat 'call venv\\Scripts\\activate.bat & python main\\controllerLoginWeb.py'
                
                echo 'Starting API Controller...'
                bat 'call venv\\Scripts\\activate.bat & python main\\controllerApi.py'
                
                echo 'Starting List Duplication Controller...'
                bat 'call venv\\Scripts\\activate.bat & python main\\controllerListDup.py'
            }
        }
        
        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'TestResultLoginWeb/Test_Automation_Results.xlsx, TestResultApi/Test_Automation_Results.xlsx'
            }
        } 
    }
}