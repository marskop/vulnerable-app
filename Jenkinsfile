pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Static Analysis') {
            steps {
                // Run trufflehog in a Docker container
                bat 'docker run --rm -v %cd%\\app:/app trufflesecurity/trufflehog file /app'

                // Run semgrep in a Docker container
                bat 'docker run --rm -v %cd%\\app:/app returntocorp/semgrep --config=p/ci /app'

                // Run bandit in a Docker container
                bat 'docker run --rm -v %cd%\\app:/app pycqa/bandit bandit -r /app'
            }
        }

        stage('Build') {
            steps {
                bat 'build.bat'
            }
        }

        stage('Dynamic Analysis') {
            steps {
                bat 'docker run --rm -v %cd%\\app:/app zaproxy/zap2docker-stable zap-baseline.py -t http://your-app-url'
                bat 'docker run --rm sqlmap/sqlmap -u https://github.com/marskop/vulnerable-app.git --batch'
            }
        }

        stage('Deploy') {
            steps {
                bat 'deploy.bat'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/target/*.jar', allowEmptyArchive: true
            junit 'target/test-results/*.xml'
        }
    }
}
