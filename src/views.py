from apscheduler.jobstores.base import JobLookupError
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views import View
from django.views.generic import FormView

from src.forms import NotificationForm, ModifyNotificationForm
from src.notification_utils import get_notifications


class NotificationView(FormView):
    template_name = 'notification_form.html'
    form_class = NotificationForm

    def form_valid(self, form):
        job_id = form.schedule_notification()
        return render_to_response("success.html", context={"job_id_scheduled": job_id})


class ModifyNotificationView(FormView):
    template_name = 'notification_form.html'
    form_class = ModifyNotificationForm

    def form_valid(self, form):
        try:
            job_id, action = form.modify()
        except JobLookupError as e:
            return render_to_response("error.html", context={"etype": e.__class__.__name__, "message": e.message})
        return render_to_response("success.html", context={"job_id_modified": job_id, "action": action})


class ListNotificationView(View):
    http_method_names = ['get']

    def get(self, request):
        job_list = get_notifications()
        return HttpResponse(job_list, content_type='application/json')
