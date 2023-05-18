from django import forms
from .models import UserProfile,Galery,ChatMessage



#Це визначення класу форми Django з назвою `UserProfileForm`. Він успадковується від вбудованого класу `ModelForm` модуля `forms` Django.
#Клас `Meta` всередині класу `UserProfileForm` є контейнером для зберігання метаданих форми.
#У цьому випадку він визначає атрибут `model` як модель `UserProfile`. Це означає, що дана форма буде використовуватися для обробки даних для створення або оновлення екземплярів моделі `UserProfile`.
#Атрибут `fields` визначає, які саме поля з моделі `UserProfile` повинні бути включені у форму.
#У цьому випадку до форми додаються поля `'name'`, `'age'`, `'image'` і `'phone_number'`. Ці поля будуть відображатися у формі і можуть бути відредаговані користувачем.
#За замовчуванням, кожне поле у формі матиме віджет за замовчуванням, який відповідає типу даних поля.
# Наприклад, поле `CharField` матиме віджет `TextInput`, а поле `DateField` матиме віджет `DateInput`.
#Однак віджет для кожного поля можна налаштувати, передавши додаткові аргументи до визначення поля.


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name','age','image','telephone_number']





#GaleryForm - це форма, що дозволяє додавати зображення до галереї, яка пов'язана з моделлю Galery.
#Властивість Meta класу GaleryForm містить метадані форми, в даному випадку - вказується модель Galery,
# з якою пов'язана форма, та список полів ['image'], які будуть відображені у формі.
class GaleryForm(forms.ModelForm):
    class Meta:
        model = Galery
        fields = ['image']


#model: модель, для якої буде створюватись форма (у цьому випадку - ChatMessage);
#fields: перелік полів моделі, які будуть включені до форми. У даному випадку форма буде містити тільки одне поле - body.
#widgets: словник, де ключ - це назва поля моделі, а значення - це об'єкт відповідного віджету для цього поля. У даному випадку, для поля body використовується віджет Textarea з атрибутами rows=5, що дозволить створити текстове поле з п'ятьма рядками.
#labels: словник, де ключ - це назва поля моделі, а значення - це мітка поля. У даному випадку мітка для поля body не визначена, тобто буде використовуватись стандартна мітка.
#help_texts: словник, де ключ - це назва поля моделі, а значення - це текст допомоги для поля.


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {
            'body': '',
        }
        help_texts = {
            'body': '',
        }


#Клас Meta містить вказівку на модель, яка буде використовуватись для створення форми, а саме - UserProfile.
# Крім того, вказані поля, які будуть відображені в формі - name та image.
#name та image - це поля форми, які містять об'єкти CharField та ImageField відповідно.
# CharField використовується для введення текстових даних, а ImageField - для завантаження зображення.
# Параметр required=False вказує, що поле image не є обов'язковим для заповнення.
#Метод __init__ встановлює атрибути для відображення полів форми на сторінці веб-сайту.
# Зокрема, атрибут class для поля name встановлюється як form-control, щоб забезпечити відображення поля у вигляді текстового поля з відповідним стилем.
# Атрибут label для поля image оновлюється для відображення тексту Фото профілю (змініть якщо потрібно) замість Profile Photo. Атрибут class для поля image також встановлюється як form-control-file, щоб забезпечити відображення поля у вигляді файлового поля з відповідним стилем.
class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'image']
        labels = {
            'name': 'Name',
            'image': 'Profile Photo (Change if needed)',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }





