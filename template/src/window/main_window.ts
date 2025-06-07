import GObject from "gi://GObject?version=2.0"
import Gio from "gi://Gio?version=2.0"
import Adw from "gi://Adw?version=1"

import { Config } from "../config.js"

export class MainWindow extends Adw.ApplicationWindow {
	static {
		GObject.registerClass(
			{
				GTypeName: "MainWindow",
				Template: "resource:///<TEMPLATE:APPID.as_path>/window/main_window.ui",
				InternalChildren: ["toolbar_view", "header_bar", "status_page"],
			},
			this,
		)
	}

	readonly toolbar_view!: Adw.ToolbarView
	readonly header_bar!: Adw.HeaderBar
	readonly status_page!: Adw.StatusPage

	readonly settings: Gio.Settings

	constructor(params?: Partial<Adw.ApplicationWindow.ConstructorProps>) {
		super(params)

		if (Config.PROFILE === "development") {
			this.add_css_class("devel")
		}

		this.settings = new Gio.Settings({ schema_id: Config.APP_ID })

		print(`Welcome to ${Config.APP_ID}!`)
	}
}
