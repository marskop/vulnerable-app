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

        stage('Test Docker Inside Block') {
            steps {
                script {
                    dockerImage.inside {
                        sh 'echo "This is running inside the Docker container."'
                    }
                }
            }
        }
    }
}
