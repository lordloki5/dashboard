import reflex as rx
from dashboard.pages.home import  home
from dashboard.pages.live import  live
from dashboard.pages.status import  status
from dashboard.pages.diff import  diff
from dashboard.pages.versioncmp import  versioncmp



app = rx.App()
app.add_page(home, route="/")
app.add_page(live, route="/live")
app.add_page(status, route="/status")
app.add_page(diff, route="/diff")
app.add_page(versioncmp, route="/versioncmp")

