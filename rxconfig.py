import reflex as rx

config = rx.Config(
    app_name="demo",
    app_module_import="demo.app",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
