from django.forms import ModelForm, ValidationError
from .models import SimpleModel

class SimpleForm(ModelForm):
    class Meta:
        model = SimpleModel
        fields = ['name', 'occupation']
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        occupation = cleaned_data.get('occupation')
        print('COMPARE',name, occupation)
        if name != occupation:
            raise ValidationError("Must match")
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name != 'chetan':
            raise ValidationError(f"Name must be 'chetan' but you entered {name} ")
        print('EXECUTION STOPS HERE')
        return name
