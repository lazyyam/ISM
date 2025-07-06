//JenkinsFile for ISM-SONARQUBE using scm
pipeline {
  agent any

  environment {
    PYTHONPATH = "ISM/backend"
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

    stage('Install Dependencies') {
      steps {
        bat 'pip install -r ISM/backend/requirements.txt'
        bat 'pip install pytest pytest-cov'
      }
    }

    stage('Run Tests') {
      steps {
        bat 'pytest ISM/backend/test --cov=ISM/backend/app --cov-report=xml'
      }
    }

    stage('SonarCloud Analysis') {
      steps {
        withSonarQubeEnv('SonarCloud') {
          withCredentials([string(credentialsId: 'jenkins-sonarqube', variable: 'SONAR_TOKEN')]) {
            bat """
              sonar-scanner ^
                -Dsonar.login=%SONAR_TOKEN% ^
                -Dproject.settings=ISM/sonar-project.properties
            """
          }
        }
      }
    }
  }
}