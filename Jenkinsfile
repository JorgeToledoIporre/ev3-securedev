pipeline {
    agent any
    stages {
        stage('Construccion') {
            steps {
                bat 'docker build -t app-ev3 .'
            }
        }
        stage('Pruebas') {
            steps {
                bat 'docker run --rm app-ev3 pytest'
            }
        }
        stage('Despliegue') {
            steps {
                bat 'docker rm -f app-ev3 || echo Contenedor previo no encontrado'
                bat 'docker run -d --name app-ev3 -p 5000:5000 app-ev3'
            }
        }
    }
}