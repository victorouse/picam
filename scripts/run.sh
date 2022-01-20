#!/bin/bash

set -e

PI_HOST="pi@raspberrypi.local"
PI_HOME="/home/pi"
HOST_HOME="$(pwd)"

function shell() {
  echo "Starting ssh session"
  ssh -Y "$PI_HOST"
}

function cmd() {
  echo "Running: $1"
  ssh -t "$PI_HOST" "$1"
}

function copy_to_pi() {
  echo "Copying from: $HOST_HOME/* to: $PI_HOST:$PI_HOME"
  scp -r "$HOST_HOME" "$PI_HOST:$PI_HOME"
}

function copy_from_pi() {
  echo "Copying from: $PI_HOST:$PI_HOME to: $HOST_HOME/*"
  scp -r "$PI_HOST:$PI_HOME" "$HOST_HOME"
}

function copy_file_from_pi() {
  echo "Copying from: $PI_HOST:$PI_HOME to: $HOST_HOME/$1"
  scp -r "$PI_HOST:$PI_HOME/$1" "$HOST_HOME/$1"
}

function run() {
  copy_to_pi
  cmd "python pi/main.py"
}

eval "$@"
