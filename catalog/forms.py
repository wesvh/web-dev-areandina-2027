from django import forms

from .models import Option


class VoteForm(forms.Form):
    option = forms.ModelChoiceField(
        queryset=Option.objects.none(),
        widget=forms.RadioSelect,
        empty_label=None,
        label="Selecciona una opción",
    )

    def __init__(self, poll, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["option"].queryset = poll.options.all()
