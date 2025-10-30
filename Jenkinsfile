pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')   // Jenkins credentials ID for DockerHub
        SONARQUBE_ENV = credentials('sonar-token')                // SonarQube token (optional)
        IMAGE_NAME = "shaikafzalhussain/miniproject"
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
                sh '''
                    docker build -t $IMAGE_NAME:latest .
                '''
            }
        }

        stage('Push to DockerHub') {
            steps {
                echo "📤 Pushing Docker image to DockerHub..."
                sh '''
                    echo "$DOCKERHUB_CREDENTIALS_PSW" | docker login -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin
                    docker push $IMAGE_NAME:latest
                    docker logout
                '''
            }
        }

        stage('Deploy Container') {
            steps {
                echo "🚀 Deploying Docker container..."
                sh '''
                    CONTAINER_NAME=miniproject

                    # Stop & remove existing container if running
                    docker stop $CONTAINER_NAME || true
                    docker rm $CONTAINER_NAME || true

                    # Run new container
                    docker run -d -p 5000:5000 --restart always --name $CONTAINER_NAME $IMAGE_NAME:latest
                '''
            }
        }

    }

    post {
        success {
            echo "✅ Deployment successful! Access the app at: http://<EC2-PUBLIC-IP>:5000"
        }
        failure {
            echo "❌ Pipeline failed. Check console output for details."
        }
    }
}
