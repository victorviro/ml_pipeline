library('slack-notifier@master')

pipeline {
  agent any
  options {
    ansiColor('xterm')
  }
  stages {
    stage('🏗️ Prepare environment') {
      steps {
        sh "python3.8 -m virtualenv venv"
      }
    }
    stage('Install dependencies') {
      steps {
        sh "$PYTHON_ENV_CMD && python3.8 -m pip install --upgrade pip"
        sh "$PYTHON_ENV_CMD && make install-test"
      }
    }
    stage('✅ Run tests') {
      steps {
        sh "$PYTHON_ENV_CMD &&  make test"
      }
    }
    stage('🕵️ Collect test reports') {
      steps {
        junit(testResults: 'output/tests/tests.xml')
        cobertura(coberturaReportFile: 'output/coverage/coverage.xml')
      }
    }
  }
  post {
    failure {
      notifyFailedBuild()
    }
    fixed {
      notifyFixedBuild()
    }
    cleanup {
      cleanWs()
    }
  }
}
