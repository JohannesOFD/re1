plugins {
    kotlin("js") version "1.8.0" // Stelle sicher, dass das Kotlin-Plugin installiert ist
}

repositories {
    mavenCentral()
}

kotlin {
    js {
        browser {
            webpackTask {
                outputFileName = "bundle.js"
            }
        }
    }
}

tasks.register<Copy>("copyHtml") {
    from("index.html")
    into("$buildDir/distributions")
}

tasks.getByName("jsWebpack") {
    finalizedBy(tasks.named("copyHtml"))
}
