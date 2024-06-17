from fastapi import APIRouter, HTTPException
from app.models.url_item import URLItem
from app.services.recaptcha_handle import handle_recaptcha_v2, handle_recaptcha_v3
from playwright.sync_api import sync_playwright

router = APIRouter()

#Endpoint metodo POST
@router.post("/solve_recaptcha/")
def solve_recaptcha(url_item: URLItem):
    #Usamos playwright para ejecutar pruebas en navegadores:
    # a). Usamos sync_playwright en modo sincronico y se aseguran que los recursos se liberen correctamnete
    
    with sync_playwright() as p:
        # b). Lanza una nueva instancia del navegador Chromium (la base de Google Chrome)
        browser = p.chromium.launch(headless=False)
        # c). Abre una nueva pestaña o página en el navegador lanzado
        page = browser.new_page()
        # d). Navega en a la URL
        page.goto(url_item.url)
        print("Navegador")
        print(page.content())
        try:
            content = page.content()
            #switch para validar cuando usar recaptcha v2 o v3
            if "recaptcha-v2" in content or "recaptcha/api2" in content:
                handle_recaptcha_v2(page)
            elif "recaptcha-v3" in content or "recaptcha/api3" in content:
                token = handle_recaptcha_v3(page)
                return {"token": token}
            else:
                raise HTTPException(status_code=400, detail="No se encontró ReCaptcha en la página")
            
            content = page.content()
            return {"content": content}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            browser.close()