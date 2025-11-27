# Flattool TypeScript App Template
---
### Generate new Libadwaita applications that follow Flattool's conventions and practices.

This template serves as a base for new apps, and ensures that all future apps follow a similar directory structure and codebase.

## Usage

**You will need Python >= 3.6 for this!**

```bash
# Clone this repo and enter it
git clone https://github.com/flattool/typescript-app-template
cd typescript-app-template

# Create a new project
python create_app.py
```
After filling out the details, a new directory with the app name will be made in this project's parent directory. Then, `cd` to that newly made directory and run `./run.sh`.

## ESLint

The template will create an NPM project in the new app's project directory, and then optionally runs `npm install` for the project. This, of course, requires that `npm` is installed on your system. If you do not wish to use ESLint, then you do not need `npm` at all.

## Configuration

Most configuration is done interactively via `create_project.py`, but the GNOME runtime version and Blueprint Compiler version are kept track in `./TEMPLATE_CONFIG.json`. This file will be updated in this repo to follow GNOME releases. New options may be added in the future, so if it has been a while since the last time you created an app, it is recommended to clone this repo again.

## Credits

Credit to the [GNOME Typescript Template](https://gitlab.gnome.org/World/javascript/gnome-typescript-template), for the typings in `src/types/`, original `meson.build` files, and for the overall inspiration of this template.
