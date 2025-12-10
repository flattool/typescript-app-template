# {{APP_TITLE}}
## Flattool template default readme blurb

PUT PROJECT SPECIFIC ITEMS DETAILS HERE

{{#ifset INCLUDE_COC}}## Code of Conduct
- The {{APP_TITLE}} project follows the [GNOME Code of Conduct](https://conduct.gnome.org/). See `CODE_OF_CONDUCT.md` for more information.

{{/}}## Contributing
### Compiling from Source

Make sure `flatpak` and `git` are installed, then run the following to build from the repo:
```bash
# Clone this repo and enter it
git clone {{GIT_REPO}}
cd {{APP_NAME}}

# Initialize submodules
git submodule update --init --recursive

# Install build dependencies
flatpak install org.flatpak.Builder org.gnome.Sdk//{{RUNTIME_VERSION}} org.gnome.Platform//{{RUNTIME_VERSION}} org.freedesktop.Sdk.Extension.typescript//{{TS_NODE_RUNTIME_VERSION}} org.freedesktop.Sdk.Extension.node{{NODE_VERSION}}//{{TS_NODE_RUNTIME_VERSION}} -y

# Build, install, and run
./run.sh
```

### Formatting
{{APP_TITLE}} uses [ESLint](https://eslint.org/) plugins for code formatting. An NPM package file is provided for easy installation.
- Install using `npm install` in the project root directory
