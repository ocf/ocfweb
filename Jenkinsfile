if (env.BRANCH_NAME == 'master') {
    properties([
        pipelineTriggers([
            triggers: [
                [
                    $class: 'jenkins.triggers.ReverseBuildTrigger',
                    upstreamProjects: 'ocflib/master', threshold: hudson.model.Result.SUCCESS
                ]
            ]
        ]),
    ])
}

def sha

node('slave') {
    step([$class: 'WsCleanup'])

    stage('check-out-code') {
        // TODO: I think we can factor out the "src" subdirectory now that we
        // don't build a Debian package?
        dir('src') {
            checkout scm
            sha = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()

            // TODO: figure out how to get the git plugin to do this for us
            sh 'git submodule update --init'
        }
    }

    stash 'src'
}

def version = "${new Date().format("yyyy-MM-dd-'T'HH-mm-ss")}-git${sha}"
withEnv([
    'DOCKER_REPO=docker-push.ocf.berkeley.edu/',
    "DOCKER_REVISION=${version}",
]) {
    parallel(
        test: {
            node('slave') {
                unstash 'src'
                stage('test') {
                    dir('src') {
                        sh 'make test'
                    }
                }
            }
        },

        cook_image: {
            node('slave') {
                step([$class: 'WsCleanup'])
                unstash 'src'
                stage('cook-image') {
                    dir('src') {
                        sh 'make cook-image'
                    }
                }
            }
        },
    )


    if (env.BRANCH_NAME == 'master') {
        node('deploy') {
            step([$class: 'WsCleanup'])
            unstash 'src'

            stage('push-to-registry') {
                dir('src') {
                    sh 'make push-image'
                }
            }

            stage('deploy-to-prod') {
                // TODO: make these deploy and roll back together!
                build job: 'marathon-deploy-app', parameters: [
                    [$class: 'StringParameterValue', name: 'app', value: 'ocfweb/web'],
                    [$class: 'StringParameterValue', name: 'version', value: version],
                ]
                build job: 'marathon-deploy-app', parameters: [
                    [$class: 'StringParameterValue', name: 'app', value: 'ocfweb/worker'],
                    [$class: 'StringParameterValue', name: 'version', value: version],
                ]
                build job: 'marathon-deploy-app', parameters: [
                    [$class: 'StringParameterValue', name: 'app', value: 'ocfweb/static'],
                    [$class: 'StringParameterValue', name: 'version', value: version],
                ]
            }
        }
    }
}


// vim: ft=groovy
