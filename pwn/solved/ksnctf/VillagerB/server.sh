#!/bin/sh
socat TCP-LISTEN:3000,reuseaddr,fork EXEC:"strace ././villager"
