pipeline {
    agent any

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

        stage('Publish Test Results') {
            steps {
                junit 'target/surefire-reports/*.xml'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'target/surefire-reports/*.xml', fingerprint: true
        }
    }
}