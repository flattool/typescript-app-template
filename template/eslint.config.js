import { defineConfig } from "eslint/config"
import tsParser from "@typescript-eslint/parser"
import tsPlugin from "@typescript-eslint/eslint-plugin"
import prettierPlugin from "eslint-plugin-prettier"
import prettierConfig from "eslint-config-prettier"
import jsonc from "eslint-plugin-jsonc"

// Rules that apply to both JS and TS
const sharedJsTsRules = {
	"object-shorthand": ["error", "always"],
	"prettier/prettier": "error",
}

export default defineConfig([
	{
		ignores: [
			"**/.*",
			"**/*.d.ts",
			"**/__pycache__",
			"_build",
			"node_modules",
			"package.json",
			"package-lock.json",
			"gi-types",
		],
	},
	{
		// JavaScript
		files: ["**/*.js"],
		languageOptions: {
			parserOptions: {
				sourceType: "module",
			},
		},
		plugins: {
			prettier: prettierPlugin,
		},
		rules: {
			...sharedJsTsRules,
		},
		...prettierConfig.flat,
	},
	{
		// TypeScript
		files: ["**/*.ts"],
		languageOptions: {
			parser: tsParser,
			parserOptions: {
				ecmaVersion: "latest",
				sourceType: "module",
				project: "./tsconfig.json",
			},
		},
		plugins: {
			"@typescript-eslint": tsPlugin,
			prettier: prettierPlugin,
		},
		rules: {
			...sharedJsTsRules,
			"@typescript-eslint/explicit-function-return-type": "error",
		},
		...prettierConfig.flat,
	},
	{
		// JSON
		files: ["**/*.json", "**/*.json.in"],
		languageOptions: {
			parser: jsonc,
		},
		plugins: {
			jsonc,
			prettier: prettierPlugin,
		},
		rules: {
			"prettier/prettier": "error",
		},
		...prettierConfig.flat,
	},
])
