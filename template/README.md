# {{APP_TITLE}}
## Flattool template default readme blurb

PUT PROJECT SPECIFIC ITEMS DETAILS HERE

## 📜 Code of Conduct
- The Ignition project follows the [GNOME Code of Conduct](https://conduct.gnome.org/). See `CODE_OF_CONDUCT.md` for more information.

## 👥 Contributing
### Compiling from Source

Make sure `flatpak` and `git` are installed, then run the following to build from the repo:
```bash
# Clone this repo and enter it
git clone {{GIT_REPO}}
cd {{APP_NAME}}
git submodule update --init

# Install build dependencies
flatpak install org.flatpak.Builder org.gnome.Sdk//{{RUNTIME_VERSION}} org.gnome.Platform//{{RUNTIME_VERSION}} org.freedesktop.Sdk.Extension.typescript//{{TS_NODE_RUNTIME_VERSION}} org.freedesktop.Sdk.Extension.node20//{{TS_NODE_RUNTIME_VERSION}} -y

# Build, install, and run
./run.sh
```

### Formatting CHANGE ME !!!!!!
{{APP_TITLE}} uses [pre-commit](https://pre-commit.com/) for code formatting.
- Install using `pip install pre-commit`
- Run `pre-commit install` in the Ignition repository root to set up pre-commit for this repo.
- Run `pre-commit run --all-files` to format all files in the repository.

If you run into a situation where pre-commit is broken, you can use `git commit --no-verfiy` to skip the pre-commit checks.
