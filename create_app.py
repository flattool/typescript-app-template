#!/usr/bin/env python3
from template_engine import TemplateEngine

def main():
	engine = TemplateEngine()
	engine.register_logic("ifdef", lambda key, context: key in context)
	engine.register_logic("ifundef", lambda key, context: not key in context)
	print("WIP")


if __name__ == "__main__":
	main()
