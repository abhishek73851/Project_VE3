# analyzer/forms.py
from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "email", "age", "csv_file"]

    def clean_csv_file(self):
        csv_file = self.cleaned_data.get("csv_file")
        if csv_file:
            if not csv_file.name.endswith(".csv"):
                raise forms.ValidationError("Only CSV files are allowed.")
            if csv_file.size > 5 * 1024 * 1024:  # Limit file size to 5MB
                raise forms.ValidationError("File size exceeds the limit of 5MB.")
        return csv_file
