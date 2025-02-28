from django import forms
from django.core.exceptions import ValidationError

class YouTubeDownloadForm(forms.Form):
    youtube_url = forms.URLField(
        label="YouTube Video URL",
        widget=forms.URLInput(attrs={"class": "form-control", "id": "id_youtube_url"}),
        help_text="Enter a valid YouTube URL"
    )

    video_quality = forms.ChoiceField(
        label="Select Video Quality",
        choices=[],  # Initially empty, will be populated via JavaScript
        widget=forms.Select(attrs={"class": "form-select", "id": "id_video_quality"}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        qualities = kwargs.pop('qualities', None)
        super().__init__(*args, **kwargs)
        if qualities:
            self.fields['video_quality'].choices = qualities

    def clean_youtube_url(self):
        url = self.cleaned_data['youtube_url']
        if 'youtube.com' not in url and 'youtu.be' not in url:
            raise ValidationError("Please enter a valid YouTube URL.")
        return url