import GLib from "gi://GLib?version=2.0"
import Gio from "gi://Gio?version=2.0"
import Gtk from "gi://Gtk?version=4.0"
import Adw from "gi://Adw?version=1"

import { GObjectify } from "./utils/gobjectify.js"
import { MainWindow } from "./window/main_window.js"

@GObjectify.Class({ manual_gtype_name: "Gjs_Application" })
export class Application extends Adw.Application {
	private _main_window?: MainWindow

	public constructor() {
		super({
			application_id: pkg.app_id,
			flags: Gio.ApplicationFlags.DEFAULT_FLAGS,
		})
	}

	@GObjectify.SimpleAction({ accels: ["<primary>q"] })
	public override quit(): void { super.quit() }

	@GObjectify.SimpleAction()
	protected about(): void {
		const gtk_version = `${Gtk.MAJOR_VERSION}.${Gtk.MINOR_VERSION}.${Gtk.MICRO_VERSION}`
		const adw_version = `${Adw.MAJOR_VERSION}.${Adw.MINOR_VERSION}.${Adw.MICRO_VERSION}`
		const os_string = `${GLib.get_os_info("NAME")} ${GLib.get_os_info("VERSION")}`
		const lang = GLib.environ_getenv(GLib.get_environ(), "LANG")
		const troubleshooting = (
			`OS: ${os_string}\n`
			+ `{{APP_NAME}} version: ${pkg.version}\n`
			+ `GTK: ${gtk_version}\n`
			+ `libadwaita: ${adw_version}\n`
			+ `App ID: ${pkg.app_id}\n`
			+ `Profile: ${pkg.profile}\n`
			+ `Language: ${lang}`
		)

		const dialog = Adw.AboutDialog.new_from_appdata("/{{APP_ID_AS_PATH}}/appdata", null)
		dialog.version = pkg.version
		dialog.debug_info = troubleshooting
		{{#ifset DONATION_LINK}}dialog.add_link(_("Donate"), "{{DONATION_LINK}}")
		{{/}}dialog.present(this.active_window)
	}

	public override vfunc_activate(): void {
		(this._main_window ??= new MainWindow({ application: this })).present()
	}
}

export function main(argv: string[]): Promise<number> {
	const app = new Application()
	return app.runAsync(argv)
}
