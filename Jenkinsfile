pipeline {
    agent any
    environment {
        APP_NAME = "airline"
        RELEASE = "1.0.0"
        IMAGE_TAG = "${RELEASE}-${BUILD_NUMBER}"
        JENKINS_MASTER_DNS_URL = "ec2-13-232-237-15.ap-south-1.compute.amazonaws.com"
        CD_JOB_NAME = "FlightPricePrediction-CD"
    }
    stages {
        stage("Cleanup Workspace") {
            steps {
                cleanWs()
            }
        }

        stage("Checkout from SCM") {
            steps {
                git branch: 'main', credentialsId: 'GitHub', url: 'https://github.com/gawaliashay/FlightPricePrediction-CI'
            }
        }

        stage("Build & Push Docker Image") {
            steps {
                withCredentials([usernamePassword(credentialsId: 'DockerHub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
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

        stage("Trivy Scan") {
            steps {
                withCredentials([usernamePassword(credentialsId: 'DockerHub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        def imageName = "${DOCKER_USER}/${APP_NAME}"
                        sh '''
                            docker run -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy image ${DOCKER_USER}/${APP_NAME}:latest \
                            --no-progress --scanners vuln --exit-code 0 \
                            --severity HIGH,CRITICAL --format table
                        '''
                    }
                }
            }
        }

        stage("Cleanup Artifacts") {
            steps {
                withCredentials([usernamePassword(credentialsId: 'DockerHub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        def imageName = "${DOCKER_USER}/${APP_NAME}"
                        sh "docker rmi ${imageName}:${IMAGE_TAG} || true"
                        sh "docker rmi ${imageName}:latest || true"
                    }
                }
            }
        }

        stage("Trigger CD Pipeline") {
            steps {
                withCredentials([string(credentialsId: 'JENKINS_API_TOKEN', variable: 'JENKINS_TOKEN')]) {
                    script {
                        def triggerUrl = "http://${JENKINS_MASTER_DNS_URL}:8080/job/${CD_JOB_NAME}/buildWithParameters?token=MLOPS-TOKEN"
                        sh '''
                            curl -v -k --user admin:$JENKINS_TOKEN \
                            -X POST -H 'cache-control: no-cache' \
                            -H 'content-type: application/x-www-form-urlencoded' \
                            --data 'IMAGE_TAG=${IMAGE_TAG}' ${triggerUrl}
                        '''
                    }
                }
            }
        }
    }

    /*
    post {
        failure {
            emailext body: '''${SCRIPT, template="groovy-html.template"}''',
            subject: "${env.JOB_NAME} - Build # ${env.BUILD_NUMBER} - Failed",
            mimeType: 'text/html', to: "gawali.ashay@gmail.com"
        }
        success {
            emailext body: '''${SCRIPT, template="groovy-html.template"}''',
            subject: "${env.JOB_NAME} - Build # ${env.BUILD_NUMBER} - Successful",
            mimeType: 'text/html', to: "gawali.ashay@gmail.com"
        }
    }
    */
}
