from django.urls import path

from . import views

app_name = "missed_meetings"

urlpatterns = [
    path("", views.my_reports, name="my_reports"),
    path("<int:year>/<int:month>/", views.my_reports, name="my_reports_month"),
    path("report/<int:report_id>/edit/", views.edit_report, name="edit_report"),
    path("report/<int:report_id>/delete/", views.delete_report, name="delete_report"),
    path("admin/", views.all_reports, name="all_reports"),
    path(
        "admin/<int:year>/<int:month>/",
        views.all_reports,
        name="all_reports_month",
    ),
]
