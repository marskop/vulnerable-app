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
                sh 'trufflehog --regex --entropy=True .'
                sh 'semgrep --config=p/ci'
                sh 'bandit -r .'
            }
        }

        stage('Build') {
            steps {
                sh './build.sh'
            }
        }

        stage('Dynamic Analysis') {
            steps {
                sh 'docker run --rm -v $(pwd):/workspace -w /workspace zaproxy/zap2docker-stable zap-baseline.py -t http://your-app-url'
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
