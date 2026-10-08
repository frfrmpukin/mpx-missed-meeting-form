from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

from . import urls


class MissedMeetingsMenuItemHook(MenuItemHook):
    def render(self, request):
        if not request.user.has_perm(
            "missed_meetings.access_missed_meeting_reports"
        ):
            return ""
        return super().render(request)


@hooks.register("url_hook")
def register_urls():
    return UrlHook(urls, "missed_meetings", r"^missed-meetings/")


@hooks.register("menu_item_hook")
def register_menu():
    return MissedMeetingsMenuItemHook(
        "Missed Meetings",
        "fas fa-calendar-check fa-fw",
        "missed_meetings:my_reports",
        order=1100,
    )
