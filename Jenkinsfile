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
                // comment out for now because its not working as expected
                // Run trufflehog in Docker container
                // bat 'docker run --rm -v %cd%\\app:/app marsko/vulnerable-app:latest trufflehog https://github.com/marskop/vulnerable-app.git'
                // bat 'echo Trufflehog Exit Code: %ERRORLEVEL%'

                // Run semgrep in Docker container
                bat 'docker run --rm -v %cd%\\app:/app marsko/vulnerable-app:latest semgrep --config=p/ci /app'
                bat 'echo Semgrep Exit Code: %ERRORLEVEL%'

            // comment out for now to pass to the next step
            // Run bandit in Docker container
            // bat 'docker run --rm -v %cd%\\app:/app marsko/vulnerable-app:latest bandit -r /app'
            // bat 'echo Bandit Exit Code: %ERRORLEVEL%'
            }
        }

        // stage('Build') {
        //     steps {
        //         bat 'pip install -r requirements.txt'
        //         bat 'if not exist app.py (echo "Error: app.py not found!" & exit 1)'
        //         echo 'Build completed successfully.'
        //     }
        // }

        // stage('Dynamic Analysis') {
        //     steps {
        //         // bat 'docker run --rm -v %cd%\\app:/app zaproxy/zap2docker-stable zap-baseline.py -t https://github.com/marskop/vulnerable-app.git'
        //         bat 'docker run --rm -v %cd%\\app:/app marsko/vulnerable-app:latest sqlmap -u https://c16f-2a02-85f-9a07-c918-4df0-638e-6aac-7ed4.ngrok-free.app/login --data="username=test&password=test" --batch --random-agent'

        //          // Χρήση του ZAP Docker image για δυναμική ανάλυση
        //         // bat 'docker run --rm -v %cd%\\app:/zap/wrk/:rw -t owasp/zap2docker-stable zap-baseline.py -t https://github.com/marskop/vulnerable-app.git -r zap_report.html'
        //     }
        // }

        stage('Dynamic Analysis with SQLmap') {
            steps {
                bat 'docker run --rm -v %cd%\\app:/app marsko/vulnerable-app:latest sqlmap -u https://c16f-2a02-85f-9a07-c918-4df0-638e-6aac-7ed4.ngrok-free.app/login --data="username=test&password=test" --batch --random-agent'
            }
        }

        // stage('Dynamic Analysis with OWASP ZAP') {
        //     steps {
        //         // Χρησιμοποιήστε το OWASP ZAP για ανάλυση ευπαθειών της εφαρμογής
        //         // bat '''
        //         // docker run --rm -v %cd%\\app:/zap/wrk/:rw zaproxy/zap-stable zap-baseline.py -t https://c16f-2a02-85f-9a07-c918-4df0-638e-6aac-7ed4.ngrok-free.app/search -r zap_report.html
        //         // '''
        //         bat '''
        //         docker run --rm -v %cd%\\app:/zap/wrk/:rw zaproxy/zap-stable zap-baseline.py -t https://c16f-2a02-85f-9a07-c918-4df0-638e-6aac-7ed4.ngrok-free.app/redirect -r zap_report.html
        //         '''
        //     }
        // }

         stage('Nmap Scan') {
            steps {
                script {
                    // Ensure that Nmap is installed, or run it via Docker
                    bat '''
                    docker run --rm instrumentisto/nmap nmap -sV --script=vuln fb25-2a02-85f-9a07-c918-4df0-638e-6aac-7ed4.ngrok-free.app > nmap_report.txt
                    '''
                }
            }
        }

                stage('ZAP Active Scan') {
            steps {
                script {
                    def targetUrl = "https://fb25-2a02-85f-9a07-c918-4df0-638e-6aac-7ed4.ngrok-free.app/command" // Replace with your ngrok URL if needed
                    def zapOptions = "-t ${targetUrl} -r zap_report.html -z \"-config api.disablekey=true\""

                    // Perform the baseline scan (passive scan)
                    bat "docker run --rm -v %cd%\\app:/zap/wrk/:rw zaproxy/zap-stable zap-baseline.py ${zapOptions}"

                    // Perform the active scan
                    bat "docker run --rm -v %cd%\\app:/zap/wrk/:rw zaproxy/zap-stable zap-full-scan.py ${zapOptions}"
                }
            }
        }

        stage('Deploy') {
            steps {
                bat 'deploy.bat'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/target/*.jar', allowEmptyArchive: true
            junit 'target/test-results/*.xml'
            archiveArtifacts artifacts: 'zap_report.html', allowEmptyArchive: true
            archiveArtifacts artifacts: ' nmap_report.html', allowEmptyArchive: true
        }
    }
}
