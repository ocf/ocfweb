pipeline {
  // TODO: Make this cleaner: https://issues.jenkins-ci.org/browse/JENKINS-42643
  triggers {
    upstream(
      upstreamProjects: (env.BRANCH_NAME == 'master' ? 'ocflib/master,dockers/master' : ''),
      threshold: hudson.model.Result.SUCCESS,
    )
  }

  agent {
    label 'slave'
  }

  options {
    ansiColor('xterm')
    timeout(time: 1, unit: 'HOURS')
  }

  script {
    def sha
  }

  stages {
    stage('init-submodules') {
      steps {
        sha = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()

        // TODO: figure out how to get the git plugin to do this for us
        sh 'git submodule update --init'
      }
    }

    script {
      def version = "${new Date().format("yyyy-MM-dd-'T'HH-mm-ss")}-git${sha}"
    }

    stage('parallel-test-cook') {
      environment {
        DOCKER_REPO = 'docker-push.ocf.berkeley.edu/'
        DOCKER_REVISION = version
      }
      parallel {
        stage('test') {
          steps {
            sh 'make test'
          }
        }

        stage('cook-image') {
          steps {
            sh 'make cook-image'
          }
        }
      }
    }

    stage('push-to-registry') {
      when {
        branch 'master'
      }
      agent {
        label 'deploy'
      }
      steps {
        sh 'make push-image'
      }
    }

    stage('deploy-to-prod') {
      when {
        branch 'master'
      }
      agent {
        label 'deploy'
      }
      steps {
        // TODO: Make these deploy and roll back together!
        // TODO: Also try to parallelize these if possible?
        marathonDeployApp('ocfweb/web', version)
        marathonDeployApp('ocfweb/worker', version)
        marathonDeployApp('ocfweb/static', version)
      }
    }
  }

  post {
    failure {
      emailNotification()
    }
    always {
      node(label: 'slave') {
        ircNotification()
      }
    }
  }
}

// vim: ft=groovy
