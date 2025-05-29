#!/usr/bin/env sh
flatpak run org.flatpak.Builder --install --user --force-clean _build build-aux/<TEMPLATE:APPID>.json \
&& flatpak run <TEMPLATE:APPID>//master
