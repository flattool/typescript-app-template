#!/usr/bin/env python3
from template_engine import TemplateEngine
from re import Pattern
# import re

def get_input(
	message: str,
	*,
	is_optional: bool,
	err_message: str = 'Invalid input, please try again...',
	regex: Pattern[str] | None = None,
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

		print(err_message)


def main():
	engine = TemplateEngine()
	engine.register_logic('ifdef', lambda key, context: key in context)
	engine.register_logic('ifundef', lambda key, context: not key in context)


if __name__ == '__main__':
	main()
