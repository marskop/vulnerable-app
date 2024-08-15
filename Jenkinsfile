pipeline {
    agent any

    stages {
        stage('Test Docker Direct Interaction') {
            steps {
                bat 'docker run --rm alpine echo "Docker is running and accessible."'
            }
        }
    }
}
