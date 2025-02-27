pipeline {
    agent any

    environment {
        // Используем Python 3.11
        PYTHON_VERSION = '3.11'
        // Путь к виртуальному окружению
        VENV_PATH = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                // Получаем код из репозитория
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                script {
                    // Устанавливаем необходимые пакеты
                    sh '''
                        sudo apt-get update
                        sudo apt-get install -y python3.11 python3.11-venv python3-pip xvfb ffmpeg wget unzip \
                            libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 \
                            libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 \
                            libpango-1.0-0 libcairo2 libatspi2.0-0
                    '''

                    // Создаем и активируем виртуальное окружение
                    sh """
                        python3.11 -m venv ${VENV_PATH}
                        . ${VENV_PATH}/bin/activate
                        python -m pip install --upgrade pip
                        pip install -r requirements.txt
                    """
                }
            }
        }

        stage('Setup Virtual Display') {
            steps {
                script {
                    // Запускаем виртуальный дисплей
                    sh '''
                        Xvfb :99 -screen 0 1920x1080x24 -ac +extension GLX +render -noreset &
                        export DISPLAY=:99
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    try {
                        // Создаем директории для результатов
                        sh '''
                            mkdir -p allure-results
                            mkdir -p test_results
                            mkdir -p test_videos
                        '''

                        // Запускаем тесты
                        sh """
                            . ${VENV_PATH}/bin/activate
                            export DISPLAY=:99
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
                // Генерируем отчет Allure
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'allure-results']]
                ])

                // Сохраняем видео как артефакты
                archiveArtifacts artifacts: 'test_videos/**/*', allowEmptyArchive: true
                archiveArtifacts artifacts: 'allure-results/**/*', allowEmptyArchive: true
            }

            // Очищаем рабочее пространство
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