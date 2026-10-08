# Alliance Auth Missed Meeting Reports

An Alliance Auth app for members to record missed meetings they listened to.
Each submission stores the member and meeting date, and members can submit one
entry per meeting date. Submissions also include an optional comments field
for questions, comments, complaints, or concerns, limited to 500 characters.

Members can view, edit, and delete their own submissions. Authorized users can
view monthly summaries for all members and, when granted the corresponding
permissions, edit or delete any member's submission.
Access to the app itself is controlled separately, so administrators can limit
who sees the navigation link and can open any of its pages.

## Installation

Install the package in the Alliance Auth virtual environment:

```shell
pip install git+https://github.com/frfrmpukin/mpx-missed-meeting-form.git
```

Add `missed_meetings` to `INSTALLED_APPS` in your Alliance Auth settings, then
apply database migrations, collect static files, and restart Alliance Auth:

```shell
python /home/allianceserver/myauth/manage.py migrate
python /home/allianceserver/myauth/manage.py collectstatic --noinput
supervisorctl restart myauth:
```

Alliance Auth hooks add the **Missed Meetings** link to the navigation menu.

## Permissions

Assign these permissions to users or groups in Alliance Auth's permission
settings:

| Permission | What it allows |
|---|---|
| **Can access missed meeting reports** (`access_missed_meeting_reports`) | Allows access to the app and displays its navigation link. Assign this permission to the users or groups who should use the module. |
| **Can add missed meeting report** (`add_missedmeetingreport`) | Standard Django add permission. The member submission form does not require it. |
| **Can view missed meeting report** (`view_missedmeetingreport`) | Standard Django view permission. It does not grant access to the all-members monthly summary. |
| **Can change missed meeting report** (`change_missedmeetingreport`) | Allows editing any member's submission. Members can edit their own submissions without it. |
| **Can delete missed meeting report** (`delete_missedmeetingreport`) | Allows deleting any member's submission. Members can delete their own submissions without it. |
| **Can view all missed meeting reports** (`view_all_reports`) | Grants access to the monthly summary of all members' submissions. |

The add, view, change, and delete permissions are Django's standard model
permissions. `access_missed_meeting_reports` and `view_all_reports` are
permissions added by this app.
