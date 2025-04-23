from playwright.sync_api import sync_playwright

homepage = "https://www.chess.com/"
onlinePlay_test = "https://www.chess.com/play/online"


def playwright_structer():
    """ Inicializuje prohlížeč a stránku, vrací je jako objekty. """
    p = sync_playwright().start()
    prohlizec = p.chromium.launch(headless=True)
    stranka = prohlizec.new_page()
    return p, prohlizec, stranka


def test_nacteni_homepage():
    p, prohlizec, stranka = playwright_structer()

    # Navigace na stránku
    stranka.goto(homepage)

    # Ověření výsledků přes assert
    assert stranka.title() == "Chess.com - Play Chess Online - Free Games"

    # Uzavření prohlížeče
    prohlizec.close()
    p.stop()


def test_cookies_banner_display():
    p, prohlizec, stranka = playwright_structer()
    id_container = "#onetrust-group-container"

    stranka.goto(homepage)

    # Ověření, že cookies banner existuje
    stranka.locator(f"div{id_container}").wait_for(state="visible")
    assert stranka.locator(f"div{id_container}").is_visible(), "Cookies banner se nezobrazuje!"

    prohlizec.close()
    p.stop()


def test_logo_navigation():
    p, prohlizec, stranka = playwright_structer()

    # Přechod na jinou stránku než homepage
    stranka.goto(onlinePlay_test)
    stranka.wait_for_load_state("networkidle")
    current_url = stranka.url

    # Kliknutí na logo pro návrat na homepage
    logo_selektor = "#sb > div.nav-top-menu > a.nav-link-component.nav-link-main-design.chess-logo-wrapper.sprite.chess-logo.no-panel"
    logo = stranka.locator(logo_selektor)
    logo.click()

    # Ověření přesměrování
    stranka.wait_for_load_state("networkidle")

    assert stranka.url == homepage or stranka.url == homepage + "home", "Kliknutí na logo nepřesměrovalo na domovskou stránku"
    assert stranka.url != current_url, "URL se po kliknutí na logo nezměnila"

    prohlizec.close()
    p.stop()

