from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _


class ContentTypeRestrictedFileField(FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    """
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop('content_types') if 'content_types' in kwargs else []
        self.max_upload_size = kwargs.pop('max_upload_size') if 'max_upload_size' in kwargs else 0

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def save_form_data(self, instance, data):
        if data is not None:
            _file = getattr(instance, self.attname)
            if _file != data:
                _file.delete(save=False)
        super(ContentTypeRestrictedFileField, self).save_form_data(instance, data)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)
        _file = data.file

        try:
            content_type = _file.content_type
            if content_type in self.content_types:
                if _file._size > self.max_upload_size:
                    raise forms.ValidationError(_('Please keep filesize under {}. Current filesize {}').format(
                        filesizeformat(self.max_upload_size), filesizeformat(_file._size))
                    )
            else:
                raise forms.ValidationError(_('Filetype not supported'))
        except AttributeError:
            pass

        return data
