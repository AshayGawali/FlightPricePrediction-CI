pipeline {
    agent any
    environment {
        APP_NAME = "airline"
        RELEASE = "1.0.0"
        IMAGE_TAG = "${RELEASE}-${BUILD_NUMBER}"
        JENKINS_MASTER_URL = "http://ec2-13-232-237-15.ap-south-1.compute.amazonaws.com:8080"
        CD_JOB_NAME = "FlightPricePrediction-CD"
        EMAIL_RECIPIENT = "gawali.ashay@gmail.com"
    }
    
    stages {
        stage("Cleanup Workspace") {
            steps {
                cleanWs()
            }
        }

        stage("Checkout from SCM") {
            steps {
                git branch: 'main', 
                credentialsId: 'GitHub', 
                url: 'https://github.com/gawaliashay/FlightPricePrediction-CI'
            }
        }

        stage("Build & Push Docker Image") {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'DockerHub', 
                    usernameVariable: 'DOCKER_USER', 
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    script {
                        def imageName = "${DOCKER_USER}/${APP_NAME}"
                        def dockerImage = docker.build(imageName)
                        docker.withRegistry('', 'DockerHub') {
                            dockerImage.push("${IMAGE_TAG}")
                            dockerImage.push("latest")
                        }
                    }
                }
            }
        }

        stage("Trivy Security Scan") {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'DockerHub', 
                    usernameVariable: 'DOCKER_USER', 
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    script {
                        def imageName = "${DOCKER_USER}/${APP_NAME}"
                        sh """
                            docker run -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy image ${imageName}:latest \
                            --no-progress --scanners vuln --exit-code 1 \
                            --severity CRITICAL --format table
                        """
                    }
                }
            }
        }

        stage("Cleanup Docker Artifacts") {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'DockerHub', 
                    usernameVariable: 'DOCKER_USER', 
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    script {
                        def imageName = "${DOCKER_USER}/${APP_NAME}"
                        sh """
                            docker rmi ${imageName}:${IMAGE_TAG} || true
                            docker rmi ${imageName}:latest || true
                            docker system prune -f || true
                        """
                    }
                }
            }
        }

        stage("Trigger CD Pipeline") {
            steps {
                build job: env.CD_JOB_NAME, 
                      parameters: [string(name: 'IMAGE_TAG', value: env.IMAGE_TAG)],
                      wait: false,
                      propagate: false
            }
        }
    }

        post {
        always {
            cleanWs()
        }
        success {
            script {
                echo "Pipeline completed successfully!"
            }
        }
        failure {
            script {
                echo "Pipeline failed - please check logs for details"
            }
        }
    }
}
    /*
    post {
        always {
            cleanWs()
        }
        success {
            emailext body: '''${SCRIPT, template="groovy-html.template"}''',
            subject: "${env.JOB_NAME} - Build # ${env.BUILD_NUMBER} - Successful",
            mimeType: 'text/html', 
            to: "${env.EMAIL_RECIPIENT}"
        }
        failure {
            emailext body: '''${SCRIPT, template="groovy-html.template"}''',
            subject: "${env.JOB_NAME} - Build # ${env.BUILD_NUMBER} - Failed",
            mimeType: 'text/html', 
            to: "${env.EMAIL_RECIPIENT}"
        }
    }
    */
}
