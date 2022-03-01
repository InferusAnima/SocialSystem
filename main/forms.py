from django import forms


class CreateNewList(forms.Form):
    name = forms.CharField(label="Название", max_length=127)
    description = forms.CharField(widget=forms.Textarea(), label='Описание', max_length=1023)
    beginning = forms.DateTimeField(label='Время начала', widget=forms.TextInput(attrs={'type': 'date'}))
    geocode = forms.CharField(label='Геокод', max_length=128)
    image = forms.ImageField(required=False, label='Фото')
    limit = forms.IntegerField(label="Лимит участников")
    award = forms.IntegerField(label="Вознаграждение")


class EditProfile(forms.Form):
    image = forms.ImageField(required=False, label='Фото')
    geocode = forms.CharField(required=False, label='Геокод', max_length=128)
    phone = forms.CharField(required=False, label='Телефон', max_length=16)
    about = forms.CharField(widget=forms.Textarea(), required=False, label='О себе', max_length=256)

