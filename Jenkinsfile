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
                        try {
                            def imageName = "${DOCKER_USER}/${APP_NAME}"
                            echo "Building Docker image: ${imageName}"
                            def dockerImage = docker.build(imageName)
                            
                            echo "Pushing image with tag: ${IMAGE_TAG}"
                            docker.withRegistry('', 'DockerHub') {
                                dockerImage.push("${IMAGE_TAG}")
                                dockerImage.push("latest")
                            }
                        } catch (Exception e) {
                            echo "Docker operation failed: ${e.getMessage()}"
                            currentBuild.result = 'FAILURE'
                            error("Docker build/push failed")
                        }
                    }
                }
            }
        }

        stage("Trivy Security Scan") {
            steps {
                script {
                    try {
                        withCredentials([usernamePassword(
                            credentialsId: 'DockerHub', 
                            usernameVariable: 'DOCKER_USER', 
                            passwordVariable: 'DOCKER_PASS'
                        )]) {
                            def imageName = "${DOCKER_USER}/${APP_NAME}"
                            echo "Scanning image for vulnerabilities: ${imageName}:latest"
                            
                            // Run Trivy scan but don't fail the pipeline
                            def scanResult = sh(
                                script: """
                                    docker run -v /var/run/docker.sock:/var/run/docker.sock \
                                    aquasec/trivy image ${imageName}:latest \
                                    --no-progress --scanners vuln \
                                    --severity HIGH,CRITICAL --format table
                                """,
                                returnStatus: true
                            )
                            
                            if (scanResult != 0) {
                                echo "WARNING: Vulnerabilities found in the image"
                                currentBuild.result = 'UNSTABLE'
                            }
                        }
                    } catch (Exception e) {
                        echo "Trivy scan failed: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }

        stage("Cleanup Docker Artifacts") {
            when {
                expression { currentBuild.result != 'FAILURE' }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'DockerHub', 
                    usernameVariable: 'DOCKER_USER', 
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    script {
                        def imageName = "${DOCKER_USER}/${APP_NAME}"
                        echo "Cleaning up Docker artifacts"
                        sh """
                            docker rmi ${imageName}:${IMAGE_TAG} || echo "Failed to remove ${IMAGE_TAG}"
                            docker rmi ${imageName}:latest || echo "Failed to remove latest"
                            docker system prune -f || echo "Docker prune failed"
                        """
                    }
                }
            }
        }
/*
        stage("Trigger CD Pipeline") {
    steps {
        withCredentials([string(credentialsId: 'JENKINS_API_TOKEN', variable: 'JENKINS_API_TOKEN')]) {
            script {
                echo "Attempting to trigger CD pipeline with IMAGE_TAG=${IMAGE_TAG}"
                
                // Secure way to handle the curl command with credentials
                def response = sh(
                    script: """
                        curl -sS -k -w '%{http_code}' \
                        --user admin:${JENKINS_API_TOKEN} \
                        -X POST \
                        -H 'cache-control: no-cache' \
                        -H 'content-type: application/x-www-form-urlencoded' \
                        --data 'IMAGE_TAG=${IMAGE_TAG}' \
                        '${JENKINS_MASTER_URL}/job/${CD_JOB_NAME}/buildWithParameters?token=MLOPS-TOKEN' \
                        -o /dev/null
                    """,
                    returnStdout: true
                ).trim()
                
                // Check the HTTP status code
                if (response != "201" && response != "200") {
                    error("Failed to trigger CD pipeline - HTTP status ${response}")
                } else {
                    echo "Successfully triggered CD pipeline (HTTP ${response})"
                }
            }
        }
    }
}
    post {
        always {
            cleanWs()
            script {
                def subject = "${env.JOB_NAME} - Build #${env.BUILD_NUMBER} - ${currentBuild.result}"
                emailext(
                    subject: subject,
                    body: """<p>Build Status: ${currentBuild.result}</p>
                            <p>Check console output at <a href="${env.BUILD_URL}">${env.JOB_NAME} #${env.BUILD_NUMBER}</a></p>""",
                    mimeType: 'text/html',
                    to: env.EMAIL_RECIPIENT
                )
            }
        }
    }*/
}
}
