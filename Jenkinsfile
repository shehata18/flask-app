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

        stage('Debug Env') {
            steps {
                sh '''
                whoami
                which python3
                python3 --version
                which pip
                env
                '''
            }
        }


        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv || true
                source venv/bin/activate
                python3 -m pip install --upgrade pip
                python3 -m pip install -r requirements.txt
                python3 -m pip install pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                source venv/bin/activate
                pytest
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

                    ssh -i $SSH_KEY -o StrictHostKeyChecking=no $SSH_USER@${SERVER_IP} << EOF
                        unzip -o /home/mohamed/${ZIP_NAME} -d ${APP_DIR}
                        cd ${APP_DIR}
                        source venv/bin/activate
                        pip install -r requirements.txt
                        sudo systemctl restart flask-app
                    EOF
                    '''
                }
            }
        }
    }
}
