pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.11'
        DISPLAY = ':0'
    }
    
    stages {
        stage('Проверка файлов') {
            steps {
                sh '''
                    echo "Текущая директория:"
                    pwd
                    echo "Содержимое директории:"
                    ls -la
                    
                    # Создаем requirements.txt если его нет
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
        
        stage('Подготовка окружения') {
            steps {
                sh '''
                    # Проверяем наличие Homebrew
                    if ! command -v brew &> /dev/null; then
                        echo "Установка Homebrew..."
                        CI=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
                        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
                        eval "$(/opt/homebrew/bin/brew shellenv)"
                    fi
                    
                    # Добавляем Homebrew в PATH
                    export PATH="/opt/homebrew/bin:$PATH"
                    
                    # Установка Node.js если его нет
                    if ! command -v node &> /dev/null; then
                        echo "Установка Node.js..."
                        sudo brew install node
                    fi
                    
                    # Проверяем установку Node.js и npm
                    node --version
                    npm --version
                    
                    # Установка Python и создание виртуального окружения
                    python3 -m venv venv
                    . venv/bin/activate
                    
                    # Установка Python зависимостей
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Скачивание тестового видео') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -c "
import requests, os
video_url = 'https://drive.usercontent.google.com/u/0/uc?id=1Rv3Qitap2wANEx0I-7NLvSp1cEQlE6_K&export=download'
video_path = os.path.join(os.getcwd(), 'output.y4m')
if not os.path.exists(video_path):
    print('Downloading video...')
    response = requests.get(video_url, stream=True)
    response.raise_for_status()
    with open(video_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print('Video downloaded successfully')
else:
    print('Video file already exists')"
                '''
            }
        }
        
        stage('Запуск тестов') {
            steps {
                sh '''
                    . venv/bin/activate
                    
                    # Создаем директории для результатов
                    mkdir -p allure-results test_results test_videos
                    
                    # Запускаем тесты в headless режиме
                    pytest sqs_kafka_listener.py -v -k test_video_call_activation --alluredir=./allure-results
                '''
            }
        }
    }
    
    post {
        always {
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