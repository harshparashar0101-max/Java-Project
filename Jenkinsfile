pipeline {
    agent any

    environment {
        XRAY_BASE_URL = 'https://xray.cloud.getxray.app'
        PROJECT_KEY   = 'LOGI'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/harshparashar0101-max/Java-Project.git'
            }
        }

        stage('Check Maven') {
            steps {
                bat 'mvn -version'
            }
        }

        stage('Run Maven Tests') {
            steps {
                bat 'mvn clean test'
            }
        }

        stage('Publish Test Results in Jenkins') {
            steps {
                junit 'target/surefire-reports/*.xml'
            }
        }

        stage('Authenticate to Xray') {
            steps {
                withCredentials([
                    string(credentialsId: 'XRAY_CLIENT_ID', variable: 'XRAY_CLIENT_ID'),
                    string(credentialsId: 'XRAY_CLIENT_SECRET', variable: 'XRAY_CLIENT_SECRET')
                ]) {
                    bat '''
                    powershell -Command "$body = @{client_id='%XRAY_CLIENT_ID%'; client_secret='%XRAY_CLIENT_SECRET%'} | ConvertTo-Json; $token = Invoke-RestMethod -Method Post -Uri 'https://xray.cloud.getxray.app/api/v2/authenticate' -ContentType 'application/json' -Body $body; Set-Content -Path xray_token.txt -Value $token"
                    '''
                }
            }
        }

       stage('Import Results to Xray') {
            steps {
             bat '''
            powershell -Command "$token = (Get-Content xray_token.txt -Raw).Trim('\\"'); $files = Get-ChildItem 'target/surefire-reports/TEST-*.xml'; foreach ($file in $files) { Invoke-RestMethod -Method Post -Uri 'https://xray.cloud.getxray.app/api/v2/import/execution/junit?projectKey=LOGI' -Headers @{ Authorization = 'Bearer ' + $token } -ContentType 'text/xml' -InFile $file.FullName }"
            '''
    }
}
    }

    post {
        always {
            archiveArtifacts artifacts: 'target/surefire-reports/*.xml', fingerprint: true
        }
    }
}