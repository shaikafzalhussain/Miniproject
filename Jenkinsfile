pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        SONARQUBE_ENV = credentials('sonar-token')
        IMAGE_NAME = "shaikafzalhussain/miniproject"
        CONTAINER_NAME = "miniproject"
        APP_PORT = "5000"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "📦 Checking out code from GitHub..."
                git branch: 'main', url: 'https://github.com/shaikafzalhussain/Miniproject.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "📦 Installing Python dependencies..."
                sh 'pip3 install -r app/requirements.txt'
            }
        }

        stage('Install NodeJS for SonarQube') {
            steps {
                echo "🧰 Installing Node.js for SonarQube analysis..."
                sh '''
                    sudo apt-get update -y
                    sudo apt-get install -y nodejs npm
                    node -v
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo "🔍 Running SonarQube analysis..."
                withSonarQubeEnv('MySonarQubeServer') {
                    sh '''
                        cd app
                        sonar-scanner \
                          -Dsonar.projectKey=MiniProject \
                          -Dsonar.sources=. \
                          -Dsonar.host.url=http://13.233.85.145:9000 \
                          -Dsonar.login=$SONARQUBE_ENV
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image..."
                sh 'docker build -t $IMAGE_NAME:latest .'
            }
        }

        stage('Push to DockerHub') {
            steps {
                echo "📤 Pushing Docker image to DockerHub..."
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push $IMAGE_NAME:latest
                    '''
                }
            }
        }

        stage('Deploy Container') {
            steps {
                echo "🚀 Deploying Docker container..."
                sh '''
                    echo "Stopping and removing old container if it exists..."
                    docker stop $CONTAINER_NAME || true
                    docker rm $CONTAINER_NAME || true

                    echo "Pulling latest image from DockerHub..."
                    docker pull $IMAGE_NAME:latest

                    echo "Running new container..."
                    docker run -d -p $APP_PORT:5000 --name $CONTAINER_NAME $IMAGE_NAME:latest
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully! Application running at http://<YOUR-EC2-IP>:$APP_PORT"
        }
        failure {
            echo "❌ Pipeline failed! Check logs above for details."
        }
    }
}
