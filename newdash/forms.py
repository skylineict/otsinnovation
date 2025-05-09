from django import forms
from .models import MyUser

class FacilitatorProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 
            'bio', 'profile_image', 'linkedin_profile', 
            'twitter_profile', 'github_profile'
        ]

    def __init__(self, *args, **kwargs):
        super(FacilitatorProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['phone_number'].required = True
