pkgdatadir = get_option('datadir') / meson.project_name()
gnome = import('gnome')

blueprints = custom_target(
	'blueprints',
	input: files(
		'gtk/help-overlay.blp',
		'window/main_window.blp',
	),
	output: '.',
	command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

tsc_out = meson.project_build_root() / 'tsc-out'

typescript = custom_target(
	'typescript-compile',
	build_by_default: true,
	build_always_stale: true,
	command: [ tsc, '-p', meson.project_source_root() / 'tsconfig.json', '--outDir', tsc_out ],
	output: ['tsc-output'],
)

bin_conf = configuration_data()
bin_conf.set('GJS', find_program('gjs').full_path())
bin_conf.set('PACKAGE_VERSION', meson.project_version())
bin_conf.set('PACKAGE_NAME', meson.project_name())
bin_conf.set('prefix', get_option('prefix'))
bin_conf.set('libdir', get_option('prefix') / get_option('libdir'))
bin_conf.set('datadir', get_option('prefix') / get_option('datadir'))
bin_conf.set('resource_path', '<TEMPLATE:APPID.as_path>')
bin_conf.set('APP_ID', '<TEMPLATE:APPID>')

bin_conf.set('PROFILE', profile)
if get_option('profile') == 'development'
	vcs_tag = run_command('git', 'rev-parse', '--short', 'HEAD').stdout().strip()
	bin_conf.set('VERSION', meson.project_version() + '.dev-' + vcs_tag)
else
	bin_conf.set('VERSION', meson.project_version())
endif

config_vars = configure_file(
	input: 'config.json.in',
	output: 'config.json',
	configuration: bin_conf,
)

data_res = gnome.compile_resources(
	'<TEMPLATE:APPID>.data',
	'<TEMPLATE:APPID>.data.gresources.xml',
	gresource_bundle: true,
	install: true,
	install_dir: pkgdatadir,
	dependencies: [blueprints, config_vars],
)

configure_file(
	input: '<TEMPLATE:APPID>.in',
	output: '<TEMPLATE:APPID>',
	configuration: bin_conf,
	install: true,
	install_dir: get_option('bindir'),
	install_mode: ['rwxr-xr-x', 'root', 'root'],
)

src_res = gnome.compile_resources(
	'<TEMPLATE:APPID>.src',
	'<TEMPLATE:APPID>.src.gresources.xml',
	gresource_bundle: true,
	install: true,
	install_dir: pkgdatadir,
	source_dir: tsc_out,
	dependencies: [
		config_vars,
		typescript,
	],
)
