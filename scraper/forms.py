from django import forms


class scraperForm(forms.Form):
    url = forms.URLField(
        label="",
        widget=forms.URLInput(attrs={"size": 50}),
        initial="",
        help_text="Add new Page",
    )
