from django import forms


class CreateNewList(forms.Form):
    name = forms.CharField(label="Название", max_length=127)
    description = forms.CharField(widget=forms.Textarea(), label='Описание', max_length=1023)
    beginning = forms.DateTimeField(label='Время начала', widget=forms.TextInput(attrs={'type': 'date'}))
    geocode = forms.CharField(label='Геокод', max_length=128)
    image = forms.ImageField(required=False, label='Фото')
    limit = forms.IntegerField(label="Лимит участников")
    award = forms.IntegerField(label="Вознаграждение")
