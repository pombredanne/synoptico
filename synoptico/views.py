import json

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView, CreateView

from account.mixins import LoginRequiredMixin

from .forms import TimelineMappingForm
from .models import Project, Timeline, TimelineMapping


class HomePageView(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context.update({
            "projects": Project.objects.all(),
        })
        return context


class ProjectDetailView(DetailView):
    model = Project


class TimelineDetailView(DetailView):
    model = Timeline

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        queryset = queryset.filter(project__slug=slug)
        try:
            obj = queryset.get(pk=pk)
        except queryset.model.DoesNotExist:
            raise Http404("No timeline found matching the query")
        return obj

    def get_context_data(self, **kwargs):
        context = super(TimelineDetailView, self).get_context_data(**kwargs)
        context.update({
            "form": TimelineMappingForm(timeline=self.get_object())
        })
        return context


class TimelineMappingCreateView(LoginRequiredMixin, CreateView):
    form_class = TimelineMappingForm
    model = TimelineMapping

    def dispatch(self, request, *args, **kwargs):
        self.timeline = get_object_or_404(Timeline, pk=kwargs["pk"])
        return super(TimelineMappingCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TimelineMappingCreateView, self).get_form_kwargs()
        kwargs.update({
            "timeline": self.timeline
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(TimelineMappingCreateView, self).get_context_data(**kwargs)
        context.update({"timeline": self.timeline})
        return context

    def form_valid(self, form):
        form.save(who=self.request.user)
        print form.cleaned_data
        if self.request.POST.get("save") == "add-another":
            url = reverse(
                "timeline_events_mapping_create",
                args=[self.timeline.project.slug, self.timeline.pk]
            )
        else:
            url = reverse(
                "timeline_detail",
                args=[self.timeline.project.slug, self.timeline.pk]
            )
        return HttpResponseRedirect(url)


def ajax_autocomplete_events(request, pk):
    project = get_object_or_404(Project, pk=pk)
    events = project.events.all()
    data = [
        {
            "pk": event.pk,
            "description": event.description,
            "mappings": [
                {"pk": m.pk, "offset": m.offset_display(), "timeline": m.timeline.name}
                for m in event.mappings.all()
            ]
        }
        for event in events
    ]
    return HttpResponse(json.dumps(data), content_type="application/json")
