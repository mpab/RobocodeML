#!/usr/bin/env bash

ROBOCODE=robocode-1.9.3.2

if [ -d "./$ROBOCODE" ]; then
    echo "robocode folder '$ROBOCODE' already exists"
    exit
fi

java -jar installers/$ROBOCODE-setup.jar ./$ROBOCODE