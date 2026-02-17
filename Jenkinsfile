pipeline {
    agent any

    options {
        timeout(time: 15, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        // Ensure Poetry uses the project venv in workspace
        POETRY_VIRTUALENVS_IN_PROJECT = 'true'
        POETRY_VIRTUALENVS_CREATE = 'true'
        // Poetry installs to ~/.local/bin - add to PATH for all stages
        PATH = "${env.HOME}/.local/bin:${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python & Dependencies') {
            steps {
                sh '''#!/bin/bash
                    set -e
                    # Use system Python or ensure Python 3.13 is available
                    # Fedora 42: Python 3.13+ should be available as python3
                    python3 --version

                    # Install Poetry if not present
                    if ! command -v poetry &> /dev/null; then
                        curl -sSL https://install.python-poetry.org | python3 -
                        export PATH="$HOME/.local/bin:$PATH"
                    fi

                    # Install project dependencies (including dev)
                    poetry install --with dev --no-interaction
                '''
            }
        }

        stage('Lint') {
            steps {
                sh 'poetry run ruff check src tests || true'
                sh 'poetry run ruff format --check src tests || true'
            }
        }

        stage('Test') {
            steps {
                sh 'poetry run pytest tests/ -v --tb=short -rfE --junitxml=junit.xml'
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'junit.xml'
                }
            }
        }

        stage('Coverage') {
            steps {
                sh 'poetry run pytest tests/ -v --cov=python_unit_testing --cov-report=xml --cov-report=html --cov-fail-under=0'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'htmlcov/**,coverage.xml', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        always {
            cleanWs(deleteDirs: true, patterns: [[pattern: '.venv/**', type: 'INCLUDE']])
        }
        failure {
            echo 'Build or tests failed. Check logs for details.'
        }
        success {
            echo 'Build and tests passed successfully.'
        }
    }
}
