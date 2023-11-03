pipeline {
    agent none
    stages {
        stage('Build Test') {
            agent { label 'builtin' }
            steps {
                sh 'chmod 700 -R scripts/'
                sh './scripts/docker-build.sh test'
            }
        }
        stage('OWASP DependencyCheck') {
            agent { label 'builtin' }
            steps {
                dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'OWASP Dependency Check'
            }
        }
        stage('Test') {
            agent { label 'builtin' }
            steps {
                sh 'chmod 700 -R scripts/'
                sh './scripts/cert-gen.sh'
                sh './scripts/docker-deploy.sh test'
                sh 'docker ps'
                sh './scripts/test.sh test'
                sh './scripts/docker-kill-volumes.sh test'
            }
        }
        stage('Build Stg') {
            agent { label 'host' }
            steps {
                withCredentials([file(credentialsId: 'stg_secrets', variable: 'secrets_file')]) {
                    sh '''
                        chmod 700 -R scripts/
                        . ./scripts/set-env.sh
                        ./scripts/docker-build.sh stg
                    '''
                }
            }
        }
        stage('Test Stg') {
            agent { label 'host' }
            steps{
                withCredentials([file(credentialsId: 'stg_secrets', variable: 'secrets_file')]) {
                    sh '''
                        chmod 700 -R scripts/
                        . ./scripts/set-env.sh
                        ./scripts/cert-gen.sh
                        ./scripts/docker-deploy.sh stg
                        ./scripts/test.sh stg
                    '''
                }
            }
        }
        stage('Build Prod') {
            agent { label 'host' }
            steps {
                withCredentials([file(credentialsId: 'prod_secrets', variable: 'secrets_file')]) {
                    sh '''
                        chmod 700 -R scripts/
                        . ./scripts/set-env.sh
                        ./scripts/docker-build.sh prod
                    '''
                }
            }
        }
        stage('Deploy Prod') {
            agent { label 'host' }
            steps {
                withCredentials([file(credentialsId: 'prod_secrets', variable: 'secrets_file')]) {
                    sh '''
                        chmod 700 -R scripts/
                        . ./scripts/set-env.sh
                        ./scripts/cert-gen.sh
                        ./scripts/docker-deploy.sh prod
                        ./scripts/test.sh prod
                    '''
                }
            }
        }
    }
    post {
        success {
            node('builtin') {
                dependencyCheckPublisher pattern: 'dependency-check-report.xml'
            }
        }
    }
}
