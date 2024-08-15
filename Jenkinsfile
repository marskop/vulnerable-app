// pipeline {
//     agent any

//     environment {
//         DOCKER_IMAGE = 'vulnerable-app'
//     }

//     stages {
//         stage('Checkout') {
//             steps {
//                 checkout scm
//             }
//         }
        
//         stage('Build Docker Image') {
//             steps {
//                 script {
//                     dockerImage = docker.build(DOCKER_IMAGE)
//                 }
//             }
//         }

//         stage('Run Container') {
//             steps {
//                 script {
//                     dockerImage.run('-d -p 5000:5000 --name vuln-app')
//                 }
//             }
//         }
//         stage('Static Analysis') {
//             steps {
//                 sh 'pip install bandit'
//                 sh 'bandit -r .'
//                 sh 'pip install truffleHog'
//                 sh 'trufflehog --regex --entropy=True .'
//             }
//         }

//         stage('Dynamic Analysis') {
//             steps {
//                 // Nmap for open ports and services
//                 sh 'nmap -p 5000 localhost'

//                 // SQLMap for SQL Injection
//                 sh 'sqlmap -u http://localhost:5000/login --data="username=admin&password=admin" --batch'

//                 // OWASP ZAP for XSS, Open Redirect, etc.
//                 sh 'zap-cli start'
//                 sh 'zap-cli open-url http://localhost:5000'
//                 sh 'zap-cli spider http://localhost:5000'
//                 sh 'zap-cli active-scan http://localhost:5000'
//                 sh 'zap-cli report -o zap_report.html -f html'
//                 sh 'zap-cli stop'

//                 // Docker image vulnerability scan
//                 sh 'docker scan ' + DOCKER_IMAGE
//             }
//         }
//     }
//     post {
//         always {
//             // Stop and remove the Docker container
//             sh 'docker stop vuln-app || true'
//             sh 'docker rm vuln-app || true'
//         }
//     }
// }

// V2

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

        // stage('Run Static Analysis Inside Docker') {
        //     steps {
        //         script {
        //             // Use a Python Docker image to run static analysis tools inside a container
        //             docker.image('python:3.9').inside {
        //                 bat 'pip install bandit'
        //                 bat 'bandit -r .'
        //                 bat 'pip install truffleHog'
        //                 bat 'trufflehog --regex --entropy=True .'
        //             }
        //         }
        //     }
        // }

        stage('Run Application and Perform Dynamic Analysis') {
            steps {
                script {
                    dockerImage.inside {
                        sh 'nohup python app.py &'

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
                    }
                }
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

