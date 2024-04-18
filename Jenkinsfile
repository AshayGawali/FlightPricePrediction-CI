pipeline {
    agent any
    environment {
        APP_NAME = "flight-Pred"
        RELEASE = "1.0.0"
        DOCKER_USER = "ashay1987"
        DOCKER_PASS = "DockerHub"
        IMAGE_NAME = "${DOCKER_USER}/${APP_NAME}"
        IMAGE_TAG = "${RELEASE}-${BUILD_NUMBER}"
        JENKINS_API_TOKEN = credentials("JENKINS_API_TOKEN")
        JENKINS_MASTER_DNS_URL = "ec2-3-111-30-182.ap-south-1.compute.amazonaws.com"
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
                    docker.withRegistry('', DOCKER_PASS) {
                        docker_image = docker.build "${IMAGE_NAME}"
                    }
                    docker.withRegistry('', DOCKER_PASS) {
                        docker_image.push("${IMAGE_TAG}")
                        docker_image.push("latest")
                    }
                }
            }
        }/*
        stage("Trivy Scan") {
            steps {
                script {
                    sh ('docker run -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image ashay1987/flight:latest --no-progress --scanners vuln  --exit-code 0 --severity HIGH,CRITICAL --format table')
                }
            }
        }*/
        stage ('Cleanup Artifacts') {
            steps {
                script {
                    sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker rmi ${IMAGE_NAME}:latest"
                }
            }
        }
        stage("Trigger CD Pipeline") {
            steps {
                script {
                    sh "curl -v -k --user admin:${JENKINS_API_TOKEN} -X POST -H 'cache-control: no-cache' -H 'content-type: application/x-www-form-urlencoded' --data 'IMAGE_TAG=${IMAGE_TAG}' '${JENKINS_MASTER_DNS_URL}:8080/job/${CD_JOB_NAME}/buildWithParameters?token=mlops-token'"
                    /*curl --user "username:<JENKINS_API_TOKEN>" -X POST -H "Content-Type: application/x-www-form-urlencoded" --data "parameter_name=parameter_value" "<jenkinsMaster_url>/job/<job_name>/buildWithParameters?token=<your_api_token>&<parameter_name>=<parameter_value>" */
                }
            }
        }
    }/*
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
    }*/
}
