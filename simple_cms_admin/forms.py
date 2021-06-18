from django import forms


class ThingForm(forms.Form):
    tenant_id = forms.UUIDField()
    thing_type_id = forms.UUIDField()
    data = forms.CharField()
    is_published = forms.BooleanField(required=False)
    archive_at = forms.DateTimeField(required=False)
    publish_at = forms.DateTimeField(required=False)
