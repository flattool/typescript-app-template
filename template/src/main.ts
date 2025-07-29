import Gio from "gi://Gio?version=2.0"
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
		new Adw.AboutDialog({
			application_name: "<TEMPLATE:APP_TITLE>",
			application_icon: pkg.app_id,
			developer_name: "<TEMPLATE:DEVELOPER_NAME>",
			version: pkg.version,
			developers: ["<TEMPLATE:DEVELOPER_NAME> <<TEMPLATE:DEVELOPER_EMAIL>>"],
			copyright: "© 2025 <TEMPLATE:DEVELOPER_NAME>",
		}).present(this.active_window)
	}

	public override vfunc_activate(): void {
		(this._main_window ??= new MainWindow({ application: this })).present()
	}
}

export function main(argv: string[]): Promise<number> {
	const app = new Application()
	return app.runAsync(argv)
}
