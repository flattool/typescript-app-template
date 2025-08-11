#!/usr/bin/env sh
flatpak run org.flatpak.Builder --install --user --force-clean _build build-aux/{{APP_ID}}.json \
&& flatpak run {{APP_ID}}//master
