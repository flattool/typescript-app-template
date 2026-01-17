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

## UI Files

Instead of using XML files for UI, this template favors using [Blueprint Compiler](https://gnome.pages.gitlab.gnome.org/blueprint-compiler/).
A BLP file for the main window will be created in the resulting `PROJECT/src/window/main_window.blp`, and can be used as a starting pint.

To add a new UI file to the project, just create it wherever you want!
The Meson build system has been configured to automatically find all BLP files in `src/`, compile them, and even generate a gresource file for them, so you don't need to lift a finger!

## Icons

To find new icons to use for your app, we reccomend using [Icon Library](https://flathub.org/en/apps/org.gnome.design.IconLibrary), which features many, many icons that match the Adwaita style.

To add these new icons to your app, simply put the icon's XML file into `PROJECT/data/icons/`.
The Meson build system has been configured to automatically find all SVG files in `data/icons/` and generate a gresource file for them, so you, again, don't need to lift a finger!

## GObjectify

[GObjectify](https://github.com/flattool/gobjectify) is a powerful helper-library to make data-drive apps in GNOME JS with TS. This template utilizes it heavily.
Class files with GObjectify look a bit different than with vanilla GNOME JS, but it's all the same under the hood. It's been included to vastly improve the app-writing experience.
GObjectify's [repo](https://github.com/flattool/gobjectify) includes examples of usage, along with vast JSDoc comments to help you get started!

## GIR TypeScript Types

This template relies on Flattool's generated GObject types for TypeScript. You shouldn't need to worry about it apart from updating it over time with your app.
[Its repo](https://github.com/flattool/gir-ts-types) has the instructions on how to update the types.

## ESLint

The template will create an NPM project in the new app's project directory, and then optionally runs `npm install` for the project. This, of course, requires that `npm` is installed on your system. If you do not wish to use ESLint, then you do not need `npm` at all.

## Configuration

Most configuration is done interactively via `create_project.py`, but the GNOME runtime version and Blueprint Compiler version are kept track in `./TEMPLATE_CONFIG.json`. This file will be updated in this repo to follow GNOME releases. New options may be added in the future, so if it has been a while since the last time you created an app, it is recommended to clone this repo again.

## Credits

Credit to the [GNOME Typescript Template](https://gitlab.gnome.org/World/javascript/gnome-typescript-template), for the typings in `src/types/`, original `meson.build` files, and for the overall inspiration of this template.
