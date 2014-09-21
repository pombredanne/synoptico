from django import forms

from .models import Event, TimelineMapping


class TimelineMappingForm(forms.Form):

    offset = forms.CharField()
    event_pk = forms.IntegerField(widget=forms.HiddenInput, required=False)
    event_description = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.timeline = kwargs.pop("timeline")
        super(TimelineMappingForm, self).__init__(*args, **kwargs)

    def clean_offset(self):
        offset = self.cleaned_data["offset"]
        TimelineMapping.validate_offset(self.timeline, offset)
        return offset

    def create_mapping(self):
        if self.cleaned_data["event_pk"] is not None:
            event = Event.objects.get(pk=self.cleaned_data["event_pk"])
        else:
            event = Event.objects.create(
                project=self.timeline.project,
                description=self.cleaned_data["event_description"]
            )
        mapping = self.timeline.mappings.create(
            event=event,
            offset=self.cleaned_data["offset"]
        )
        return mapping