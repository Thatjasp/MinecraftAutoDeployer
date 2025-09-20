import os
import docker

client = docker.from_env()


def bedrockServer(version: str):
    client.images.pull("itzg/minecraft-bedrock-server", version)
    enviromentVariableMap = {'EULA': True}
    volumeMap = {"mc-bedrock-data:/data"}
    client.containers.run("itzg/minecraft-bedrock-server",
                          environment=enviromentVariableMap, volume=volumeMap)


if __name__ == "__main__":
    client.images.pull("ubuntu:latest")
#    bedrockServer("1.3.2")
