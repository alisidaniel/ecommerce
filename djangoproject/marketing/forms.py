from django import forms
from .models import MarketingPreference 

class MarketingPreferenceForm(forms.ModelForm):
	subscribed = forms.BooleanField(label=' Receive Marketing Email ? ', required=False, widget=forms.CheckboxInput(
		attrs = {
		"type": "checkbox",
		}
		))
	class Meta:
		model = MarketingPreference
		fields = [
			'subscribed'
			]