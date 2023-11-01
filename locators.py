from selenium.webdriver.common.by import By

class Locators:
    # --- Login Page Element Locations ---
    EMAIL_BOX = (By.ID, "email") 
    PASSW_BOX = (By.ID, "password")
    SUBMIT_BUT = (By.XPATH, "/html/body/section/div/form/button")
    EMAIL_LOGIN = (By.XPATH, "/html/body/section/div/button[3]")

    # --- Product Info Element Locations ---
    ADDRESS_SECT = (By.XPATH, '//*[@id="show-buildings"]/div[3]')
    TYPOLOGIES_SECT = (By.ID, "typologies-section")
    TYPO_COLUMNS = (By.XPATH, '//*[@id="info_typologies"]/table/thead/tr/th')
    TYPO_NAMES = (By.CSS_SELECTOR, "p[class$='iJnpzz']")
    INFO_TYPO = (By.ID, "info_typologies")
    TABLE_TYPO = (By.CSS_SELECTOR, "[class$='guLmaw']")
    MARKED_PRICE = (By.CSS_SELECTOR, "[class$='gxukQz']")
    SECT_TABLE = (By.TAG_NAME, 'table')
    COMISION_VAL = (By.CSS_SELECTOR, "span[class$='ggXOVs']")
    MORE_INFO = (By.XPATH, '//*[@id="left_column"]/fieldset[2]/div[2]')
    LINK_FILES = (By.CSS_SELECTOR, "a[class$='link-files']")
    DOWNLOAD_BUT = (By.XPATH, '//*[@id="headerDocument"]/div/div[2]/button[1]')
    EXIT_DOWNLOAD_BUT = (By.XPATH, '//*[@id="headerDocument"]/div/div[1]/button')

    # --- Products Listing Element Locations ---
    N_BUILDINGS = (By.XPATH, '//*[@id="intro_step2"]/fieldset/div/div[1]/b[2]')
    N_PAGES = (By.XPATH, '//*[@id="properties_list_page"]/div/fieldset/div/ul/li[9]/a')
    NEXT_PAGE_BUT = (By.CSS_SELECTOR, "a[class='next-page-button']")
    CARDS_IN_PAGE = (By.XPATH, '//*[@id="intro_step2"]/fieldset/div/div[1]/b[1]')
    BUILDINGS_LIST = (By.XPATH, '//*[@id="properties_list_page"]/div')
    CARD_XPATH = '(By.XPATH, //*[@id="properties_list_page"]/div/div[{c}]/a)'
    
    # --- Modals and Cookies Elements Locations ---
    PUSH_MODAL = (By.CLASS_NAME, 'pushModal active')
    PUSH_DENY = (By.CSS_SELECTOR, 'a[@id = "pushActionRefuse"]')
    PUSH_ACCEPT = (By.ID, 'pushConfirmation')
    COOKIE_BANNER = (By.ID, 'CookieBanner')
    COOKIE_ACCEPT_BUT = (By.CLASS_NAME, 'cookiebanner__buttons__deny')
    
    # --- Web Driver Path and URLs  ---
    DRIVER_PATH = r'C:\Users\miche\.wdm\drivers\chromedriver\win64\116.0.5845.188\chromedriver.exe' ## INSERT THE PATH OS YOUR CHROMEDRIVER 
    DOWNLOAD_FOLDER = r'C:\Users\miche\OneDrive\Documentos\Projetos\orulo-scraper\driver_downloads'
    DATA_FOLDER = 'driver_data/'
    IDS_FILE = DATA_FOLDER + 'ids.csv'
    _USER =  'your@email.com'## ORULO USER 
    _PASS =  'your password'## ORULO PASSWORD 
    AUTH_URL = 'https://auth.orulo.com.br/'
    BASE_URL = 'https://www.orulo.com.br'
    LOGIN_URL = BASE_URL + "/login"
    SIGNIN_URL = BASE_URL + "/customers/sign_in"
    BUILDINGS_URL = 'https://www.orulo.com.br/buildings'
    BUILDINGS_URL_CUR = BUILDINGS_URL + '?map_sw_lat=-26.146481085879522&map_sw_lng=-50.29376965382065&map_ne_lat=-24.889227182699656&map_ne_lng=-48.19707967900325&page=1&sort=building_name&order=asc'

def card_locators(_ncards):
    cards = []
    card_xpath = '//*[@id="properties_list_page"]/div/div[{c}]/a'
    for n in range(2, _ncards + 2):
        cards.append((By.XPATH, card_xpath.format(c=n)))
    return cards


