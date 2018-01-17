#!/bin/bash
sleep 5
wget -q $1 -O jasmine-agent.py
systemctl restart jasmine-agent.service