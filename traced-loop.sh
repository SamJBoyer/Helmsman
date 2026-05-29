#!/bin/bash
maxloops=$1
sysprompt=$2
instructions=$3

completed=false

trace_dir="agent_traces"


if [ -d "agent_traces" ]; then
    echo "Moving agent_traces to legacy"
    if [ ! -d "legacy" ]; then
        mkdir legacy
    fi
    
    
    mv agent_traces legacy/agent_traces-$(date +%Y%m%d%H%M%S)
fi




mkdir -p $trace_dir


for ((i=0; i<maxloops; i++)); do

    loop_dir="ralph-$i"
    mkdir -p $trace_dir/$loop_dir

    prompt_worker=$(< $sysprompt)
    instruct=" follow these instructions: "
    prompt_worker+="$instruct"
    prompt_worker+=$(< $instructions)

    output_worker=$(agent -f --trust --model auto --approve-mcps "$prompt_worker")

    trace_path=$trace_dir/$loop_dir/trace.md
    echo $output_worker > $trace_path

    prompt_supervisor=$(< Agents/supervisor.txt)
    prompt_supervisor+="$instruct"
    prompt_supervisor+="@$trace_path"
    output_supervisor=$(agent -f --trust --model auto --approve-mcps "$prompt_supervisor")
    supervisor_path=$trace_dir/$loop_dir/supervisor.md
    echo $output_supervisor > $supervisor_path

    if [[ $output_worker == *"<promise>COMPLETE</promise>"* ]]; then
        echo "Complete"
        completed=true
        break
    fi
    echo "Loop $i"
done

if [ "$completed" = false ]; then
    echo "Failed to complete the task in $maxloops loops"
fi