from django.forms import ClearableFileInput


class ClearableImageInput(ClearableFileInput):
    template_name = 'qa/forms/widgets/clearable_image_input.html'
