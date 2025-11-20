#!/usr/bin/env bash

HERE="$(dirname "$0")"
cd "$HERE"

# Create a full-static binary that should not require dependencies on libc
# https://stackoverflow.com/questions/61319677/flags-needed-to-create-static-binaries-in-golang

CGO_ENABLED=0 go build -trimpath -o bin/paf -a -ldflags '-extldflags -static' "$@"

