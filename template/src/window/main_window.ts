import Gio from "gi://Gio?version=2.0"
import Adw from "gi://Adw?version=1"

import { GObjectify } from "../utils/gobjectify.js"

@GObjectify.Class({ template: "/<TEMPLATE:APPID.as_path>/window/main_window" })
export class MainWindow extends Adw.ApplicationWindow {
	protected readonly settings = new Gio.Settings({ schema_id: pkg.app_id })

	public constructor(params?: Partial<Adw.ApplicationWindow.ConstructorProps>) {
		super(params)

		if (pkg.profile === "development") this.add_css_class("devel")
		print(`Welcome to ${pkg.app_id}!`)
	}
}
