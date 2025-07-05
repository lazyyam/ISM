pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker-hub-credentials')
        DOCKER_IMAGE = "yamzhan/ism-demov1:latest"
        JIRA_SITE = 'my-jira'
        JIRA_ISSUE = 'ISM-1'
    }

    stages {
        stage('Jira - Start Progress') {
            steps {
                script {
                    jiraTransitionIssue(
                        site: env.JIRA_SITE,
                        idOrKey: env.JIRA_ISSUE,
                        input: [
                            transition: [ id: '21' ] // In Progress
                        ]
                    )
                    jiraAddComment(
                        site: env.JIRA_SITE,
                        idOrKey: env.JIRA_ISSUE,
                        comment: "✅ Jenkins build started for image `${env.DOCKER_IMAGE}`"
                    )
                }
            }
        }

        stage('Docker Login') {
            steps {
                script {
                    bat """
                        docker logout
                        docker login -u %DOCKERHUB_CREDENTIALS_USR% -p %DOCKERHUB_CREDENTIALS_PSW%
                    """
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    bat """
                        docker buildx create --use || echo Buildx instance exists
                        docker buildx build --platform linux/amd64 -t %DOCKER_IMAGE% --push .
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    withKubeConfig(
                        caCertificate: 'C:\\Users\\User\\.minikube\\ca.crt',
                        clusterName: 'kubernetes-dashboard',
                        contextName: '',
                        credentialsId: 'kubernets-jenkins',
                        namespace: 'default',
                        restrictKubeConfigAccess: false,
                        serverUrl: 'http://127.0.0.1:53255'
                    ) {
                        bat 'kubectl apply -f deployment.yaml'
                        bat 'kubectl apply -f service.yaml'
                        bat 'kubectl get deployments'
                        bat 'kubectl describe deployment ism-app'
                        bat 'kubectl get pods -o wide'
                        bat 'kubectl get services'
                    }
                }
            }
        }

        stage('Jira - Mark Done') {
            steps {
                script {
                    jiraAddComment(
                        site: env.JIRA_SITE,
                        idOrKey: env.JIRA_ISSUE,
                        comment: "✅ Deployment of `${env.DOCKER_IMAGE}` completed successfully to Kubernetes."
                    )
                    jiraTransitionIssue(
                        site: env.JIRA_SITE,
                        idOrKey: env.JIRA_ISSUE,
                        input: [
                            transition: [ id: '31' ] // Done transition
                        ]
                    )
                }
            }
        }
    }

    post {
        failure {
            script {
                jiraAddComment(
                    site: env.JIRA_SITE,
                    idOrKey: env.JIRA_ISSUE,
                    comment: "❌ Jenkins pipeline failed. Please check the build logs."
                )
            }
        }
    }
}
