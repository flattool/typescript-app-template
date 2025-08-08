from typing import Callable, List, Dict, Tuple
from typing_extensions import Literal
from pathlib import Path
import re

Token = Tuple[Literal['text', 'var', 'logic_start', 'logic_end'], str]
LogicHandler = Callable[[str, Dict[str, str]], bool]

LOGIC_END = '{{/}}'
ESCAPE_OPEN = '\0FLATTOOL_TEMPLATE_ENGINE_ESCAPE_OPEN\0'
ESCAPE_CLOSE = '\0FLATTOOL_TEMPLATE_ENGINE_ESCAPE_CLOSE\0'

class TemplateEngine:
	_logic_handlers: Dict[str, LogicHandler]

	def __init__(self):
		self._logic_handlers = {}


	def register_logic(self, name: str, handler: LogicHandler):
		self._logic_handlers[name] = handler


	def render(self, template: str, context: Dict[str, str]) -> str:
		template = template.replace("{{{{", ESCAPE_OPEN)
		template = template.replace("}}}}", ESCAPE_CLOSE)

		if re.search(r'{{/\w+}}', template):
			raise ValueError(f'Only {LOGIC_END} is permitted as a block closing tag.')

		tokens = self._tokenize(template)
		output, _ = self._parse(tokens, context)

		output = output.replace(ESCAPE_OPEN, "{{")
		output = output.replace(ESCAPE_CLOSE, "}}")

		return output


	def render_files_recursive(self, template_root: Path, output_root: Path, context: Dict[str, str]):
		for file_path in template_root.rglob('*'):
			if not file_path.is_file():
				continue

			relative_path = file_path.relative_to(template_root)
			rendered_rel_path = self._render_path_parts(relative_path, context)
			output_path = output_root / rendered_rel_path
			output_path.parent.mkdir(parents=True, exist_ok=True)
			content = file_path.read_text(encoding='utf-8')
			rendered_content = self.render(content, context)
			output_path.write_text(rendered_content, encoding='utf-8')


	def _render_path_parts(self, relative: Path, context: Dict[str, str]) -> Path:
		rendered_parts: List[str] = []
		for part in relative.parts:
			rendered = self.render(part, context)
			if not rendered:
				raise ValueError(f'Rendered path component is empty (from {part!r})')

			if rendered in ('.', '..'):
				raise ValueError(f'Invalid rendered path component: {rendered!r}')

			if '/' in rendered or '\\' in rendered:
				raise ValueError(f'Path component contains separator: {rendered!r}')

			rendered_parts.append(rendered)

		return Path(*rendered_parts)


	def _tokenize(self, template: str) -> List[Token]:
		pattern = re.compile(
			r'\{\{#(\w+)\s+(\w+)\}\}|' + re.escape(LOGIC_END) + r'|\{\{(\w+)\}\}',
			re.DOTALL,
		)
		pos = 0
		tokens: List[Token] = []

		# Regex Group                  [0,  1,  2,  3]
		# Variable:    {{var}}         [{{var}},  None,  None,  'var']
		# Logic start: {{#ifdef var}}  [{{#ifdef}},  'ifdef',  'var',  None]
		# Logic end:   LOGIC_END       [LOGIC_END,  None,  None,  None]

		for match in pattern.finditer(template):
			if match.start() > pos:
				tokens.append(('text', template[pos : match.start()]))

			if (func_name := match.group(1)) and (func_arg := match.group(2)):
				tokens.append(('logic_start', f'{func_name}:{func_arg}'))
			elif match.group(0) == LOGIC_END:
				tokens.append(('logic_end', ''))
			elif text := match.group(3):
				tokens.append(('var', text))

			pos = match.end()

		if pos < len(template):
			tokens.append(('text', template[pos :]))

		return tokens


	def _parse(self,
		tokens: List[Token],
		context: Dict[str, str],
		index: int = 0,
	) -> Tuple[str, int]:
		output: str = ''

		while index < len(tokens):
			token_type, value = tokens[index]

			if token_type == 'text':
				output += value
				index += 1
			elif token_type == 'var':
				output += context.get(value, '')
				index += 1
			elif token_type == 'logic_start':
				logic_name, key = value.split(':', 1)
				handler = self._logic_handlers.get(logic_name)
				if handler is None:
					raise ValueError(f'No handler registered for logic: {logic_name}')

				index += 1
				inner_content, index = self._parse(tokens, context, index)
				if handler(key, context):
					output += inner_content

			elif token_type == 'logic_end':
				return output, index + 1

		return output, index
