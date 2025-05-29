#!/usr/bin/env python3
import re, json, sys, shutil, subprocess
from datetime import datetime
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve()
SCRIPT_DIR = SCRIPT_PATH.parent
TEMPLATE_DIR = SCRIPT_DIR / "template"
TEMPLATE_CONFIG_PATH = SCRIPT_DIR / "TEMPLATE_CONFIG.json"
IGNORE_FILE_AND_DIRS = [
	"node_modules",
	"package-lock.json",
]

def err_exit(message: str):
	print(message)
	sys.exit(1)


def app_name_input() -> str:
	name_regex = re.compile("^(?![.])[A-Za-z0-9!#$%&()*+,\\-.:<=>?[\\]^_{}|~]+$")
	while True:
		app_name = input("App name (e.g: my-app): ").strip()
		if app_name and name_regex.search(app_name):
			return app_name

		print("Input was not a valid app name (must be a valid Linux filename with no special characters")


def id_input() -> str:
	while True:
		appid = input("Enter App ID (e.g org.website.MyApp): ").strip()
		split_id = appid.split(".")
		if len(split_id) < 3:
			print("App ID must contain 2 periods (.)")
			continue

		for part in split_id[0 : -2]:
			if "-" in part:
				print("Hyphen (-) is only allowed in the last part ID")
				continue

		return appid


def url_input(message: str) -> str:
	link_regex = re.compile(
		"((http|https)://)(www.)?[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)"
	)
	while True:
		link = input(message).strip()
		if link and link_regex.search(link):
			return link

		print("Input was not a valid URL")


def repo_input(app_name: str) -> str:
	while True:
		repo = url_input("Enter Git repository URL (last part must match app name) (repo does not need to exist yet): ")
		last_part = repo.split("/")[-1]
		if last_part == app_name:
			return repo

		print("Last part did not match app name")
		print(f"Last part: {last_part}")
		print(f"App name: {app_name}")


def email_input() -> str:
	email_regex = re.compile("^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$")
	while True:
		email = input("Enter Developer's Email: ").strip()
		if email and email_regex.search(email):
			return email

		print("Input was not a valid email")


def copy_files(destination_dir: Path):
	if destination_dir.exists():
		err_exit(f"Path already exists at {destination_dir}")

	try:
		shutil.copytree(TEMPLATE_DIR, destination_dir, ignore=shutil.ignore_patterns(*IGNORE_FILE_AND_DIRS))
	except Exception as e:
		err_exit(f"Error occurred when trying to copy template files:\n{e}")


def rename_files(project_dir: Path, replacements: dict[str, str]):
	if not project_dir.exists() or not project_dir.is_dir():
		err_exit(f"Project path {project_dir} is not a directory or doesn't exist")

	# Iterate from deepest path first, to ensure safe renaming
	for path in sorted(project_dir.rglob("*"), key=lambda p: -len(p.parts)):
		if path.is_file() or path.is_dir():
			new_name = path.name
			for old, new in replacements.items():
				if old in new_name:
					new_name = new_name.replace(old, new)

			if new_name != path.name:
				new_path = path.parent / new_name
				path.rename(new_path)


def replace_text(project_dir: Path, replacements: dict[str, str]):
	for path in project_dir.rglob("*"):
		if path.is_file():
			content = ""
			try:
				content = path.read_text(encoding="utf-8")
			except (UnicodeDecodeError, FileNotFoundError):
				continue

			new_content = content
			for old, new in replacements.items():
				if old in new_content:
					new_content = new_content.replace(old, new)

			if new_content != content:
				path.write_text(new_content, encoding="utf-8")


def install_node_packages(project_path: Path):
	while True:
		response = input("Install Node packages for linting and formatting? [Y|n]: ").strip().lower()
		if response in ["y", "n", ""]:
			if response == "n":
				return

			break

	try:
		print("Installing Node packages for linting and formatting...")
		subprocess.run(["npm", "install"], cwd=project_path, check=True)
	except Exception as e:
		print("Failed to install Node packages due to error:")
		print(e)
		print("\nContinuing with project initialization...")


def get_input_no_skip(message: str, lower=False) -> str:
	while True:
		response = input(message).strip()
		if len(response) > 0:
			return response.lower() if lower else response


if __name__ == "__main__":
	config = {}
	try:
		with TEMPLATE_CONFIG_PATH.open("r") as f:
			config = json.load(f)
	except FileNotFoundError:
		err_exit(f"Could not find config at {TEMPLATE_CONFIG_PATH}")
	except json.JSONDecodeError:
		err_exit(f"Invalid JSON format at {TEMPLATE_CONFIG_PATH}")

	REPLACEMENTS: dict[str, str] = {
		# CLI Inputs
		"<TEMPLATE:APP_NAME>": (app_name := app_name_input()),
		"<TEMPLATE:GIT_REPO_URL>": repo_input(app_name),
		"<TEMPLATE:APP_TITLE>": get_input_no_skip("App title (e.g: My App): "),
		"<TEMPLATE:APPID>": (appid := id_input()),
		"<TEMPLATE:APPID.as_path>": appid.replace(".", "/"),
		"<TEMPLATE:DEVELOPER_NAME>": get_input_no_skip("Developer name: "),
		"<TEMPLATE:DEVELOPER_EMAIL>": email_input(),
		"<TEMPLATE:DEVELOPER_DONATION_LINK>": url_input("Enter Developer's Donation Link: "),

		# Config Options
		"<TEMPLATE:RUNTIME_VERSION>": config["runtime_version"],
		"<TEMPLATE:BLUEPRINT_COMPILER_TAG>": config["blueprint_compiler_tag"],

		# Other Values
		"<TEMPLATE:CURRENT_DATE>": datetime.now().strftime("%Y-%m-%d"),
		"<ESCAPE_NAME>": "",
	}

	project_path = SCRIPT_DIR.parent / REPLACEMENTS["<TEMPLATE:APP_NAME>"]

	copy_files(project_path)
	rename_files(project_path, REPLACEMENTS)
	replace_text(project_path, REPLACEMENTS)
	install_node_packages(project_path)

	try:
		print("Initializing Git repo...")
		subprocess.run(["git", "init", "-b", "main"], cwd=project_path, check=True)

		print("Adding and initializing gi-types submodule...")
		subprocess.run([
			"git", "submodule", "add",
			"-b", "nightly",
			"--name", "gi-types",
			"https://gitlab.gnome.org/BrainBlasted/gi-typescript-definitions",
			"gi-types",
		], cwd=project_path, check=True)

		print("Installing Flatpak runtime and sdk...")
		subprocess.run([
			"flatpak", "install",
			"org.flatpak.Builder",
			f"org.gnome.Sdk//{config['runtime_version']}",
			f"org.gnome.Platform//{config['runtime_version']}"
		], check=True)
	except subprocess.CalledProcessError as e:
		err_exit(f"Init commands failed:\n{e}")

	print(f"\nProject created at: {project_path}")
	print("Make sure to setup proper metadata, desktop entry, and Code Of Conduct contact info!")
