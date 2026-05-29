#!/bin/bash
set -euo pipefail

if [ "${1:-}" = "validate" ]; then
    output=$(python3 hello_world.py)
    if [ "$output" != "hello world" ]; then
        echo "hello_world.py: expected 'hello world', got '$output'" >&2
        exit 1
    fi
    echo "validate: hello_world.py OK"

    root="$(cd "$(dirname "$0")" && pwd)"
    export PATH="${root}/bin:${PATH}"
    if ! command -v matlab >/dev/null 2>&1; then
        echo "hello_world.m: matlab not found (install MathWorks MATLAB or set MATLAB_ROOT)" >&2
        exit 1
    fi
    output=$(matlab -batch "cd('${root}'); run('hello_world.m')" 2>&1 | tr -d '\r' | tail -n 1)
    if [ "$output" != "hello world" ]; then
        echo "hello_world.m: expected 'hello world', got '$output'" >&2
        exit 1
    fi
    echo "validate: hello_world.m OK"

    output=$(python3 add_one_two.py)
    if [ "$output" != "3" ]; then
        echo "add_one_two.py: expected '3', got '$output'" >&2
        exit 1
    fi
    echo "validate: add_one_two.py OK"
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
