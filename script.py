import argparse
import socket
from contextlib import closing
from dataclasses import dataclass

import docker

client = docker.from_env()


def addArguments():
    parser = argparse.ArgumentParser(
        prog="Minecraft Server Docker Launcher",
        description="This program spins up a Bedrock or Java Minecraft Server",
        epilog="It will ",
    )
    parser.add_argument("version")
    parser.add_argument("--bedrock", action="store_true")
    parser.add_argument("--java", action="store_true")


def checkPort(host: str, portNum: int):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, portNum)) == 0:
            return True
        else:
            return False
    return False


@dataclass
class bedrockServerParams:
    detach: bool
    version: str
    name: str


def bedrockServer(version: str, name: str):
    client.images.pull("itzg/minecraft-bedrock-server", version)
    enviromentVariableMap = {"EULA": True}
    #    volumeMap = {"mc-bedrock-data:/data"}
    client.containers.run(
        "itzg/minecraft-bedrock-server",
        environment=enviromentVariableMap,
        detach=True,
        name=name,
    )


if __name__ == "__main__":
    addArguments()
    checkPort("localhost", 25565)
    client.images.pull("itzg/minecraft-server:latest")
    bedrockServer("latest", "minecraft1")
