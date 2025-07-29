import GObject from "gi://GObject?version=2.0"
import Gio from "gi://Gio?version=2.0"
import Adw from "gi://Adw?version=1"

import { MainWindow } from "./window/main_window.js"

export class Application extends Adw.Application {
	static {
		GObject.registerClass(this)
	}

	private main_window?: MainWindow

	public constructor() {
		super({
			application_id: pkg.app_id,
			flags: Gio.ApplicationFlags.DEFAULT_FLAGS,
		})

		// Actions
		const quit_action = new Gio.SimpleAction({ name: "quit" })
		quit_action.connect("activate", () => this.quit())
		this.add_action(quit_action)
		this.set_accels_for_action("app.quit", ["<primary>q"])

		const show_about_action = new Gio.SimpleAction({ name: "about" })
		show_about_action.connect("activate", () => new Adw.AboutDialog({
			application_name: "<TEMPLATE:APP_TITLE>",
			application_icon: pkg.app_id,
			developer_name: "<TEMPLATE:DEVELOPER_NAME>",
			version: pkg.version,
			developers: ["<TEMPLATE:DEVELOPER_NAME> <<TEMPLATE:DEVELOPER_EMAIL>>"],
			copyright: "© 2025 <TEMPLATE:DEVELOPER_NAME>",
		}).present(this.active_window))
		this.add_action(show_about_action)
	}

	public override vfunc_activate(): void {
		if (!this.main_window) {
			this.main_window = new MainWindow({ application: this })
		}

		this.main_window.present()
	}
}

export function main(argv: string[]): Promise<number> {
	const app = new Application()
	return app.runAsync(argv)
}
