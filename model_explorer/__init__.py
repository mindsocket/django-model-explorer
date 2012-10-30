from django.contrib import admin
from functools import update_wrapper
from django.core.exceptions import PermissionDenied
from django.contrib.admin.options import csrf_protect_m
from django.contrib.admin.views.main import ChangeList
import logging
from django import forms

logger = logging.getLogger(__name__)

class ChartForm(forms.Form):
    chart_row = forms.ChoiceField()
    chart_col = forms.ChoiceField()
    chart_var = forms.ChoiceField()
    chart_measure = forms.ChoiceField(choices=(("Sum", "Sum"), ("Count", "Count"), ("Average", "Average")))

    def __init__(self, chart_fields, chart_vars):
        super(ChartForm, self).__init__()
        choices = [(field, field) for field in chart_fields]
        self.fields['chart_row'].choices = choices
        self.fields['chart_col'].choices = choices
        choices = [(field, field) for field in chart_vars]
        self.fields['chart_var'].choices = choices

class ExplorerList(ChangeList):
    chart_fields = []

    def __init__(self, request, *args, **kwargs):
        get = request.GET.copy()
        self.chart_row = get.pop('chart_row', None)
        self.chart_col = get.pop('chart_col', None)
        self.chart_var = get.pop('chart_var', None)
        self.chart_measure = get.pop('chart_measure', None)
        request.GET = get
        ChangeList.__init__(self, request, *args, **kwargs)

class ModelAdmin(admin.ModelAdmin):
    change_list_template = "model_explorer/change_list.html"
    chart_template = None
    categorical_fields = None
    measure_fields = None
    actions = None
    chart_fields = []
    chart_vars = []

    def get_urls(self):
        from django.conf.urls import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        urlpatterns = patterns('',
            url(r'^chart/$',
                wrap(self.chart_view),
                name='%s_%s_chart' % info),
        )
        urlpatterns += super(ModelAdmin, self).get_urls()
        return urlpatterns

    def get_changelist(self, request, **kwargs):
        return ExplorerList

    def get_chart_fields(self):
        if self.chart_fields:
            return self.chart_fields

        from django.db import models
        chart_fields = []
        for field in self.model._meta.fields:
            if field.choices or isinstance(field, models.NullBooleanField) or isinstance(field, models.BooleanField):
                chart_fields.append(field.name)
        return chart_fields

    def get_chart_vars(self):
        if self.chart_vars:
            return self.chart_vars

        from django.db import models
        chart_vars = []
        for field in self.model._meta.fields:
            if isinstance(field, models.FloatField) or isinstance(field, models.IntegerField):
                chart_vars.append(field.name)
        return chart_vars

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        response = super(ModelAdmin, self).changelist_view(request, extra_context=extra_context)
        explorer_list = response.context_data['cl']
        explorer_list.chart_fields = self.get_chart_fields()
        explorer_list.chart_vars = self.get_chart_vars()
        if explorer_list.chart_fields:
            explorer_list.chart_form = ChartForm(chart_fields=explorer_list.chart_fields, chart_vars=explorer_list.chart_vars)
        return response

    @csrf_protect_m
    def chart_view(self, request, extra_context=None):
        """
        The 'chart' admin view for this model.
        """
        response = self.changelist_view(request, extra_context)
        response.template_name = self.chart_template or [
            'model_explorer/%s/%s/chart.html' % (response.context_data['app_label'], response.context_data['cl'].model._meta.object_name.lower()),
            'model_explorer/%s/chart.html' % response.context_data['app_label'],
            'model_explorer/chart.html'
        ]
        return response