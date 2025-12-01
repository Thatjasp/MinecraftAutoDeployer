import argparse
import re
import socket
import sys
from contextlib import closing
from dataclasses import dataclass

import docker
from docker.errors import NotFound

client = docker.from_env()


def containerExits(name: str):
    """
    Ensure a Docker container with a given name exists.
    If it exists, return that container object.
    If not, create and return the new container.

    Args:
        name (str): Name of the container.

    Returns:
        bool: Does Container Exist
    """

    # Check if container exists
    try:
        client.containers.get(name)
        return True
    except NotFound:
        print(f"[INFO] Container '{name}' does not exist.")
        return False


def isPortOpen(host: str, portNum: int):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, portNum)) == 0:
            return True
        else:
            print("WARNING: Port", portNum, "not open", file=sys.stderr)
            return False
    return False


def checkPortRegex(arg_value, pat=re.compile(r"^\d{1,5}:\d{1,5}$")):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError("invalid value")
    return arg_value


def addArguments():
    parser = argparse.ArgumentParser(
        prog="Minecraft Server Docker Launcher",
        description="This program spins up a Bedrock or Java Minecraft Server",
        epilog="It will ",
    )
    parser.add_argument("version")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--bedrock", action="store_true")
    group.add_argument("--java", action="store_true")
    parser.add_argument("-p", "--port", type=checkPortRegex)
    return parser.parse_args()


@dataclass
class bedrockServerParams:
    detach: bool
    version: str
    name: str


@dataclass
class bedrockEnviromentVariables:
    eula: bool


def bedrockServer(version: str, name: str, internalPort: str, externalPort: str):
    client.images.pull("itzg/minecraft-bedrock-server", "latest")
    enviromentVariableMap = {"EULA": True, "VERSION": version}
    ports = {internalPort: externalPort}
    #    volumeMap = {"mc-bedrock-data:/data"}
    client.containers.run(
        "itzg/minecraft-bedrock-server",
        environment=enviromentVariableMap,
        detach=True,
        name=name,
        ports=ports,
    )


if __name__ == "__main__":
    dockerArgs = addArguments()
    version = dockerArgs.version
    argPorts = dockerArgs.port.split(":")
    # I will need to parse internal due to need for tcp
    internalPort = argPorts[0]
    externalPort = argPorts[1]
    #    if not isPortOpen("localhost", int(externalPort)):
    #        exit(-1)
    if dockerArgs.bedrock:
        bedrockServer(version, "minecraft", internalPort, externalPort)
    if dockerArgs.java:
        raise Exception("JAVA NOT IMPLEMENTED")
