pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.11'
        DISPLAY = ':0'
        HOME = "${env.WORKSPACE}"
        CHROME_VERSION = '122.0.6261.69'
        WORKSPACE_DIR = "${env.WORKSPACE}"
        PATH = "${env.WORKSPACE}/Library/Python/3.9/bin:${env.PATH}"
        PYTHONPATH = "${env.WORKSPACE}"
    }
    
    stages {
        stage('Проверка файлов') {
            steps {
                echo "Проверка наличия необходимых файлов..."
                sh '''
                    ls -la
                    echo "Python path: $PYTHONPATH"
                    echo "PATH: $PATH"
                    echo "Текущая директория:"
                    pwd
                '''
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
                        
                        cd ..
                        
                        # Проверяем наличие requirements.txt
                        if [ ! -f requirements.txt ]; then
                            echo "Создаем requirements.txt"
                            cat > requirements.txt << EOL
selenium==4.18.1
pytest==8.0.0
pytest-html==4.1.1
allure-pytest==2.13.2
requests==2.31.0
allure-python-commons==2.13.2
pytest-xdist==3.5.0
pytest-timeout==2.2.0
pytest-rerunfailures==13.0
opencv-python==4.9.0.80
pillow==10.2.0
psutil==5.9.8
webdriver-manager==4.0.1
pytest-selenium==4.1.0
EOL
                        fi
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
                    # Обновляем pip
                    python3 -m pip install --upgrade pip
                    
                    # Устанавливаем зависимости
                    python3 -m pip install -r requirements.txt
                    
                    # Проверяем наличие файла с тестами
                    ls -la sqs_kafka_listener.py
                    
                    # Запускаем тесты
                    python3 -m pytest sqs_kafka_listener.py -v -k test_video_call_activation --alluredir=./allure-results
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