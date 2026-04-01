#!/usr/bin/env sh

LOCAL_REPO={{APP_NAME}}-local-repo

flatpak run org.flatpak.Builder --force-clean --user --repo=LOCAL_REPO _build build-aux/{{APP_ID}}.json
flatpak build-bundle LOCAL_REPO {{APP_NAME}}.flatpak {{APP_ID}}
rm -rf LOCAL_REPO

unset LOCAL_REPO
