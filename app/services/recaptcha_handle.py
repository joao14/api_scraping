from time import sleep
from playwright.sync_api import Page
from app.core.config import settings

def handle_recaptcha_v2(page: Page):

    page.wait_for_selector(".g-recaptcha iframe")

    iframe_element = page.query_selector(".g-recaptcha iframe")

    recaptcha_frame = iframe_element.content_frame()
    
    if not recaptcha_frame:
        raise Exception("No se pudo obtener el iframe de ReCaptcha")
    
    recaptcha_frame.wait_for_selector(".recaptcha-checkbox-border")

    checkbox = recaptcha_frame.query_selector(".recaptcha-checkbox-border")
    if checkbox:
        checkbox.click()
    else:
        raise Exception("No se encontró el checkbox de ReCaptcha")
    
    sleep(7)

def handle_recaptcha_v3(page: Page):

    site_key = settings.RECAPTCHA_SITE_KEY

    if not site_key:
        raise ValueError("La clave del sitio de ReCaptcha no está configurada")
    
    token = page.evaluate(f"grecaptcha.execute('{site_key}', {{action: 'homepage'}})")

    return token