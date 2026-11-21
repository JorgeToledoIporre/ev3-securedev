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
        stage('Pruebas de Seguridad - OWASP ZAP') {
            steps {
                bat 'ping -n 6 127.0.0.1 > nul'
                bat 'docker run --rm ghcr.io/zaproxy/zaproxy:stable zap-full-scan.py -t "http://host.docker.internal:5000/hello?name=test" || echo Escaneo ZAP finalizado con alertas detectadas'
            }
        }
    }
}