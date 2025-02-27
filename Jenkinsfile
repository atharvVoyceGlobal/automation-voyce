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
                    // Устанавливаем зависимости через brew
                    sh '''
                        # Проверяем и обновляем brew
                        brew update || true
                        
                        # Устанавливаем Python и другие зависимости
                        brew list python@3.11 || brew install python@3.11
                        brew list ffmpeg || brew install ffmpeg
                        brew list wget || brew install wget
                        
                        # Проверяем установку Python
                        python3.11 --version || brew link --force python@3.11
                    '''

                    // Создаем и активируем виртуальное окружение
                    sh """
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
                        // Создаем директории для результатов
                        sh '''
                            mkdir -p allure-results
                            mkdir -p test_results
                            mkdir -p test_videos
                        '''

                        // Запускаем тесты
                        sh """
                            source ${VENV_PATH}/bin/activate
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