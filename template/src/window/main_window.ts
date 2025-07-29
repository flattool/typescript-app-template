import GObject from "gi://GObject?version=2.0"
import Gio from "gi://Gio?version=2.0"
import Adw from "gi://Adw?version=1"

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

	protected readonly toolbar_view!: Adw.ToolbarView
	protected readonly header_bar!: Adw.HeaderBar
	protected readonly status_page!: Adw.StatusPage

	protected readonly settings = new Gio.Settings({ schema_id: pkg.app_id })

	public constructor(params?: Partial<Adw.ApplicationWindow.ConstructorProps>) {
		super(params)

		if (pkg.profile === "development") this.add_css_class("devel")
		print(`Welcome to ${pkg.app_id}!`)
	}
}
