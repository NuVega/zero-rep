from django.http import HttpResponse


def home_view(request):
    return HttpResponse("""
        <h1>Добро пожаловать!</h1>
        <p><a href='/data'>Перейти на страницу /data</a></p>
        <p><a href='/test'>Перейти на страницу /test</a></p>
    """)


def data_view(request):
    return HttpResponse("""
        <h2>Страница Data</h2>
        <p>Здесь могли быть какие-то уникальные данные.</p>
        <p><a href='/'>Вернуться на главную</a></p>
        """)


def test_view(request):
    return HttpResponse("""
        <h2>Страница Test</h2>
        <p>Здесь могла быть ваша реклама</p>
        <p><a href='/'>Вернуться на главную</a></p>
        """)