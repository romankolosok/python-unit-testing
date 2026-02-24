pipeline {
    agent any

    options {
        timeout(time: 15, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        POETRY_VIRTUALENVS_IN_PROJECT = 'true'
        POETRY_VIRTUALENVS_CREATE = 'true'
        PATH = "${env.HOME}/.local/bin:${env.PATH}"
        GITHUB_TOKEN = credentials('github-token-id')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                sh '''#!/bin/bash
                    set -e
                    if ! command -v poetry &> /dev/null; then
                        curl -sSL https://install.python-poetry.org | python3 -
                    fi
                    poetry install --with dev --no-interaction
                '''
            }
        }

        stage('Test & Coverage') {
            steps {
                // Ensure --cov points to your actual package directory
                sh 'poetry run pytest tests/ -v --junitxml=junit.xml --cov=src --cov-report=xml --cov-report=html'
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'junit.xml'

                    recordCoverage(
                        tools: [[parser: 'COBERTURA', pattern: 'coverage.xml']],
                        id: 'python-coverage',
                        name: 'Python Code Coverage'
                    )

                    publishHTML target: [
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Detailed Coverage Report'
                    ]
                }
            }
        }
    }

    post {
        always {
            // Updated to the most reliable syntax to avoid "instantiation" errors
            step([$class: 'GitHubCommitStatusSetter', contextSource: [$class: 'DefaultCommitContextSource', context: 'Jenkins/Build']])

            cleanWs(deleteDirs: true, patterns: [[pattern: '.venv/**', type: 'INCLUDE']])
        }

        failure {
            echo 'Build failed. Check the GitHub interface or Jenkins logs.'
        }
    }
}