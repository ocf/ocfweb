stage name: 'clean-workspace'
node('slave') {
    step([$class: 'WsCleanup'])
}

// check out code
stage name: 'check-out-code'
node('slave') {
    dir('src') {
        checkout scm
    }
    stash 'src'
}


// run tests
stage name: 'test'

node('slave') {
    unstash 'src'
    dir('src') {
        sh 'make test'
    }
}

// cook images
stage name: 'test-cook-image'

node('slave') {
    unstash 'src'
    dir('src') {
        sh 'make cook-image'
    }
}


// deploy to prod
if (env.BRANCH_NAME == 'master') {
    def version = new Date().format("yyyy-MM-dd-'T'HH-mm-ss")
    withEnv([
        'DOCKER_REPO=docker-push.ocf.berkeley.edu/',
        "DOCKER_REVISION=${version}",
    ]) {
        stage name: 'cook-prod-image'
        node('slave') {
            unstash 'src'
            dir('src') {
                sh 'make cook-image'
            }
        }

        stage name: 'push-to-registry'
        node('deploy') {
            unstash 'src'
            dir('src') {
                sh 'make push-image'
            }
        }
    }

    stage name: 'deploy-to-prod'
    // TODO: make these deploy and roll back together!
    build job: 'marathon-deploy-app', parameters: [
        [$class: 'StringParameterValue', name: 'app', value: 'ocfweb/web'],
        [$class: 'StringParameterValue', name: 'version', value: version],
    ]
    build job: 'marathon-deploy-app', parameters: [
        [$class: 'StringParameterValue', name: 'app', value: 'ocfweb/worker'],
        [$class: 'StringParameterValue', name: 'version', value: version],
    ]
}


// vim: ft=groovy
