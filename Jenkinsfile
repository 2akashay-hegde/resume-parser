pipeline {
  agent any

  environment {
    DOCKER_IMAGE = 'resume-parser'
    DOCKER_TAG = 'latest'
    DOCKER_HUB_CREDENTIALS = 'docker-hub-creds'
    LLM_API_KEY = 'llm-api-key'
  }

  stages {
    stage('Unit Test') {
      steps {
        script {
          if (isUnix()) {
            sh '''
              docker run --rm -v "$PWD":/app -w /app python:3.11-slim bash -lc \
              "python -m pip install --upgrade pip && python -m pip install -r app/requirements.txt && python -m pytest -q"
            '''
          } else {
            bat 'docker run --rm -v "%cd%":/app -w /app python:3.11-slim bash -lc "python -m pip install --upgrade pip && python -m pip install -r app/requirements.txt && python -m pytest -q"'
          }
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          if (isUnix()) {
            sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
          } else {
            bat "docker build -t %DOCKER_IMAGE%:%DOCKER_TAG% ."
          }
        }
      }
    }

    stage('Push Docker Image') {
      when {
        expression { env.BRANCH_NAME == 'main' }
      }
      steps {
        withCredentials([usernamePassword(credentialsId: env.DOCKER_HUB_CREDENTIALS, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          script {
            if (isUnix()) {
              sh 'echo $DOCKER_PASS | docker login --username $DOCKER_USER --password-stdin'
              sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_USER}/${DOCKER_IMAGE}:${DOCKER_TAG}"
              sh "docker push ${DOCKER_USER}/${DOCKER_IMAGE}:${DOCKER_TAG}"
            } else {
              bat "echo %DOCKER_PASS% | docker login --username %DOCKER_USER% --password-stdin"
              bat "docker tag %DOCKER_IMAGE%:%DOCKER_TAG% %DOCKER_USER%/%DOCKER_IMAGE%:%DOCKER_TAG%"
              bat "docker push %DOCKER_USER%/%DOCKER_IMAGE%:%DOCKER_TAG%"
            }
          }
        }
      }
    }

    stage('Validate LLM Credential') {
      steps {
        withCredentials([string(credentialsId: env.LLM_API_KEY, variable: 'OPENAI_API_KEY')]) {
          script {
            if (isUnix()) {
              sh 'echo "LLM API key is available in a secret variable"'
            } else {
              bat 'echo LLM API key is available in a secret variable'
            }
          }
        }
      }
    }
  }

  post {
    always {
      script {
        if (isUnix()) {
          sh 'docker logout || true'
        } else {
          bat 'docker logout || true'
        }
      }
    }
  }
}
