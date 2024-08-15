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
                sh 'trufflehog --regex --entropy=True /app'
                sh 'semgrep --config=p/ci /app'
                sh 'bandit -r /app'
            }
        }
          stage('Build') {
            steps {
                sh './build.sh'
            }
        }

        stage('Dynamic Analysis') {
            steps {
                sh 'docker run --rm -v $(pwd)/app:/app zaproxy/zap2docker-stable zap-baseline.py -t http://your-app-url'
                sh 'docker run --rm sqlmap/sqlmap -u http://your-app-url --batch'
            }
        }

        stage('Deploy') {
            steps {
                sh './deploy.sh'
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
