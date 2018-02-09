pipeline {
    agent any
    stages {
        stage('Example') {
            steps {
                echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL}"
            }
        }
	 stage('build'){
	    steps{
                sh 'mkdir dinesh'
		sh 'cd dinesh'
		sh 'echo "creating 1st file" > /var/lib/jenkins/workspace/pipeline/dinesh/1stfile'
		sh 'echo "Creating 2nd file" > /var/lib/jenkins/workspace/pipeline/dinesh/2ndfile'
		sh 'echo "creating 3rd file" > /var/lib/jenkins/workspace/pipeline/dinesh/3rdfile'
     
		sh 'echo "The no of files to be dispalyed"'
               
		sh 'ls -ll dinesh'
	
    }
}
}
}


