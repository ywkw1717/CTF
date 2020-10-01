#!/bin/sh
socat TCP-LISTEN:3000,reuseaddr,fork EXEC:"strace -i ./classic_aa9e979fd5c597526ef30c003bffee474b314e22"
