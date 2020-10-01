#!/bin/sh
# socat TCP-LISTEN:3000,reuseaddr,fork EXEC:"strace -i ./one_ef36d5ef6169aeda65259f627f282930b93cf6e5"
socat tcp-l:3000.reuseaddr exec:"./one_ef36d5ef6169aeda65259f627f282930b93cf6e5"
