#!/usr/bin/env bash

ROBOCODE=./robocode-1.9.3.2

start_listener() {
./python/listener.py &
}

start_robocode () {
  java -Xmx512M \
  -Dsun.io.useCanonCaches=false \
  -Ddebug=true \
  -DNOSECURITY=true \
  -DROBOTPATH=./target/classes \
  -cp "$ROBOCODE/libs/*:./lib/*:./target:/*" robocode.Robocode \
  -battle ./train.battle \
  -tps 100 &
}

#mvn clean install
#start_listener
#rm -rf $ROBOCODE/robots/Bots
#cp -R target/classes/Bots $ROBOCODE/robots/Bots

start_robocode

trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

wait