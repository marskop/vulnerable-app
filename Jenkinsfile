pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'vulnerable-app'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t vulnerable-app .'
                // script {
                //     dockerImage = docker.build(DOCKER_IMAGE)
                // }
            }
        }
        stage('Static Analysis') {
            steps {
                sh 'pip install bandit'
                sh 'bandit -r .'
                sh 'pip install truffleHog'
                sh 'trufflehog --regex --entropy=True .'
            }
        }
        stage('Run Container') {
            steps {
                script {
                    dockerImage.run("-d -p 5000:5000 --name vuln-app")
                }
            }
        }
        stage('Dynamic Analysis') {
            steps {
                // Nmap for open ports and services
                sh 'nmap -p 5000 localhost'

                // SQLMap for SQL Injection
                sh 'sqlmap -u http://localhost:5000/login --data="username=admin&password=admin" --batch'

                // OWASP ZAP for XSS, Open Redirect, etc.
                sh 'zap-cli start'
                sh 'zap-cli open-url http://localhost:5000'
                sh 'zap-cli spider http://localhost:5000'
                sh 'zap-cli active-scan http://localhost:5000'
                sh 'zap-cli report -o zap_report.html -f html'
                sh 'zap-cli stop'

                // Docker image vulnerability scan
                sh 'docker scan ' + DOCKER_IMAGE
            }
        }
    }
    post {
        always {
            // Stop and remove the Docker container
            sh 'docker stop vuln-app || true'
            sh 'docker rm vuln-app || true'
        }
    }
}
