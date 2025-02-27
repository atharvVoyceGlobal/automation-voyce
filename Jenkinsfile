pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.11'
        VENV_PATH = 'venv'
        PATH = "/opt/homebrew/bin:/usr/local/bin:${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'pwd && ls -la'  // Показываем текущую директорию и её содержимое
            }
        }

        stage('Setup Environment') {
            steps {
                script {
                    // Проверяем переменные окружения
                    sh '''
                        echo "=== Checking Environment Variables ==="
                        echo "AGENT_URL: ${AGENT_URL}"
                        echo "CUSTOMER_URL: ${CUSTOMER_URL}"
                        echo "WORKSPACE: ${WORKSPACE}"
                        echo "Current directory: $(pwd)"
                        echo "Directory contents before env.py creation:"
                        ls -la
                    '''

                    // Создаем env.py с переменными окружения
                    sh '''
                        echo "=== Creating env.py ==="
                        echo "class EV:" > env.py
                        echo "    AGENT_URL = '$AGENT_URL'" >> env.py
                        echo "    CUSTOMER_URL = '$CUSTOMER_URL'" >> env.py
                        echo "    AGENT_LOGIN = '$AGENT_LOGIN'" >> env.py
                        echo "    AGENT_PASSWORD = '$AGENT_PASSWORD'" >> env.py
                        echo "    AGENT_ALT_LOGIN = '$AGENT_ALT_LOGIN'" >> env.py
                        echo "    OPERATOR_LOGIN = '$OPERATOR_LOGIN'" >> env.py
                        echo "    AGENT_ALT_PASSWORD = '$AGENT_ALT_PASSWORD'" >> env.py
                        echo "    OPERATOR_PASSWORD = '$OPERATOR_PASSWORD'" >> env.py
                        echo "    CUSTOMER_LOGIN = '$CUSTOMER_LOGIN'" >> env.py
                        
                        echo "=== Checking env.py content ==="
                        cat env.py
                        
                        echo "=== Directory contents after env.py creation ==="
                        ls -la
                    '''

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
                        
                        echo "=== Python Environment Info ==="
                        which python
                        python --version
                        pip list
                        echo "PYTHONPATH: \$PYTHONPATH"
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
                            
                            echo "=== Test Environment Setup ==="
                            echo "Current directory: $(pwd)"
                            echo "Directory contents:"
                            ls -la
                            echo "env.py contents:"
                            cat env.py
                        '''

                        sh '''
                            export PATH=/opt/homebrew/bin:/usr/local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
                            export NODE_PATH=/opt/homebrew/lib/node_modules
                            export PYTHONPATH="${WORKSPACE}:${PYTHONPATH:-}"
                            source venv/bin/activate
                            
                            echo "=== Python Test Environment ==="
                            echo "Python path: $(which python)"
                            echo "Python version: $(python --version)"
                            echo "PYTHONPATH: $PYTHONPATH"
                            echo "Working directory: $(pwd)"
                            echo "Directory contents:"
                            ls -la
                            
                            npm install -g @puppeteer/browsers
                            python -c "import sys; print('Python sys.path:', sys.path)"
                            PYTHONPATH="${WORKSPACE}" pytest sqs_kafka_listener.py -v -k test_video_call_activation --alluredir=./allure-results
                        '''
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