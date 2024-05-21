from django import forms


class scraperForm(forms.Form):
    url = forms.URLField(
        label="",
        widget=forms.URLInput(
            attrs={
                "size": 50,
                "placeholder": "Add new Page",
            }
        ),
        initial="",
    )
