from django import forms
from django.core.exceptions import ValidationError
from .models import Config
from topo_proxy.tunnels.facebook import FacebookAPI


class ConfigForm(forms.ModelForm):

    class Meta:
        model = Config
        fields = ('remote_account', 'local_account', 'delay', 'timeout',)

    def clean_account(self, key):
        data = self.cleaned_data[key]
        metadata = data.split(':', 1)

        if len(metadata) != 2:
            raise ValidationError("Should look like 'usernme:password'")

        email, password = metadata
        fb = FacebookAPI()

        try:
            fb.login(email, password)
        except Exception as e:
            print(e)
            raise ValidationError("Incorrect username or password.")

        return data

    def clean_remote_account(self):
        return self.clean_account('remote_account')

    def clean_local_account(self):
        return self.clean_account('local_account')
