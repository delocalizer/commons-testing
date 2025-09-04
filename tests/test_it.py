def test_it(settings):
    assert settings.BASE_URL.startswith('https://')
