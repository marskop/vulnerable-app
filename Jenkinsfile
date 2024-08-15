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
                script {
                    dockerImage = docker.build(DOCKER_IMAGE)
                }
            }
        }

        stage('Run Static Analysis') {
            steps {
                script {
                    // Convert Windows path to Unix path for Docker
                    def unixWorkspace = pwd().replace('C:', '/c').replaceAll('\\\\', '/')

                    dockerImage.inside("--workdir ${unixWorkspace}") {
                        sh 'pip install bandit'
                        sh 'bandit -r .'
                    }
                }
            }
        }

        stage('Run Application and Dynamic Analysis') {
            steps {
                script {
                    // Convert Windows path to Unix path for Docker
                    def unixWorkspace = pwd().replace('C:', '/c').replaceAll('\\\\', '/')

                    dockerImage.inside("--workdir ${unixWorkspace}") {
                        sh 'nohup python app.py &'
                        sh 'nmap -p 5000 localhost'
                        sh 'sqlmap -u http://localhost:5000/login --data="username=admin&password=admin" --batch'
                    }
                }
            }
        }
    }
    post {
        always {
            // Clean up
            sh 'docker stop vuln-app || true'
            sh 'docker rm vuln-app || true'
        }
    }
}
