from django import forms
from .models import Post


class SecurityQuestions(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('onprem_sid', 'name', 'email')

    def clean(self):
        pass


class ChangePassword(forms.Form):
    old_pass = forms.CharField(widget=forms.PasswordInput())
    new_pass = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = '__all__'

    def clean(self):
        cleaned_data = super(ChangePassword, self).clean()
        old_pass = cleaned_data.get("old_pass")
        new_pass = cleaned_data.get("new_pass")
        confirm_password = cleaned_data.get("confirm_password")

        if new_pass != confirm_password:
            raise forms.ValidationError(
                "New password does not match"
            )


class LookUpUser(forms.Form):
    email = forms.CharField()

    class Meta:
        fields = '__all__'


class ForgotPassword(forms.Form):
    answer_one = forms.CharField(max_length=200)
    answer_two = forms.CharField(max_length=200)
    answer_three = forms.CharField(max_length=200)

    class Meta:
        fields = '__all__'


class ResetPassword(forms.Form):
    new_pass = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = '__all__'

    def clean(self):
        cleaned_data = super(ResetPassword, self).clean()
        new_pass = cleaned_data.get("new_pass")
        confirm_password = cleaned_data.get("confirm_password")

        if new_pass != confirm_password:
            raise forms.ValidationError(
                "New password does not match"
            )
