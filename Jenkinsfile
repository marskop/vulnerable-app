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
                // Run trufflehog in Docker container
                bat 'docker run --rm -v %cd%\\app:/app marsko/vulnerable-app:latest trufflehog https://github.com/marskop/vulnerable-app.git'
                bat 'echo Trufflehog Exit Code: %ERRORLEVEL%'

                // Run semgrep in Docker container
                bat 'docker run --rm -v %cd%\\app:/app marsko/vulnerable-app:latest semgrep --config=p/ci /app'
                bat 'echo Semgrep Exit Code: %ERRORLEVEL%'

                // Run bandit in Docker container
                // bat 'docker run --rm -v %cd%\\app:/app marsko/vulnerable-app:latest bandit -r /app'
                // bat 'echo Bandit Exit Code: %ERRORLEVEL%'
            }
        }

        // stage('Build') {
        //     steps {
        //         bat 'pip install -r requirements.txt'
        //         bat 'if not exist app.py (echo "Error: app.py not found!" & exit 1)'
        //         echo 'Build completed successfully.'
        //     }
        // }

        stage('Dynamic Analysis') {
            steps {
                // bat 'docker run --rm -v %cd%\\app:/app zaproxy/zap2docker-stable zap-baseline.py -t https://github.com/marskop/vulnerable-app.git'
                bat 'docker run --rm -v %cd%\\app:/app marsko/vulnerable-app:latest sqlmap -u https://github.com/marskop/vulnerable-app.git --batch'
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
