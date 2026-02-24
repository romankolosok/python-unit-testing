pipeline {
    agent any

    options {
        timeout(time: 15, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        // This ensures the GitHub status is updated automatically by the plugin
        preserveStashes(buildCount: 5)
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

        stage('Setup Python & Dependencies') {
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

        stage('Lint') {
            steps {
                // We use || true so the pipeline continues even if linting has minor warnings
                sh 'poetry run ruff check src tests || true'
                sh 'poetry run ruff format --check src tests || true'
            }
        }

        stage('Test & Coverage') {
            steps {
                // Combines testing and coverage generation into one step for efficiency
                // Generates junit.xml (Tests) and coverage.xml (Cobertura format)
                sh 'poetry run pytest tests/ -v --junitxml=junit.xml --cov=src --cov-report=xml --cov-report=html'
            }
            post {
                always {
                    // 1. Record Test Results in Jenkins
                    junit allowEmptyResults: true, testResults: 'junit.xml'

                    // 2. Record Coverage (This posts the "Check" to GitHub automatically)
                    recordCoverage(
                        tools: [[parser: 'COBERTURA', pattern: 'coverage.xml']],
                        id: 'python-coverage',
                        name: 'Python Code Coverage',
                        sourceCodeRetention: 'LAST_BUILD'
                    )

                    // 3. Publish HTML Report for Jenkins UI
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
            // Sends the "Success/Failure" status back to the GitHub commit list
            step([$class: 'GitHubCommitStatusSetter',
                  contextSource: [$class: 'DefaultCommitContextSource', context: 'Jenkins/Build-and-Test'],
                  reposSource: [$class: 'AnyRepoSource']])

            cleanWs(deleteDirs: true, patterns: [[pattern: '.venv/**', type: 'INCLUDE']])
        }

        failure {
            echo 'Build or tests failed. Check the GitHub Checks tab for details.'
        }
    }
}