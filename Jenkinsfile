pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.11'
        DISPLAY = ':0'
        HOME = "${env.WORKSPACE}"
        CHROME_VERSION = '122.0.6261.69'  // Последняя стабильная версия Chrome
        WORKSPACE_DIR = "${env.WORKSPACE}"
    }
    
    stages {
        stage('Проверка файлов') {
            steps {
                echo "Проверка наличия необходимых файлов..."
                sh 'ls -la'
            }
        }
        
        stage('Подготовка окружения') {
            steps {
                script {
                    // Создаем директорию для Chrome и ChromeDriver
                    sh '''
                        mkdir -p chrome_installation
                        cd chrome_installation
                        
                        # Скачиваем Chrome для Mac ARM
                        echo "Downloading Chrome..."
                        curl -o chrome.dmg https://dl.google.com/chrome/mac/universal/stable/GGRO/googlechrome.dmg
                        
                        # Монтируем DMG и копируем приложение
                        hdiutil attach chrome.dmg
                        cp -R "/Volumes/Google Chrome/Google Chrome.app" .
                        hdiutil detach "/Volumes/Google Chrome"
                        
                        # Скачиваем ChromeDriver
                        echo "Downloading ChromeDriver..."
                        curl -LO "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/mac-arm64/chromedriver-mac-arm64.zip"
                        unzip chromedriver-mac-arm64.zip
                        
                        # Создаем файл с путями
                        echo "CHROME_PATH=${WORKSPACE_DIR}/chrome_installation/Google Chrome.app/Contents/MacOS/Google Chrome" > ../chrome_paths.txt
                        echo "CHROMEDRIVER_PATH=${WORKSPACE_DIR}/chrome_installation/chromedriver-mac-arm64/chromedriver" >> ../chrome_paths.txt
                        
                        # Делаем ChromeDriver исполняемым
                        chmod +x "chromedriver-mac-arm64/chromedriver"
                    '''
                }
            }
        }
        
        stage('Скачивание тестового видео') {
            steps {
                echo "Скачивание тестового видео..."
                sh '''
                    mkdir -p test_files
                    cd test_files
                    curl -L -o test_video.mp4 "https://www.dropbox.com/scl/fi/2unbqg3cpqd1yvpom76ir/test_video.mp4?rlkey=v8c9round5f4xtb5aqwcq5qqv7&dl=1"
                '''
            }
        }
        
        stage('Запуск тестов') {
            steps {
                echo "Запуск тестов..."
                sh '''
                    python3 -m pip install -r requirements.txt
                    python3 -m pytest test_sqs_kafka_listener.py -v
                '''
            }
        }
    }
    
    post {
        always {
            echo "Очистка..."
            cleanWs()
            
            // Сохраняем результаты тестов и видео
            archiveArtifacts artifacts: 'test_videos/**, allure-results/**, test_results/**', allowEmptyArchive: true
            
            // Генерируем отчет Allure
            allure([
                includeProperties: false,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'allure-results']]
            ])
        }
    }
} 