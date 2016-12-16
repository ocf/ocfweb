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
