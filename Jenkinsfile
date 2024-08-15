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
                bat 'trufflehog --regex --entropy=True /app'
                bat 'semgrep --config=p/ci /app'
                bat 'bandit -r /app'
            }
        }
          stage('Build') {
            steps {
                bat './build.bat'
            }
        }

        stage('Dynamic Analysis') {
            steps {
                bat 'docker run --rm -v $(pwd)/app:/app zaproxy/zap2docker-stable zap-baseline.py -t http://your-app-url'
                bat 'docker run --rm sqlmap/sqlmap -u http://your-app-url --batch'
            }
        }

        stage('Deploy') {
            steps {
                bat './deploy.sh'
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
