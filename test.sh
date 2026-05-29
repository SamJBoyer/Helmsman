#!/bin/bash
set -euo pipefail

if [ "${1:-}" = "validate" ]; then
    output=$(python3 hello_world.py)
    if [ "$output" != "hello world" ]; then
        echo "hello_world.py: expected 'hello world', got '$output'" >&2
        exit 1
    fi
    echo "validate: hello_world.py OK"
    exit 0
fi

maxloops=$1
sysprompt=$2
instructions=$3

completed=false

mkdir -p agent_traces


for ((i=0; i<maxloops; i++)); do

    trace_dir="ralph-$i"
    mkdir -p agent_traces/$trace_dir

    prompt=$(< $sysprompt)
    prompt+=" follow these instructions: "
    prompt+=$(< $instructions)

    echo "$prompt"

    echo "Loop $i"
done

if [ "$completed" = false ]; then
    echo "Failed to complete the task in $maxloops loops"
fi