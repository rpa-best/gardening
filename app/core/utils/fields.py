from django.db.models import CharField


class StrippingCharField(CharField):
    def formfield(self, **kwargs):
        kwargs['strip'] = True
        return super().formfield(**kwargs)
    
    def to_python(self, value: str) -> str:
        return value.strip().replace(" ", "")