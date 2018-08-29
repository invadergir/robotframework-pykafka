#!/bin/bash

export KAFKA_BROKER_VERSION="1.0.0"
export KAFKA_HOST="localhost:9092"

set -x
if [ -z "$OUTPUTDIR" ]; then
    export OUTPUTDIR=results
fi

ROBOT_TEST_FILE="$1"
if [ -z "$ROBOT_TEST_FILE" ]; then
    #export ROBOT_TEST_FILE=text-produce-consume.robot
    ROBOT_TEST_FILE=json-produce-consume.robot
fi
set +x
echo "Using:"
echo "OUTPUTDIR=$OUTPUTDIR"
echo "ROBOT_TEST_FILE=$ROBOT_TEST_FILE"
SUCCESS=false
set -x
robot -d $OUTPUTDIR  $ROBOT_TEST_FILE && SUCCESS=true
set +x
if ! $SUCCESS; then
    chromium --new-window results/report.html  &
    #FILE=$(readlink -f results/log.html)
    #chromium --new-window 'file://'$FILE'#s1-t1'  &
fi
