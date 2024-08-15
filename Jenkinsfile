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

        stage('Run Docker Container') {
            steps {
                script {
                    // Convert the workspace path to a Unix-compatible path
                    def unixWorkspace = pwd().replaceAll('C:/', '/c/').replaceAll('\\\\', '/')

                    dockerImage.inside("--workdir ${unixWorkspace}") {
                        sh 'echo "Docker container is running and accessible."'
                    }
                }
            }
        }
    }
}
