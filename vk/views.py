import json
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from .forms import *
from django.http import JsonResponse
from .models import UserProfile,Galery,Friend,News
from django.contrib.auth.decorators import login_required


#фунція для виходу з стандартої бібліотеки
def Logout(request):
    logout(request)
    return redirect('login')
#Спочатку функція перевіряє, чи є вхідний запит POST-запитом, використовуючи request.method. Якщо це так, функція витягує значення username, password1, password2 та email з POST-даних запиту за допомогою request.POST.get().
#Потім функція створює новий об'єкт користувача за допомогою вбудованого в Django методу create_user() моделі User.
# Цей метод приймає три параметри: ім'я користувача, email та пароль. Функція передає витягнуті змінні uname, email і pass1 до цього методу для створення нового об'єкта користувача, який потім зберігається в базі даних за допомогою методу save().
#Нарешті, функція повертає HTTP-відповідь перенаправлення за допомогою функції redirect(), спрямовуючи користувача на сторінку входу в систему.
# Якщо вхідний запит не є POST-запитом, функція рендерить шаблон vk/register.html за допомогою функції render().
def Singup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')

        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        email = request.POST.get('email')

        my_user = User.objects.create_user(uname,email,pass1)
        my_user.save()
        return redirect('login')

    return render(request, 'vk/register.html')

#Функція отримує в якості параметра об'єкт запиту, який є об'єктом HttpRequest, що містить інформацію про поточний запит від клієнта.
#Спочатку функція перевіряє, чи метод запиту є 'POST', що означає, що форма була надіслана з обліковими даними для входу.
# Якщо це не 'POST', функція просто відображає шаблон 'vk/login.html'.
#Якщо метод запиту 'POST', функція отримує ім'я користувача та пароль з даних форми за допомогою методу request.POST.get().
# Потім вона викликає метод authenticate(), наданий Django, передаючи змінні ім'я користувача та пароль як аргументи.
# Якщо об'єкт користувача, що повертається методом authenticate(), не дорівнює None, це означає, що користувач надав дійсні облікові дані для входу і його автентифіковано.
#Потім функція викликає метод login(), наданий Django, передаючи запит і об'єкти користувача як аргументи для входу користувача.
# Нарешті, функція перевіряє, чи має автентифікований користувач атрибут користувача (чи профіль вже створено) і перенаправляє користувача на відповідну сторінку: "головну" для звичайних користувачів або "профіль" для користувачів які створили профіль.
#Якщо об'єкт користувача, що повертається функцією authenticate(), дорівнює None, функція нічого не робить (на це вказує інструкція pass) і продовжує рендеринг шаблону 'vk/login.html'.

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            if hasattr(user, 'user'):
                return redirect('main')
            else:
                return redirect('profile')
        else:
            pass

    return render (request,'vk/login.html')


#Ця функція відповідає за обробку запитів на завантаження зображення на сайт.
# Основна логіка функції полягає в перевірці того, що запит є запитом методу POST, що означає, що на сервер надійшла форма з даними.
#Якщо запит є запитом методу POST, то відбувається валідація даних, що надійшли з форми.
# Якщо дані вірні, то створюється новий екземпляр моделі "Galery", який є моделлю для зображень у галереї на сайті.
# При створенні екземпляру не відбувається збереження в базі даних, що забезпечує більш гнучкий підхід до зберігання даних.
# Далі до об'єкту "Galery" додається властивість "user", що містить інформацію про користувача, який завантажив зображення.
# Після цього об'єкт зберігається в базі даних і користувач перенаправляється на головну сторінку сайту.
#Якщо запит не є запитом методу POST, тобто це запит методу GET, то створюється новий екземпляр форми "GaleryForm" і відбувається рендеринг сторінки "upload_image.html" зі створеною формою.
#Форма відображається на сторінці, де користувач може заповнити її та завантажити зображення.
#У кінці функція повертає відображення з формою, щоб користувач міг заповнити її.

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = GaleryForm(request.POST, request.FILES)
        if form.is_valid():
            galery = form.save(commit=False)
            galery.user = request.user
            galery.save()
            return redirect('main')
    else:
        form = GaleryForm()
    return render(request, 'vk/upload_image.html', {'form': form})

#Функція отримує на вхід об'єкт запиту і перевіряє метод запиту, щоб визначити, чи це GET або POST запит.
#Якщо метод запиту POST, функція створює новий екземпляр UserProfileForm з переданими даними і файлами.
#Якщо форма є дійсною, вона зберігає дані форми в базі даних, створюючи новий об'єкт профілю і встановлюючи в полі User значення поточного користувача, а потім перенаправляє на головну сторінку.
#Якщо метод запиту не POST, функція створює новий порожній екземпляр UserProfileForm і рендерить шаблон 'create_profile.html' з об'єктом форми.
#Це дозволяє користувачеві заповнити форму і відправити її для створення нового профілю.
def createProfile(request):
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                return redirect('main')
        else:
            form = UserProfileForm()
        return render(request, 'vk/create_profile.html', {'form': form})
#Декоратор `@login_required` - це декоратор Django, який гарантує, що лише авторизовані користувачі можуть отримати доступ до подання.
#Якщо користувач не автентифікований, його буде перенаправлено на сторінку входу (як визначено в аргументі `login_url`).
#Функція отримує об'єкт `request` як аргумент, який є об'єктом Django `HttpRequest`, що представляє вхідний запит від браузера користувача.
#Функція починає роботу з отримання профілю користувача і всіх зображень, що належать цьому користувачеві, з моделі `Galery`.
# Вона також створює або отримує об'єкт `Friend` для користувача і отримує всіх користувачів зі списку друзів.
#Потім функція створює словник `context`, що містить об'єкти `profile`, `images` і `friends`, які передаються до шаблону `main.html` для рендерингу.
#Нарешті, функція повертає об'єкт `HttpResponse`, сформований за допомогою шаблону `main.html` і словника `context`.

@login_required(login_url='login')
def main(request):
    profile = request.user.user
    images = Galery.objects.filter(user_id=request.user.id)
    friend, _ = Friend.objects.get_or_create(c_user=request.user)
    friends = friend.users.all()

    context = {
        'profile': profile,
        'images': images,
        'friends': friends,

    }
    return render(request, 'vk/main.html', context=context)


#Це функція перегляду у веб-додатку Django, яка відображає список користувачів.
# Вона вимагає, щоб користувач був зареєстрований для доступу до сторінки, як зазначено в декораторі `@login_required`.
#У функції профіль користувача отримується з об'єкта `request`, який передається в представлення як аргумент.
#Змінна `users` встановлюється в значення набору запитів всіх об'єктів `UserProfile`, за винятком користувача, який на даний момент увійшов в систему.
#Модель `Friend` використовується для відстеження друзів користувача, і змінна `friends` встановлюється як набір запитів до друзів поточного користувача.
#Якщо користувач не має друзів, змінній `friends` присвоюється порожній список.
#Словник `friend_status` створюється для зберігання статусу дружби користувача, що увійшов до системи, з кожним користувачем у запиті `users`.
#Ключами словника є ідентифікатори користувачів, а значеннями - булеві значення, що вказують на те, чи є користувач другом користувача, який увійшов до системи.
#Список словників з назвою `user_data` створюється для зберігання даних, які будуть відображатися для кожного користувача у наборі запитів `users`.
# Для кожного користувача словник містить інформацію про профіль користувача (`user`), його статус дружби (`is_friend`) та ім'я (`name`).
#Нарешті, змінні `user_data` і `profile` передаються до функції `render` разом з файлом шаблону для відображення (`vk/user_list.html`).


@login_required
def user_list(request):
    profile = request.user.user
    users = UserProfile.objects.exclude(id=request.user.user.id)
    try:
        friend = Friend.objects.get(c_user=request.user)
        friends = friend.users.all()
    except Friend.DoesNotExist:
        friends = []


    friend_status = {}
    for f in friends:
        if f != request.user:

            friend_status[f.id] = True


    user_data = []
    for user in users:
        user_data.append({
            'user': user,
            'is_friend': friend_status.get(user.user.id, False),
            'name': user.name,

        })

    return render(request, 'vk/user_list.html', {'users': user_data,'profile':profile})


#Це функція перегляду, яка дозволяє користувачеві додавати або видаляти друзів зі свого списку друзів.
#Функція перегляду приймає три параметри: об'єкт `request`, рядок `operation` і ціле число `pk`.
#Параметр `operation` може мати значення `add` або `remove`, вказуючи на те, чи користувач хоче додати або видалити друга.
#Параметр `pk` є первинним ключем профілю користувача, який додається або видаляється.
#Спочатку функція отримує профіль користувача друга за допомогою функції швидкого доступу `get_object_or_404`, яка видає помилку 404, якщо об'єкт не знайдено.
#Залежно від значення параметра `operation` викликаються методи `Friend.make_frien()` або `Friend.lose_frien()` для додавання або видалення друга зі списку друзів користувача.
#Ці методи оновлюють модель `Friend` у базі даних.
#Нарешті, функція перенаправляє користувача на URL-адресу `'list'` за допомогою функції перенаправлення `redirect()`.

def change_friend(request, operation, pk):
    friend = get_object_or_404(UserProfile, pk=pk).user
    if operation == 'add':
        Friend.make_friend(request.user, friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return redirect('list')


#Функція приймає POST-запит, який містить текст новини і необов'язкове зображення.
#Якщо надано і текст, і зображення, функція створює новий об'єкт `News` з даними про текст і зображення, а також про `користувача`, який опублікував новину, і зберігає його в базі даних.
#Нарешті, користувач буде перенаправлений на головну сторінку програми.
#Якщо метод запиту не POST, функція відображає шаблон для публікації новини, де користувач може ввести текст новини і вибрати зображення.
@login_required
def news_publish(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        image = request.FILES.get('image')
        if text or image:
            news = News(text=text, image=image, user=request.user)
            news.save()
            return redirect('main')
    return render(request, 'vk/news_publish.html')


#відповідає за відображення сторінки стрічки новин для користувача, що увійшов до системи.
#По-перше, декоратор @login_required гарантує, що тільки авторизовані користувачі можуть отримати доступ до цієї сторінки.
#Якщо користувач не автентифікований, він буде перенаправлений на сторінку входу.
#Потім функція отримує профіль поточного користувача і список його друзів з моделі Друг.
# Потім вона використовує метод filter(), щоб отримати всі новини, створені друзями користувача, відсортовані за полем created_at у порядку спадання.
#Нарешті, контекстний словник заповнюється новинами та профілем користувача і передається до шаблону news_feed.html для відображення сторінки.
@login_required
def news_feed(request):
    profile = request.user.user
    friends = Friend.objects.get(c_user=request.user).users.all()
    news_list = News.objects.filter(user__in=friends).order_by('-created_at')

    context = {'news_list': news_list,'profile':profile}
    return render(request, 'vk/news_feed.html', context)

#Це функція яка відображає галерею користувача. Спочатку функція перевіряє, чи користувач автентифікований за допомогою декоратора `@login_required`.
#Якщо користувач автентифікований, функція отримує профіль користувача та його зображення з моделі `Galery`.
#Якщо метод запиту POST, функція створює об'єкт `GaleryForm` з даними із запиту і перевіряє його.
#Якщо форма дійсна, функція створює новий об'єкт `Galery` з ідентифікатором користувача та даними з форми і зберігає його в базі даних.
#Нарешті, функція перенаправляє користувача на головну сторінку.
#Якщо метод запиту не POST, функція створює порожній об'єкт `GaleryForm`.
#Потім функція рендерить шаблон `user_gallery.html` з отриманими зображеннями, об'єктом форми і профілем користувача в якості контексту.

@login_required
def user_gallery(request):
    profile = request.user.user
    images = Galery.objects.filter(user=request.user)
    if request.method == 'POST':
        form = GaleryForm(request.POST, request.FILES)
        if form.is_valid():
            galery = form.save(commit=False)
            galery.user = request.user
            galery.save()
            return redirect('main')
    else:
        form = GaleryForm()
    context = {'images': images, 'form': form,'profile':profile}
    return render(request, 'vk/user_gallery.html', context)


#Функція приймає два аргументи: об'єкт запиту і параметр `news_id`, який є первинним ключем новини, яку користувач хоче вподобати.
#Спочатку функція отримує профіль аутентифікованого користувача (`request.user.user`) і новину із зазначеним `news_id` за допомогою функції `get_object_or_404`, яка повертає сторінку помилки 404, якщо новина не існує.
#Якщо метод запиту POST (тобто користувач заповнив форму, щоб поставити лайк або не поставити лайк допису), функція перевіряє, чи поставив користувач лайк допису, чи ні.
#Якщо користувач вже вподобав новину, функція видаляє його вподобання з цієї новини. Якщо користувач не вподобав публікацію, функція додає його лайк до публікації.
#Нарешті, функція перенаправляє користувача на URL-адресу "всі", яка, найімовірніше, є сторінкою, що відображає всі новини.
@login_required
def like_news(request, news_id):
    profile = request.user.user
    news = get_object_or_404(News, pk=news_id)
    if request.method == 'POST':
        if request.user in news.likes.all():
            news.likes.remove(request.user)
        else:
            news.likes.add(request.user)
    return redirect('all')


#Функція отримує об'єкт `request` та `recipient_id` як параметри.
#Спочатку функція отримує об'єкт `UserProfile` користувача, який увійшов до системи за допомогою `request.user.user`.
#Потім вона отримує об'єкт `UserProfile` одержувача за допомогою параметра `recipient_id`.
#Далі функція створює екземпляр `ChatMessageForm`, отримує всі об'єкти `ChatMessage` і перевіряє, чи метод `request` є `POST`.
#Якщо це так, вона створює новий екземпляр `ChatMessage` з даними форми, встановлює поля відправника і одержувача, зберігає повідомлення і перенаправляє на ту ж сторінку з оновленою історією чату.
#Нарешті, функція рендерить шаблон `send.html` зі словниковим контекстом, що містить одержувача, форму, відправника, чати та об'єкти профілю.

@login_required
def message(request, recipient_id):
    profile = request.user.user
    recipient = UserProfile.objects.get(pk=recipient_id)
    sender = request.user.user
    form = ChatMessageForm()
    chats = ChatMessage.objects.all()
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.msg_sender = sender
            message.msg_reciver = recipient
            message.save()
            return redirect('message', recipient_id=recipient_id)
    context = {'recipient': recipient, 'form': form,'sender':sender,'recipient':recipient,
               'chats':chats,'profile':profile}
    return render(request, 'vk/send.html', context)


#Це функція подання Django, яка обробляє POST-запит на відправку повідомлення чату одержувачу.
#Спочатку вона перевіряє, чи користувач автентифікований за допомогою декоратора `@login_required`.
# Якщо користувач не автентифікований, його буде перенаправлено на сторінку входу.
#Ідентифікатор одержувача передається як аргумент в URL-адресі.
#Потім функція завантажує дані з тіла запиту як JSON-об'єкт за допомогою `json.loads()`.
#Функція отримує профілі відправника і одержувача з бази даних за допомогою `request.user` і моделі `UserProfile`.
#Вміст повідомлення витягується з даних JSON і створюється нове повідомлення чату за допомогою моделі `ChatMessage`.
#Функція повертає відповідь у форматі JSON, що містить тіло повідомлення чату у вигляді рядка. До функції `JsonResponse` додано `safe=False`, щоб дозволити серіалізацію об'єктів, відмінних від диктів або списків.
@login_required
def sendMessages(request,recipient_id):
    data = json.loads(request.body)
    sender = request.user.user
    recipient = UserProfile.objects.get(pk=recipient_id)
    new_chat = data['msg']
    new_chat_message = ChatMessage.objects.create(body=new_chat,msg_sender=sender,msg_reciver=recipient)

    return JsonResponse(new_chat_message.body,safe=False)


#Функція отримує два параметри - об'єкт `request` та `recipient_id`, який є первинним ключем профілю користувача одержувача повідомлення.
#Спочатку функція отримує профіль відправника за допомогою `request.user.user`, де `request.user` - це об'єкт користувача, який у даний момент увійшов до системи.
#Потім вона отримує об'єкт профілю користувача одержувача за допомогою методу `UserProfile.objects.get()` з параметром `recipient_id`.
#Потім функція створює порожній список з ім'ям `arr` і використовує модель `ChatMessage` для фільтрації повідомлень, де `msg_sender` є одержувачем, а `msg_reciver` - відправником.
#Потім вона перебирає відфільтровані чати і додає тіло кожного повідомлення до списку `arr`.
#Нарешті, функція повертає об'єкт `JsonResponse` з рядком 'work' в якості першого параметра і `save=False` для запобігання серіалізації JsonResponse.
#Ця відповідь буде надіслана назад на клієнтську сторону, щоб показати, що функція працює правильно.
#Однак вона не містить вмісту повідомлення.
@login_required
def receiveMessages(request,recipient_id):
    sender = request.user.user
    recipient = UserProfile.objects.get(pk=recipient_id)
    arr = []
    chats = ChatMessage.objects.filter(msg_sender=recipient,msg_reciver=sender)
    for chat in chats:
        arr.append(chat.body)
    return JsonResponse('work',save=False)

#Спочатку використовується декоратор "@login_required", щоб гарантувати, що тільки авторизовані користувачі можуть отримати доступ до цього подання.
#Потім функція отримує профіль користувача за допомогою атрибута "request.user.user", припускаючи, що профіль користувача пов'язаний з вбудованою моделлю користувача.
#Потім функція отримує об'єкт Друг, пов'язаний з користувачем, який містить список друзів як пов'язане поле.
# Список друзів передається до шаблону разом з профілем користувача, і створюється шаблон "friend_list.html".


@login_required
def friend_user_list(request):
    profile = request.user.user
    friend = Friend.objects.get(c_user=request.user)
    friends = friend.users.all()
    return  render(request, 'vk/friend_list.html', {'friends':friends,'profile':profile})



#Функція отримує об'єкт профілю поточного користувача та об'єкт профілю користувача за допомогою моделі `UserProfile` і створює екземпляр форми `UserEditForm` з об'єктом профілю користувача у якості екземпляра.
#Потім функція перевіряє, чи форма є дійсною.
#Якщо форма дійсна, інформація профілю користувача оновлюється, а користувач перенаправляється на головну сторінку.
#Якщо форма не є дійсною, користувачеві буде показано сторінку профілю з формою для редагування інформації.
#Контекст, що передається функції `render()`, включає об'єкт `form`, який використовується для відображення форми користувачеві, і об'єкт `profile`, який містить інформацію про поточний профіль користувача.
@login_required
def edit_profile(request):
    profile = request.user.user
    user_profile = UserProfile.objects.get(user=request.user)
    form = UserEditForm(request.POST or None, request.FILES or None, instance=user_profile)
    if form.is_valid():
        form.save()
        return redirect('main')
    return render(request, 'vk/profile.html', {'form': form,'profile':profile})

#Функція отримує два аргументи: об'єкт `request` і `message_id` - ідентифікатор повідомлення, яке користувач хоче відредагувати.
#У тілі функції код спочатку отримує об'єкт повідомлення чату з заданим ідентифікатором за допомогою методу `ChatMessage.objects.get()`.
#Потім він перевіряє метод запиту, щоб визначити, чи намагається користувач надіслати форму з оновленими даними повідомлення, чи він просто запитує сторінку.
#Якщо метод запиту `POST`, код створює об'єкт `ChatMessageForm` з оновленими даними повідомлення і перевіряє валідність форми за допомогою методу `is_valid()`.
# Якщо форма валідна, вона зберігає оновлене повідомлення в базі даних за допомогою методу `form.save()` і перенаправляє користувача на сторінку повідомлення чату для одержувача повідомлення.
#Якщо метод запиту не є `POST`, код створює об'єкт `ChatMessageForm` з даними поточного повідомлення і відображає шаблон `edit_message.html` з формою в якості контекстної змінної.
#Словник `context` містить лише одну пару ключ-значення: `'form': form`. Це робить об'єкт `form` доступним у шаблоні як змінна з назвою `form`.
@login_required
def edit_message(request, message_id):
    message = ChatMessage.objects.get(id=message_id)
    if request.method == 'POST':
        form = ChatMessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('message', recipient_id=message.msg_reciver.id)
    else:
        form = ChatMessageForm(instance=message)
    context = {'form': form}
    return render(request, 'vk/edit_message.html', context)


#Функція отримує два аргументи: `request` та `message_id`.
# Аргумент `request` є екземпляром класу `HttpRequest`, який містить інформацію про поточний запит, що обробляється. Аргумент `message_id` - це ідентифікатор повідомлення, яке потрібно видалити.
#Функція отримує повідомлення чату з заданим ID за допомогою `ChatMessage.objects.get(id=message_id)` і присвоює його змінній `message`.
#Також отримується ідентифікатор отримувача повідомлення і зберігається у змінній `recipient_id`.
#Потім викликається метод `delete()` для об'єкта `message`, щоб видалити його з бази даних.
#Нарешті, функція перенаправляє користувача до подання `message` для одержувача видаленого повідомлення за допомогою `redirect('message', recipient_id=recipient_id)`.
@login_required
def delete_message(request, message_id):
    message = ChatMessage.objects.get(id=message_id)
    recipient_id = message.msg_reciver.id
    message.delete()
    return redirect('message', recipient_id=recipient_id)




