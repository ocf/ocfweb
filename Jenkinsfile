node('slave') {
    step([$class: 'WsCleanup'])

    stage('check-out-code') {
        // TODO: I think we can factor out the "src" subdirectory now that we
        // don't build a Debian package?
        dir('src') {
            checkout scm

            // TODO: figure out how to get the git plugin to do this for us
            sh 'git submodule update --init'
        }
    }

    stash 'src'
}

node('slave') {
    step([$class: 'WsCleanup'])
    unstash 'src'

    def sha = sh(script: 'git rev-parse --short HEAD', returnStdout: true)
    def version = "${new Date().format("yyyy-MM-dd-'T'HH-mm-ss")}-git${sha}"

    stash 'src'
}

println "your git sha is: ${sha}"
println "your version: ${version}"

// vim: ft=groovy
