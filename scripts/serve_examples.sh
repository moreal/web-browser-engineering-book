#!/bin/bash

set -e

command -v python3 >/dev/null 2>&1 || { echo >&2 "python3 is required but not installed. Aborting."; exit 1; }

python3 -m http.server -d examples
