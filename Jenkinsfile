// pipeline {
//     agent any

//     stages {
//         stage('Checkout') {
//             steps {
//                 checkout scm
//             }
//         }

//         stage('TruffleHog') {
//             steps {
//                 // Run TruffleHog in Docker container
//                 bat '''
//                 docker run --rm -v %cd%\\app:/app trufflesecurity/trufflehog git https://github.com/marskop/vulnerable-app.git
//                 '''
//                 bat 'echo TruffleHog Exit Code: %ERRORLEVEL%'
//             }
//         }

//         // stage('TruffleHog Scan Filesystem') {
//         //     steps {
//         //             bat '''
//         //     docker run --rm -v %cd%\\app:/app trufflesecurity/trufflehog filesystem /app
//         //     '''

//         //          bat '''
//         //     docker run --rm -v %cd%\\app:/app trufflesecurity/trufflehog filesystem /app/app.py
//         //     '''
//         //     }
//         // }

//         stage('Static Analysis') {
//             steps {
//                 // Run semgrep in Docker container
//                 bat 'docker run --rm -v %cd%\\app:/app marsko/vulnerable-app:latest semgrep --config=p/ci /app'
//                 bat 'echo Semgrep Exit Code: %ERRORLEVEL%'

//             // comment out for now to pass to the next step
//             // Run bandit in Docker container
//             bat 'docker run --rm -v %cd%\\app:/app marsko/vulnerable-app:latest bandit -r /app'
//             bat 'echo Bandit Exit Code: %ERRORLEVEL%'
//             }
//         }

//         // stage('Build') {
//         //     steps {
//         //         bat 'pip install -r requirements.txt'
//         //         bat 'if not exist app.py (echo "Error: app.py not found!" & exit 1)'
//         //         echo 'Build completed successfully.'
//         //     }
//         // }


//         stage('Dynamic Analysis with SQLmap') {
//             steps {
//                 bat 'docker run --rm -v %cd%\\app:/app marsko/vulnerable-app:latest sqlmap -u https://c16f-2a02-85f-9a07-c918-4df0-638e-6aac-7ed4.ngrok-free.app/login --data="username=test&password=test" --batch --random-agent'
//             }
//         }

//             stage('Nmap Scan') {
//             steps {
//                     // Run Nmap in Docker and save the results to a file
//                     bat '''
//                     docker run --rm instrumentisto/nmap nmap -sV --script=vuln fb25-2a02-85f-9a07-c918-4df0-638e-6aac-7ed4.ngrok-free.app   '''
//             }
//             }

//             stage('ZAP Active Scan') {
//             steps {
//                 script {
//                     def targetUrl = 'https://fb25-2a02-85f-9a07-c918-4df0-638e-6aac-7ed4.ngrok-free.app/command' // Replace with your ngrok URL if needed
//                     def zapOptions = "-t ${targetUrl} -r zap_report.html -z \"-config api.disablekey=true\""

//                     // Perform the baseline scan (passive scan)
//                     bat "docker run --rm -v %cd%\\app:/zap/wrk/:rw zaproxy/zap-stable zap-baseline.py ${zapOptions}"

//                     // Perform the active scan
//                     bat "docker run --rm -v %cd%\\app:/zap/wrk/:rw zaproxy/zap-stable zap-full-scan.py ${zapOptions}"
//                 }
//             }
//             }

//         stage('Deploy') {
//             steps {
//                 bat 'deploy.bat'
//             }
//         }
//     }

//     post {
//         always {
//             archiveArtifacts artifacts: '**/target/*.jar', allowEmptyArchive: true
//             junit 'target/test-results/*.xml'
//             archiveArtifacts artifacts: 'zap_report.html', allowEmptyArchive: true
//         }
//     }
// }
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Αρχική λήψη του κώδικα από το αποθετήριο
                checkout scm
            }
        }

        stage('Security Scanning') {
            parallel {
                stage('TruffleHog Git Scan') {
                    steps {
                        // Εκτέλεση TruffleHog για σάρωση του αποθετηρίου Git
                        bat '''
                        docker run --rm -v %cd%\\app:/app trufflesecurity/trufflehog git https://github.com/marskop/vulnerable-app.git
                        '''
                        bat 'echo TruffleHog Exit Code: %ERRORLEVEL%'
                    }
                }

                stage('Static Analysis') {
                    steps {
                        // Εκτέλεση Semgrep για στατική ανάλυση του κώδικα
                        bat 'docker run --rm -v %cd%\\app:/app marsko/vulnerable-app:latest semgrep --config=p/ci /app'
                        bat 'echo Semgrep Exit Code: %ERRORLEVEL%'

                        // Εκτέλεση Bandit για στατική ανάλυση του κώδικα Python
                        // bat 'docker run --rm -v %cd%\\app:/app marsko/vulnerable-app:latest bandit -r /app'
                        // bat 'echo Bandit Exit Code: %ERRORLEVEL%'
                    }
                }
            }
        }

        stage('Dynamic Analysis') {
            parallel {
                stage('SQLmap Scan') {
                    steps {
                        // Εκτέλεση SQLmap για δυναμική ανάλυση SQL Injection
                        bat 'docker run --rm -v %cd%\\app:/app marsko/vulnerable-app:latest sqlmap -u https://c16f-2a02-85f-9a07-c918-4df0-638e-6aac-7ed4.ngrok-free.app/login --data="username=test&password=test" --batch --random-agent'
                    }
                }

                stage('Nmap Vulnerability Scan') {
                    steps {
                        // Εκτέλεση Nmap για σάρωση ευπαθειών δικτύου
                        bat '''
                        docker run --rm instrumentisto/nmap nmap -sV --script=vuln fb25-2a02-85f-9a07-c918-4df0-638e-6aac-7ed4.ngrok-free.app
                        '''
                    }
                }

                stage('ZAP Active Scan') {
                    steps {
                        script {
                            // Εκτέλεση OWASP ZAP για δυναμική ανάλυση (παθητική και ενεργή σάρωση)
                            def targetUrl = 'https://fb25-2a02-85f-9a07-c918-4df0-638e-6aac-7ed4.ngrok-free.app'
                            def zapOptions = "-t ${targetUrl} -r zap_report.html -z \"-config api.disablekey=true\""

                            // Παθητική σάρωση με ZAP
                            bat "docker run --rm -v %cd%\\app:/zap/wrk/:rw zaproxy/zap-stable zap-baseline.py ${zapOptions}"

                            // Ενεργή σάρωση με ZAP
                            bat "docker run --rm -v %cd%\\app:/zap/wrk/:rw zaproxy/zap-stable zap-full-scan.py ${zapOptions}"
                        }
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                // Εκτέλεση του script για την ανάπτυξη της εφαρμογής
                bat 'deploy.bat'
            }
        }
    }

    post {
        always {
            // Αρχειοθέτηση των αποτελεσμάτων της ανάλυσης και των εκθέσεων
            archiveArtifacts artifacts: '**/target/*.jar', allowEmptyArchive: true
            junit 'target/test-results/*.xml'
            archiveArtifacts artifacts: 'zap_report.html', allowEmptyArchive: true
        }
    }
}
