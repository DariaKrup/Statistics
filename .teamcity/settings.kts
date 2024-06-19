import jetbrains.buildServer.configs.kotlin.*
import jetbrains.buildServer.configs.kotlin.buildFeatures.perfmon
import jetbrains.buildServer.configs.kotlin.buildSteps.python
import jetbrains.buildServer.configs.kotlin.projectFeatures.awsConnection
import jetbrains.buildServer.configs.kotlin.projectFeatures.dockerRegistry

/*
The settings script is an entry point for defining a TeamCity
project hierarchy. The script should contain a single call to the
project() function with a Project instance or an init function as
an argument.

VcsRoots, BuildTypes, Templates, and subprojects can be
registered inside the project using the vcsRoot(), buildType(),
template(), and subProject() methods respectively.

To debug settings scripts in command-line, run the

    mvnDebug org.jetbrains.teamcity:teamcity-configs-maven-plugin:generate

command and attach your debugger to the port 8000.

To debug in IntelliJ Idea, open the 'Maven Projects' tool window (View
-> Tool Windows -> Maven Projects), find the generate task node
(Plugins -> teamcity-configs -> teamcity-configs:generate), the
'Debug' option is available in the context menu for the task.
*/

version = "2024.03"

project {

    buildType(Build)

    features {
        dockerRegistry {
            id = "PROJECT_EXT_35"
            name = "Docker Registry Project"
            userName = "dariakrup"
            password = "credentialsJSON:f542aff8-3ffb-4261-aa16-ec09ee610f31"
        }
        awsConnection {
            id = "TokenStatisticsLabs_AmazonWebServicesAwsProjectLevel"
            name = "Amazon Web Services (AWS) Project Level"
            regionName = "eu-west-1"
            credentialsType = static {
                accessKeyId = "AKIA5JH2VERVI62P5XDY"
                secretAccessKey = "credentialsJSON:c758ca1d-ccfb-4180-a136-53b3aa8941f9"
                stsEndpoint = "https://sts.eu-west-1.amazonaws.com"
            }
            allowInSubProjects = true
            allowInBuilds = true
        }
    }
}

object Build : BuildType({
    name = "Build"

    vcs {
        root(DslContext.settingsRoot)
    }

    steps {
        python {
            id = "python_runner"
            command = file {
                filename = "lab1.py"
            }
        }
        python {
            id = "python_runner_1"
            command = file {
                filename = "lab2.py"
            }
        }
    }

    triggers {
        trigger {
            type = "vcsTrigger"
        }
    }

    features {
        perfmon {
        }
    }
})
