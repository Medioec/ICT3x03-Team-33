pipeline {
    agent none
    stages {
        stage('OWASP DependencyCheck') {
            agent { label 'builtin' }
            steps {
                dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'OWASP Dependency Check'
            }
        }
        stage('Sonarqube') {
            agent { label 'builtin' }
            steps {
                script {
                    def scannerHome = tool 'sonarqube';
                    withSonarQubeEnv('sonarqube') {
                    sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=3x03 -Dsonar.sources=."
                    }
                }

            }
        }
        stage('Build Test') {
            agent { label 'builtin' }
            steps {
                withCredentials([file(credentialsId: 'test_secrets', variable: 'secrets_file')]) {
                    sh '''
                        chmod 700 -R scripts/
                        . ./scripts/set-env.sh env/test/.env
                        ./scripts/docker-build.sh test
                    '''
                }
            }
        }
        stage('Test') {
            agent { label 'builtin' }
            steps {
                withCredentials([file(credentialsId: 'test_secrets', variable: 'secrets_file')]) {
                    sh '''
                        chmod 700 -R scripts/
                        . ./scripts/set-env.sh env/test/.env
                        ./scripts/cert-gen.sh
                        ./scripts/docker-deploy.sh test
                        ./scripts/test.sh test
                        ./scripts/docker-kill-volumes.sh test
                    '''
                }
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
