from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user') #user: Це поле є OneToOneField, яке пов'язує модель UserProfile з вбудованою моделлю Django User. Воно створює відношення один-до-одного між екземпляром UserProfile та екземпляром User. Атрибут on_delete визначає, що відбувається, коли пов'язаний екземпляр User видаляється. У цьому випадку екземпляр UserProfile також буде видалено. Атрибут related_name дозволяє вказати ім'я для зворотного зв'язку від User до UserProfile.
    name = models.CharField(max_length=50)#Це поле є CharField, в якому зберігається ім'я користувача.
    age = models.IntegerField(default=0)
    telephone_number = models.CharField(max_length=20, unique=True)#Це поле є CharField, яке зберігає номер телефону користувача. Воно має атрибут unique=True, що означає, що кожен номер телефону може бути пов'язаний лише з одним користувачем.
    image = models.ImageField(upload_to='user_profile_images', blank=True,null=True)#Це поле є ImageField, в якому зберігається зображення профілю користувача. Атрибут upload_to вказує директорію, куди будуть зберігатися завантажені зображення.
    friends = models.ManyToManyField(User,blank=True)#Це поле є полем типу ManyToManyField, яке створює зв'язок "багато-до-багатьох" між екземплярами користувачів. Воно дозволяє користувачам мати декілька друзів і представлене у вигляді набору екземплярів користувачів.

    def __str__(self):
        return self.name #метод, який повертає ім'я користувача, коли екземпляр моделі перетворюється у рядок. Цей метод використовується Django для відображення читабельних представлень екземплярів моделі в адмінці Django та інших контекстах.



class Galery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)#зовнішній ключ до моделі User, що вказує на користувача, який створив цей запис галереї. Це означає, що кожен запис галереї пов'язаний з одним користувачем з моделі User. Якщо користувач видаляється, всі його записи галереї також видаляються завдяки параметру on_delete=models.CASCADE.
    image = models.ImageField(upload_to='user_galery_images', blank=True)#поле типу ImageField, яке дозволяє завантажувати фотографії в галерею. Це поле використовується для збереження шляху до зображення у серверній файловій системі після завантаження користувачем. Параметр upload_to вказує на шлях, де зберігати завантажені фотографії відносно шляху MEDIA_ROOT у файловій системі Django.




class Friend(models.Model):
    users = models.ManyToManyField(User)#Це поле ManyToManyField, яке створює зв'язок "багато-до-багатьох" між моделями "Друг" і "Користувач". Це дозволяє асоціювати декількох користувачів з одним екземпляром "Друг" і навпаки.
    c_user = models.ForeignKey(User,related_name='owner',on_delete=models.CASCADE,null=True)#This is a ForeignKey that creates a one-to-many relationship between "Friend" and "User" models. It specifies that one "Friend" instance can only be associated with one "User" instance, while one "User" instance can be associated with multiple "Friend" instances. The "related_name" attribute specifies the name of the reverse relation from the "User" model to the "Friend" model.

    @classmethod
    def make_friend(cls, c_user, n_friend):
        friend, created = cls.objects.get_or_create(
            c_user=c_user,
            defaults={'c_user': c_user},
        )
        friend.users.add(n_friend)
#Цей метод створює новий екземпляр "Друг" або отримує існуючий і додає нового користувача до його поля "користувачі".
# Метод отримує два аргументи: "c_user" (екземпляр моделі "Користувач", який представляє власника екземпляра "Друг") і "n_friend" (екземпляр моделі "Користувач", який представляє нового друга, що додається).
    @classmethod
    def lose_friend(cls, c_user, n_friend):
        friend = cls.objects.get(c_user=c_user)
        friend.users.remove(n_friend)
#Цей метод знаходить існуючий екземпляр "Друг" і видаляє користувача з його поля "користувачі". Метод отримує два аргументи: "c_user" (екземпляр моделі "Користувач", який представляє власника екземпляра "Друг") і "n_friend"
# (екземпляр моделі "Користувач", який представляє друга, що видаляється).


class News(models.Model):
    text = models.TextField()#текст новини, зберігається як TextField.
    image = models.ImageField(upload_to='news_images', blank=True,null=True)#зображення, яке може бути додано до новини, зберігається як ImageField. Якщо зображення не додано, то поле може залишатися порожнім (blank=True) або мати значення null (null=True).
    user = models.ForeignKey(User, on_delete=models.CASCADE)#зв'язок з моделлю User з Django, що відповідає за зберігання користувачів. Кожна новина пов'язана з користувачем, який її створив, за допомогою поля ForeignKey. Якщо користувач видаляється, то всі повідомлення, пов'язані з ним, також видаляються (опція on_delete=models.CASCADE).
    created_at = models.DateTimeField(auto_now_add=True)#дата та час створення новини, зберігається як DateTimeField з параметром auto_now_add=True, що автоматично заповнює поле значенням поточної дати та часу при створенні нового об'єкту.
    likes = models.ManyToManyField(User, related_name='blogpost_like')#зв'язок з моделлю User з Django, що відповідає за зберігання користувачів. Це поле є зв'язком багато до багатьох (ManyToManyField) між моделлю News та User, тобто кожен користувач може лайкати багато новин, а кожна новина може мати багато лайків. Для полегшення доступу до користувачів, які вподобали певну новину, використовується параметр related_name, який встановлює ім'я, за яким можна отримати доступ до користувачів, що лайкнули новину.

    def number_of_likes(self):
        return self.likes.count() #повертає кількість лайків, що були поставлені на цю новину.



class ChatMessage(models.Model):
    body = models.TextField()#текст повідомлення. Це поле зберігає вміст повідомлення, яке було введено користувачем.
    msg_sender = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='msg_sender')#зберігає інформацію про користувача, який створив повідомлення. Це зовнішній ключ на модель UserProfile, яка зберігає додаткову інформацію про користувача.
    msg_reciver = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='msg_reciver')#зберігає інформацію про користувача, якому адресоване повідомлення. Це також зовнішній ключ на модель UserProfile.


    def __str__(self):
        return  self.body #повертає текст повідомлення, коли модель представляється у вигляді рядка.







