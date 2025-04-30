pipeline {
    agent any

    environment {
        APP_NAME = "airline"
        RELEASE = "1.0.0"
        DOCKER_USER = "ashay1987"
        IMAGE_NAME = "${DOCKER_USER}/${APP_NAME}"
        IMAGE_TAG = "${RELEASE}-${BUILD_NUMBER}"

        DOCKER_CREDENTIALS = credentials('DockerHub')
        JENKINS_API_TOKEN = credentials('JENKINS_API_TOKEN')
        JENKINS_MASTER_DNS_URL = "ec2-3-111-214-208.ap-south-1.compute.amazonaws.com:8080"
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
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKER_CREDENTIALS) {
                        docker_image = docker.build("${IMAGE_NAME}")
                        docker_image.push("${IMAGE_TAG}")
                        docker_image.push("latest")
                    }
                }
            }
        }

        stage("Trivy Scan") {
            steps {
                script {
                    sh "docker run -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image ${IMAGE_NAME}:latest --no-progress --scanners vuln --exit-code 0 --severity HIGH,CRITICAL --format table"
                }
            }
        }

        stage("Cleanup Artifacts") {
            steps {
                script {
                    sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true"
                    sh "docker rmi ${IMAGE_NAME}:latest || true"
                }
            }
        }

        stage("Trigger CD Pipeline") {
            steps {
                script {
                    sh """
                        curl -v -k --user admin:${JENKINS_API_TOKEN} -X POST \
                        -H 'cache-control: no-cache' \
                        -H 'content-type: application/x-www-form-urlencoded' \
                        --data 'IMAGE_TAG=${IMAGE_TAG}' \
                        '${JENKINS_MASTER_DNS_URL}/job/${CD_JOB_NAME}/buildWithParameters?token=MLOPS-TOKEN'
                    """
                }
            }
        }

        /*
        stage("Email Notifications") {
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
        }
        */
    }
}
