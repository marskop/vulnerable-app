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
                // Run truffleHog to detect secrets and save the report
                sh 'trufflehog --json ./ > trufflehog-report.json'

                // Run linter for Python and save the report
                sh 'pylint **/*.py > pylint-report.txt || true'

                // Run static code analysis with Bandit and save the report
                sh 'bandit -r . -f json -o bandit-report.json'
            }
        }

        stage('Build') {
            steps {
                // Build Docker image
                sh 'docker build -t vulnerable-webapp .'
            }
        }

        stage('Dynamic Analysis') {
            steps {
                // Run nmap to check for open ports and vulnerabilities
                sh 'nmap -sV -p- 127.0.0.1 > nmap-report.txt'

                // Run SQLMap to check for SQL Injection vulnerabilities and save the report
                sh 'sqlmap -u "http://127.0.0.1:5000/login" --data="username=admin&password=adminpassword" --batch --output-dir=./sqlmap-reports'

                // Run ZAP Proxy for dynamic vulnerability scanning and save the report
                sh 'zap-cli quick-scan --self-contained http://127.0.0.1:5000 > zap-report.txt'
            }
        }

        stage('Docker Vulnerability Scan') {
            steps {
                // Scan Docker images for vulnerabilities
                sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image vulnerable-webapp > trivy-report.txt'
            }
        }
    }

    post {
        always {
            // Archive the reports as artifacts
            archiveArtifacts artifacts: '**/trufflehog-report.json', allowEmptyArchive: true
            archiveArtifacts artifacts: '**/pylint-report.txt', allowEmptyArchive: true
            archiveArtifacts artifacts: '**/bandit-report.json', allowEmptyArchive: true
            archiveArtifacts artifacts: '**/nmap-report.txt', allowEmptyArchive: true
            archiveArtifacts artifacts: '**/zap-report.txt', allowEmptyArchive: true
            archiveArtifacts artifacts: 'sqlmap-reports/**', allowEmptyArchive: true
            archiveArtifacts artifacts: '**/trivy-report.txt', allowEmptyArchive: true
        }
    }
}

// pipeline {
//     agent any

//     stages {
//         stage('Checkout') {
//             steps {
//                 checkout scm
//             }
//         }

//         stage('Static Analysis') {
//             steps {
//                 // Run truffleHog to detect secrets
//                 sh 'trufflehog --regex --entropy=True ./'

//                 // Run linter for Python
//                 sh 'pylint **/*.py'

//                 // Run static code analysis with Bandit
//                 sh 'bandit -r .'
//             }
//         }

//         stage('Build') {
//             steps {
//                 // Build Docker image
//                 sh 'docker build -t vulnerable-webapp .'
//             }
//         }

//         stage('Dynamic Analysis') {
//             steps {
//                 // Run nmap to check for open ports and vulnerabilities
//                 sh 'nmap -sV -p- 127.0.0.1'

//                 // Run SQLMap to check for SQL Injection vulnerabilities
//                 sh 'sqlmap -u "http://127.0.0.1:5000/login" --data="username=admin&password=adminpassword" --batch'

//                 // Run ZAP Proxy for dynamic vulnerability scanning
//                 sh 'zap-cli quick-scan --self-contained http://127.0.0.1:5000'
//             }
//         }

//         stage('Docker Vulnerability Scan') {
//             steps {
//                 // Scan Docker images for vulnerabilities
//                 sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image vulnerable-webapp'
//             }
//         }
//     }

//     post {
//         always {
//             // Publish results, send notifications etc.
//             archiveArtifacts artifacts: '**/reports/**', allowEmptyArchive: true
//         }
//     }
// }
