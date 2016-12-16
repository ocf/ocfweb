node('slave') {
    step([$class: 'WsCleanup'])

    stage('check-out-code') {
        // TODO: I think we can factor out the "src" subdirectory now that we
        // don't build a Debian package?
        dir('src') {
            checkout scm
            def sha = sh(script: 'git rev-parse --short HEAD', returnStdout: true)

            // TODO: figure out how to get the git plugin to do this for us
            sh 'git submodule update --init'
        }
    }

    stash 'src'
}

def version = "${new Date().format("yyyy-MM-dd-'T'HH-mm-ss")}-git${sha}"
println "your git sha is: ${sha}"
println "your version: ${version}"

// vim: ft=groovy
