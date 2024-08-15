pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
    }

    stage('Static Analysis') {
            steps {
                sh '''
                    # Εγκατάσταση εργαλείων
                    pip install bandit semgrep

                    # Εκτέλεση Bandit για έλεγχο Python code
                    bandit -r .

                    # Εκτέλεση Semgrep για στατικούς ελέγχους
                    semgrep --config p/ci .
                '''
            }
    }

    stage('Build') {
            steps {
                sh 'docker build -t vulnerable-app .'
            }
    }

    stage('Dynamic Analysis') {
            steps {
                script {
                    def dockerImage = docker.image('your-app')
                    dockerImage.run('-d -p 5000:5000')
                    sleep(10) // Δώστε λίγο χρόνο για την εκκίνηση της εφαρμογής

                    // Έλεγχος με Nmap για ευπάθειες
                    sh 'nmap -p- --script vuln localhost'

                    // Έλεγχος με SQLMap για SQL injection
                    sh 'sqlmap -u "http://localhost:5000/login" --data="username=test&password=test" --batch'
                }
            }
    }

    stage('Cleanup') {
            steps {
                sh 'docker stop $(docker ps -q --filter "ancestor=your-app")'
                sh 'docker rm $(docker ps -aq --filter "ancestor=your-app")'
            }
    }


    post {
        always {
            archiveArtifacts artifacts: '**/reports/*.xml', allowEmptyArchive: true
            junit 'reports/**/*.xml'
        }
        failure {
            mail to: 'your-email@example.com',
                 subject: "Build failed in Jenkins: ${currentBuild.fullDisplayName}",
                 body: "Build ${env.BUILD_NUMBER} failed. Please check the Jenkins logs."
        }
    }
}
