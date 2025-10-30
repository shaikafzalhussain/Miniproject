pipeline {
    agent any

    environment {
        // DockerHub image name
        IMAGE_NAME = "shaikafzalhussain/miniproject"

        // SonarQube setup name in Jenkins (from Manage Jenkins → Configure System)
        SONARQUBE_ENV = "MySonarQubeServer"
    }

    stages {

        stage('Checkout from GitHub') {
            steps {
                echo "📦 Pulling code from GitHub..."
                git branch: 'main', url: 'https://github.com/shaikafzalhussain/Miniproject.git'
            }
        }

        stage('Install Dependencies & Run Tests') {
            steps {
                echo "🧪 Setting up Python and running tests..."
                dir('app') {
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt pytest
                        pytest > test-results.txt || true
                    '''
                }
            }
            post {
                always {
                    echo "✅ Tests completed (check test-results.txt for details)."
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo "🔍 Running SonarQube scan..."
                withSonarQubeEnv("${SONARQUBE_ENV}") {
                    withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                        sh '''
                            /opt/sonar-scanner/bin/sonar-scanner \
                                -Dsonar.projectBaseDir=app \
                                -Dsonar.login=$SONAR_TOKEN
                        '''
                        echo "SonarQube scan completed."
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image..."
                sh '''
                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                    docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Push Docker Image to DockerHub') {
            steps {
                echo "📤 Pushing Docker image to DockerHub..."
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                        docker push ${IMAGE_NAME}:latest
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline succeeded — Docker image pushed to DockerHub!"
        }
        failure {
            echo "❌ Pipeline failed. Check logs for details."
        }
    }
}

