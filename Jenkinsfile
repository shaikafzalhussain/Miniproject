pipeline {
    agent any

    environment {
        // 🔐 Jenkins credentials (configure in Jenkins > Manage Credentials)
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')  // Docker Hub username & password
        SONARQUBE = credentials('sonar-token')                  // SonarQube token
        DOCKER_IMAGE = "shaikafzalhussain/miniproject"
        CONTAINER_NAME = "miniproject-v1.2"
        SONARQUBE_SERVER = "http://13.233.85.145:9000/"    // replace with your SonarQube server
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "📦 Checking out code from GitHub..."
                git branch: 'main', url: 'https://github.com/shaikafzalhussain/Miniproject.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo "🧠 Running SonarQube analysis..."
                sh '''
                sonar-scanner \
                    -Dsonar.projectKey=miniproject-v1.2 \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=$SONARQUBE_SERVER \
                    -Dsonar.login=$SONARQUBE
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image..."
                sh 'docker build -t $DOCKER_IMAGE:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "🚀 Pushing Docker image to DockerHub..."
                sh '''
                echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                docker push $DOCKER_IMAGE:latest
                '''
            }
        }

        stage('Run Container Automatically') {
            steps {
                echo '🧩 Deploying new container...'
                sh '''
                    # Stop and remove old container if it exists
                    if [ "$(docker ps -aq -f name=miniproject-v1.2)" ]; then
                        echo "🛑 Stopping and removing old container..."
                        docker stop miniproject-v1.2 || true
                        docker rm miniproject-v1.2 || true
                    fi

                    # Run a new container on port 5000
                    echo "🚀 Starting new container..."
                    docker run -d -p 5001:5000 --name miniproject-v1.2 shaikafzalhussain/miniproject:latest

                    '''
            }
        }

        stage('Health Check') {
            steps {
                echo "🩺 Checking app health..."
                script {
                    sleep 10
                    def result = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:5000", returnStdout: true).trim()
                    if (result != '200') {
                        error "❌ Health check failed! App not responding on port 5000."
                    } else {
                        echo "✅ Application is healthy and running!"
                    }
                }
            }
        }
    }

    post {
        success {
            echo "🎉 Pipeline completed successfully! Your Flask app is live inside the container."
        }
        failure {
            echo "❌ Pipeline failed! Check logs above for the issue."
        }
        always {
            echo "🧹 Cleaning up unused Docker resources..."
            sh 'docker system prune -f || true'
        }
    }
}
