from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError, transaction
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import MissedMeetingReportForm
from .models import MissedMeetingReport


def _get_report_for_action(request, report_id, permission):
    report = MissedMeetingReport.objects.filter(pk=report_id).first()
    if report is None:
        raise Http404("Report not found.")
    if report.user_id != request.user.pk and not request.user.has_perm(permission):
        raise PermissionDenied
    return report


def _month_date(year, month):
    if not 1 <= month <= 12:
        raise Http404("Invalid month.")
    try:
        return date(year, month, 1)
    except ValueError as error:
        raise Http404("Invalid year.") from error


def _month_navigation(year, month):
    current = _month_date(year, month)
    if year == 1 and month == 1:
        previous = None
    elif month == 1:
        previous = current.replace(year=year - 1, month=12)
    else:
        previous = current.replace(month=month - 1)
    if year == 9999 and month == 12:
        following = None
    elif month == 12:
        following = current.replace(year=year + 1, month=1)
    else:
        following = current.replace(month=month + 1)
    return previous, following


@login_required
@permission_required(
    "missed_meetings.access_missed_meeting_reports",
    raise_exception=True,
)
def my_reports(request, year=None, month=None):
    if year is None or month is None:
        selected_month = timezone.localdate().replace(day=1)
        return redirect(
            "missed_meetings:my_reports_month",
            year=selected_month.year,
            month=selected_month.month,
        )

    selected_month = _month_date(year, month)
    form = MissedMeetingReportForm()
    if request.method == "POST":
        form = MissedMeetingReportForm(request.POST)
        if form.is_valid():
            meeting_date = form.cleaned_data["meeting_date"]
            try:
                with transaction.atomic():
                    report = form.save(commit=False)
                    report.user = request.user
                    report.save()
            except IntegrityError:
                if MissedMeetingReport.objects.filter(
                    user=request.user,
                    meeting_date=meeting_date,
                ).exists():
                    form.add_error(
                        "meeting_date",
                        "You have already reported this meeting date.",
                    )
                else:
                    raise
            else:
                messages.success(request, "Your missed meeting was reported.")
                return redirect(
                    "missed_meetings:my_reports_month",
                    year=meeting_date.year,
                    month=meeting_date.month,
                )

    previous_month, next_month = _month_navigation(year, month)
    reports = MissedMeetingReport.objects.filter(
        user=request.user,
        meeting_date__year=year,
        meeting_date__month=month,
    )
    return render(
        request,
        "missed_meetings/monthly_report.html",
        {
            "form": form,
            "reports": reports,
            "selected_month": selected_month,
            "previous_month": previous_month,
            "next_month": next_month,
            "report_count": reports.count(),
            "can_view_all_reports": request.user.has_perm(
                "missed_meetings.view_all_reports"
            ),
        },
    )


@login_required
@permission_required(
    "missed_meetings.access_missed_meeting_reports",
    raise_exception=True,
)
@permission_required("missed_meetings.view_all_reports", raise_exception=True)
def all_reports(request, year=None, month=None):
    if year is None or month is None:
        selected_month = timezone.localdate().replace(day=1)
        return redirect(
            "missed_meetings:all_reports_month",
            year=selected_month.year,
            month=selected_month.month,
        )

    selected_month = _month_date(year, month)
    previous_month, next_month = _month_navigation(year, month)
    reports = (
        MissedMeetingReport.objects.filter(
            meeting_date__year=year,
            meeting_date__month=month,
        )
        .select_related("user")
        .order_by("user__username", "meeting_date")
    )
    return render(
        request,
        "missed_meetings/all_reports_monthly.html",
        {
            "reports": reports,
            "selected_month": selected_month,
            "previous_month": previous_month,
            "next_month": next_month,
            "report_count": reports.count(),
            "member_count": reports.values("user_id").distinct().count(),
            "can_change_reports": request.user.has_perm(
                "missed_meetings.change_missedmeetingreport"
            ),
            "can_delete_reports": request.user.has_perm(
                "missed_meetings.delete_missedmeetingreport"
            ),
        },
    )


@login_required
@permission_required(
    "missed_meetings.access_missed_meeting_reports",
    raise_exception=True,
)
def edit_report(request, report_id):
    report = _get_report_for_action(
        request,
        report_id,
        "missed_meetings.change_missedmeetingreport",
    )
    form = MissedMeetingReportForm(
        request.POST if request.method == "POST" else None,
        instance=report,
    )
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                form.save()
        except IntegrityError:
            if MissedMeetingReport.objects.filter(
                user=report.user,
                meeting_date=form.cleaned_data["meeting_date"],
            ).exclude(pk=report.pk).exists():
                form.add_error(
                    "meeting_date",
                    "You have already reported this meeting date.",
                )
            else:
                raise
        else:
            messages.success(request, "Missed meeting report updated.")
            if request.user.has_perm("missed_meetings.view_all_reports"):
                return redirect(
                    "missed_meetings:all_reports_month",
                    year=report.meeting_date.year,
                    month=report.meeting_date.month,
                )
            return redirect("missed_meetings:my_reports")

    return render(
        request,
        "missed_meetings/edit_report.html",
        {"form": form, "report": report},
    )


@login_required
@permission_required(
    "missed_meetings.access_missed_meeting_reports",
    raise_exception=True,
)
def delete_report(request, report_id):
    report = _get_report_for_action(
        request,
        report_id,
        "missed_meetings.delete_missedmeetingreport",
    )
    if request.method == "POST":
        meeting_date = report.meeting_date
        report.delete()
        messages.success(request, "Missed meeting report deleted.")
        if request.user.has_perm("missed_meetings.view_all_reports"):
            return redirect(
                "missed_meetings:all_reports_month",
                year=meeting_date.year,
                month=meeting_date.month,
            )
        return redirect("missed_meetings:my_reports")

    return render(
        request,
        "missed_meetings/delete_report.html",
        {"report": report},
    )
