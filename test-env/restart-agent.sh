#!/bin/bash

# kill current jasmine-agent
if $(ps axuf | grep -q [j]asmine-agent)
then
    kill $(ps axuf | grep [j]asmine-agent | tr -s " " | cut -d' ' -f2)
fi

# run jasmine-agent in screen
screen -S jasmine-agent -dm bash -c "cd /opt/jasmine-agent/; python3 jasmine-agent.py"