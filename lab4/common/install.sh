#!/bin/sh

apk add openrc && \
apk add strongswan

mkdir -p /run/openrc/exclusive
touch /run/openrc/softlevel

