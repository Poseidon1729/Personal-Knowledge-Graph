from django import forms
from django.forms import formset_factory
from ingest.models import File


class GraphNameForm(forms.Form):
    graph_name = forms.CharField(label="Graph Name")


class GraphForm(forms.Form):
    source = forms.ModelChoiceField(
        queryset=File.objects.all(),
        label="Source"
    )

    relation = forms.CharField(label="Relation")

    target = forms.ModelChoiceField(
        queryset=File.objects.all(),
        label="Target"
    )


GraphFormSet = formset_factory(GraphForm, extra=1)