pipeline {
    agent any

    environment {
        SERVER_IP = credentials('prod-server-ip')
        APP_DIR = "/home/mohamed/flask-app"
        ZIP_NAME = "flask-app.zip"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/shehata18/flask-app.git'
            }
        }

        stage('Build & Test') {
            steps {
                sh '''
                python3 -m venv venv || true
                venv/bin/pip install -r requirements.txt
                venv/bin/pip install pytest
                venv/bin/pytest
                '''
            }
        }

        stage('Package App') {
            steps {
                sh '''
                zip -r ${ZIP_NAME} . -x "*.git*" "venv/*"
                '''
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'ssh-key',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {
                    sh '''
                    scp -i $SSH_KEY -o StrictHostKeyChecking=no ${ZIP_NAME} \
                        $SSH_USER@${SERVER_IP}:/home/mohamed/

                    ssh -i $SSH_KEY -o StrictHostKeyChecking=no $SSH_USER@${SERVER_IP} "
                        unzip -o /home/mohamed/${ZIP_NAME} -d ${APP_DIR} &&
                        cd ${APP_DIR} &&
                        venv/bin/pip install -r requirements.txt &&
                        sudo systemctl restart flask-app
                    "
                    '''
                }
            }
        }
    }
}
