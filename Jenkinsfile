pipeline {
    agent any

    parameters {
        string(name: 'AGENT_URL', defaultValue: '', description: 'Agent URL')
        string(name: 'CUSTOMER_URL', defaultValue: '', description: 'Customer URL')
        string(name: 'AGENT_LOGIN', defaultValue: '', description: 'Agent Login')
        string(name: 'AGENT_PASSWORD', defaultValue: '', description: 'Agent Password')
        string(name: 'AGENT_ALT_LOGIN', defaultValue: '', description: 'Alternative Agent Login')
        string(name: 'OPERATOR_LOGIN', defaultValue: '', description: 'Operator Login')
        string(name: 'AGENT_ALT_PASSWORD', defaultValue: '', description: 'Alternative Agent Password')
        string(name: 'OPERATOR_PASSWORD', defaultValue: '', description: 'Operator Password')
        string(name: 'CUSTOMER_LOGIN', defaultValue: '', description: 'Customer Login')
    }

    environment {
        PYTHON_VERSION = '3.11'
        VENV_PATH = 'venv'
        PATH = "/opt/homebrew/bin:/usr/local/bin:${env.PATH}"
        HOME = "${env.HOME}"
        AGENT_URL = "${params.AGENT_URL}"
        CUSTOMER_URL = "${params.CUSTOMER_URL}"
        AGENT_LOGIN = "${params.AGENT_LOGIN}"
        AGENT_PASSWORD = "${params.AGENT_PASSWORD}"
        AGENT_ALT_LOGIN = "${params.AGENT_ALT_LOGIN}"
        OPERATOR_LOGIN = "${params.OPERATOR_LOGIN}"
        AGENT_ALT_PASSWORD = "${params.AGENT_ALT_PASSWORD}"
        OPERATOR_PASSWORD = "${params.OPERATOR_PASSWORD}"
        CUSTOMER_LOGIN = "${params.CUSTOMER_LOGIN}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                script {
                    sh '''
                        if [ ! -f "/opt/homebrew/bin/brew" ] && [ ! -f "/usr/local/bin/brew" ]; then
                            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
                        fi
                        
                        eval "$(/opt/homebrew/bin/brew shellenv 2>/dev/null || /usr/local/bin/brew shellenv)"
                        
                        brew list node || brew install node
                        
                        echo "Node.js version: $(node --version)"
                        echo "npm version: $(npm --version)"
                        echo "npx version: $(npx --version)"
                        
                        brew list python@3.11 || brew install python@3.11
                        brew list ffmpeg || brew install ffmpeg
                        brew list wget || brew install wget
                        
                        python3.11 --version || brew link --force python@3.11
                    '''

                    sh """
                        export PATH="/opt/homebrew/bin:/usr/local/bin:\${PATH}"
                        python3.11 -m venv ${VENV_PATH}
                        source ${VENV_PATH}/bin/activate
                        python -m pip install --upgrade pip
                        pip install -r requirements.txt
                    """
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    try {
                        sh '''
                            mkdir -p allure-results
                            mkdir -p test_results
                            mkdir -p test_videos
                        '''

                        sh """
                            export PATH="/opt/homebrew/bin:/usr/local/bin:\${PATH}"
                            export NODE_PATH="/opt/homebrew/lib/node_modules"
                            source ${VENV_PATH}/bin/activate
                            
                            npm install -g @puppeteer/browsers
                            
                            pytest sqs_kafka_listener.py -v -k test_video_call_activation --alluredir=./allure-results
                        """
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error("Test execution failed: ${e.message}")
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'allure-results']]
                ])

                archiveArtifacts artifacts: 'test_videos/**/*', allowEmptyArchive: true
                archiveArtifacts artifacts: 'allure-results/**/*', allowEmptyArchive: true
            }

            cleanWs()
        }
        success {
            echo 'Tests completed successfully!'
        }
        failure {
            echo 'Tests failed!'
        }
    }
} 