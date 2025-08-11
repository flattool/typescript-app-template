#!/usr/bin/env python3
import json
from template_engine import TemplateEngine
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Pattern
import re, subprocess

SCRIPT_PATH = Path(__file__).resolve()
SCRIPT_DIR = SCRIPT_PATH.parent
TEMPLATE_DIR = SCRIPT_DIR / "template"
TEMPLATE_CONFIG_PATH = SCRIPT_DIR / "TEMPLATE_CONFIG.json"
IGNORE_FILE_AND_DIRS = [
	"node_modules",
	"package-lock.json",
]
REGEXES = {
	'No Slashes': re.compile(r'^[^/\\]+$'),
	'File Path': re.compile("^(?![.])[A-Za-z0-9!#$%&()*+,\\-.:<=>?[\\]^_{}|~]+$"),
	'URL': re.compile(
		'((http|https)://)(www.)?[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)'
	),
	'App ID': re.compile('^(?:[a-zA-Z0-9_]+\\.){2,}[a-zA-Z0-9_-]+$'),
	'Email': re.compile('^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$'),
	'Yes or No or empty': re.compile('^[YyNn]?$'),
}

def get_input(
	message: str,
	*,
	is_optional: bool = False,
	err_message: str = 'Invalid input',
	regex: Optional[Pattern[str]] = None,
) -> str:
	message += (' (leave blank to ignore)' if is_optional else '') + ': '
	while True:
		response = input(message).strip()

		if is_optional and response == '':
			return ''

		if regex:
			if regex.fullmatch(response):
				return response
		elif len(response) > 0:
			return response

		print('. '.join((err_message, 'Please try again...')))


def ask_for_details() -> Dict[str, str]:
	app_name = get_input('Enter app name (e.g: my-app)', regex=REGEXES['File Path'])
	app_title = get_input(
		'Enter app title (e.g: My App)',
		err_message="Title must exist and cannot contain '/' or '\\'",
		regex=REGEXES['No Slashes'],
	)
	app_id = get_input(
		'Enter application ID (e.g: org.website.MyApp)',
		err_message=(
			'App ID must exist, contain 2 periods, be alphanumeric, cannot start nor end with a period,'
	 		+ ' and can only contain hyphens (-) in the last part'
		),
		regex=REGEXES['App ID'],
	)
	git_repo = get_input(
		'Enter Git repository URL (repo does not need to exist yet)',
		err_message='Response must be a valid URL',
		regex=REGEXES['URL'],
	)
	developer_name = get_input("Enter developer's name")
	include_coc: bool = get_input(
		'Does this project follow the GNOME Code of Conduct? [Y|n]',
		regex=REGEXES['Yes or No or empty'],
	) in ('Y', 'y', '')
	if not include_coc:
		IGNORE_FILE_AND_DIRS.append('CODE_OF_CONDUCT.md')

	# Optionals
	developer_email = get_input(
		"Enter developer's email address",
		is_optional=not include_coc,
		err_message='Response must be a valid email address',
		regex=REGEXES['Email'],
	)
	donation_link = get_input(
		"Enter developer's donation link",
		is_optional=True,
		err_message='Response must be a valid URL',
		regex=REGEXES['URL'],
	)

	return {
		'APP_NAME': app_name,
		'APP_TITLE': app_title,
		'APP_ID': app_id,
		'APP_ID_AS_PATH': app_id.replace('.', '/'),
		'DEVELOPER_NAME': developer_name,
		'DEVELOPER_EMAIL': developer_email,
		'DONATION_LINK': donation_link,
		'GIT_REPO': git_repo,
		'INCLUDE_COC': 'yes' if include_coc else '',
		'CURRENT_DATE_Y_m_d': datetime.now().strftime("%Y-%m-%d"),
	}


def install_deps(config: Dict[str, str]):
	print('Installing Flatpak dependencies...')
	subprocess.run([
		'flatpak', 'install',
		'org.flatpak.Builder',
		f"org.gnome.Sdk//{config['RUNTIME_VERSION']}",
		f"org.gnome.Platform//{config['RUNTIME_VERSION']}",
		f"org.freedesktop.Sdk.Extension.node20//{config['TS_NODE_RUNTIME_VERSION']}",
		f"org.freedesktop.Sdk.Extension.typescript//{config['TS_NODE_RUNTIME_VERSION']}",
	], check=True)


def git_setup(project_path: Path, config: Dict[str, str]):
	if not project_path.is_dir():
		raise ValueError(f"Project Path '{project_path.absolute()} is missing or is not a directory")

	print('Initializing Git repo...')
	subprocess.run(['git', 'init', '-b', 'main'], cwd=project_path, check=True)
	print('Adding and initializing gi-types submodule...')
	subprocess.run([
		'git', 'submodule', 'add',
		'-b', 'nightly',
		'--name', 'gi-types',
		'https://gitlab.gnome.org/BrainBlasted/gi-typescript-definitions',
		'gi-types',
	], cwd=project_path, check=True)
	print('Adding template as first commit...')
	subprocess.run(['git', 'add', '.'], cwd=project_path, check=True)
	subprocess.run([
		'git', 'commit',
		'-m', 'Initial commit: Flattool TypeScript App Template',
	], cwd=project_path, check=True)


def ask_and_install_node_packages(project_path: Path):
	response = get_input(
		'Install Node packages for formatting and linting? [Y|n]',
		regex=REGEXES['Yes or No or empty'],
	)
	if response in ('Y', 'y', ''):
		print('Installing Node packages for linting and formatting...')
		subprocess.run(['npm', 'install'], cwd=project_path, check=True)


def main():
	if not TEMPLATE_DIR.is_dir():
		raise ValueError(f"{TEMPLATE_DIR} directory is missing or is not a directory")

	if not TEMPLATE_CONFIG_PATH.is_file():
		raise ValueError(f"{TEMPLATE_CONFIG_PATH} directory is missing or is not a file")

	config = json.load(TEMPLATE_CONFIG_PATH.open('r'))
	context = ask_for_details()
	context.update(config)

	new_project_path = SCRIPT_DIR.parent / context['APP_NAME']
	if new_project_path.exists():
		print(f"\nDirectory at '{new_project_path.absolute()}' already exists!")
		return

	engine = TemplateEngine()
	engine.register_logic('ifset', lambda key, ctx: len(ctx.get(key, '')) > 0)
	engine.register_logic('ifunset', lambda key, ctx: len(ctx.get(key, '')) == 0)
	engine.render_files_recursive(TEMPLATE_DIR, new_project_path, context, ignore_paths=IGNORE_FILE_AND_DIRS)

	ask_and_install_node_packages(new_project_path)
	install_deps(config)
	git_setup(new_project_path, context)

	print(f"\nProject created at: '{new_project_path}'")
	print('Make sure to setup proper metadata, README info, and desktop entry items!')


if __name__ == '__main__':
	main()
