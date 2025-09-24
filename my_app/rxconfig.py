import reflex as rx

config = rx.Config(
    app_name="app",
    backend_port=8000,
    frontend_port=3000,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
