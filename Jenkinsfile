pipeline {
  agent any

  environment {
    PYTHONPATH = "backend"
    DATABASE_URL = "sqlite:///:memory:"
  }

  stages {
    stage('Clean Workspace') {
      steps {
        deleteDir()
      }
    }

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Debug Workspace') {
      steps {
        bat 'dir'
        bat 'dir backend'
      }
    }

    stage('Install Dependencies') {
      steps {
        bat 'pip install -r backend/requirements.txt'
        bat 'pip install pytest pytest-cov'
      }
    }

    stage('Run Tests') {
      steps {
        bat 'pytest backend/test --cov=backend/app --cov-report=xml'
      }
    }

    stage('SonarCloud Analysis') {
      steps {
        withSonarQubeEnv('SonarCloud') {
          withCredentials([string(credentialsId: 'jenkins-sonarqube', variable: 'SONAR_TOKEN')]) {
            bat """
              sonar-scanner ^
                -Dsonar.login=%SONAR_TOKEN% ^
                -Dproject.settings=sonar-project.properties
            """
          }
        }
      }
    }
  }
}
