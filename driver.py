import locators, time, os, csv
import pandas as pd
from locators import Locators as L
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import NoSuchElementException

class Driver(Chrome):
    def __init__(self, max_timeout = 15, minimized = False):
        self.max_timeout = max_timeout
        self.minimized = minimized
        self.cookies = True
        self.push = True
        self.options = Options()
        prefs = {"profile.default_content_settings.popups": 0,
                    "download.default_directory": L.DOWNLOAD_FOLDER, 
                    "directory_upgrade": True,
                    "profile.default_content_setting_values.notifications": 2, 
                    "profile.manage_default_content_settings.javascript": 2}
        self.options.add_experimental_option('prefs', prefs)
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--disable-extensions")
        super().__init__(L.DRIVER_PATH, options=self.options)
        if self.minimized: self.minimize_window()
    
    def login(self) -> None:
        # NAVEGAR PARA A PÁGINA DE LOGIN
        self.get(L.AUTH_URL)

        # ENCONTRAR OS ELEMENTOS DA PÁGINA
        self.check_cookies()
        email_login = self.wait_element(L.EMAIL_LOGIN)

        user, password = L._USER, L._PASS

        if email_login:
            email_login.click()
        

        email_box  = self.wait_element(L.EMAIL_BOX)
        passw_box = self.wait_element(L.PASSW_BOX)
        send_button =  self.wait_element(L.SUBMIT_BUT)
        
        # EXECUTAR CADEIA DE AÇÕES PARA COMPLETAR O LOGIN
        actions = ActionChains(self)
        actions.send_keys_to_element(email_box, user)
        actions.send_keys_to_element(passw_box, password)
        actions.click(send_button)
        actions.perform()

        # VERIFICAR SE A PÁGINA DE LOGIN ESTÁ ABERTA
        if (self.current_url == L.LOGIN_URL):
            print("\nFalha no Login.\n")
        else:
            print("\nLogin executado.\n")
    
    def wait_element(self, locator, timeout=-1, retry=True):
        ''' 
        Essa função espera até que o elemento passado por parâmetro
        esteja presente na tela.
        
        Args:
        :param element: elemento a ser encontrado
        :param timeout: tempo de espera em segundos
        :return: elemento encontrado
        '''
        if timeout < 0: timeout = self.max_timeout

        try:
            time.sleep(1)
            element = WebDriverWait(self, timeout)\
                .until(EC.presence_of_element_located(locator))
            return element
        
        except TimeoutException:
            if retry:
                print("Tempo limite atingido ao tentar encontrar o elemento na página. \
                Tentando novamente.\n")
                self.refresh()
                self.wait_element(locator, retry=False)
            else:
                print("Nao foi possível encontrar o elemento desejado @ ", locator)
                return None
        
        except NoSuchElementException:
            print("Elemento não encontrado na página.\n")
            return None
    
    def get_elements(self, locator):
        method, loc = locator
        try:
            elements = self.find_elements(method, loc)
            # print("\nElementos encotrados: ", len(elements))
        except:
            elements = None
            # print("\nElementos não foram encotrados.")
        
        return elements

    def get_cards_from_locators(self, n_cards=10):
        '''  Essa função retorna uma lista com os IDs das cartas. '''
        card_locators = locators.card_locators(n_cards)
        cards = [self.wait_element(c) for c in card_locators]
        ids = [self.get_id(c) for c in cards]
        return ids
    
    def get_id(self, element):
        ''' 
        Essa função retorna o ID do elemento passado por parâmetro.
        
        Args:
        :param element: elemento a ser encontrado
        :return: elemento encontrado
        '''
        try:
            href = element.get_attribute("href")
            href_ = href.split("/")
            card_id = href_[-1]
            return card_id
        except:
            print("Falha ao ler elemento.\n")

    def get_all_ids(self, url = L.BUILDINGS_URL_CUR) -> None:
        self.get(url)
        n_buildings = self.wait_element(L.N_BUILDINGS)
        if n_buildings:
            n_buildings = int(n_buildings.text)
            print(f"Imóveis encontrados: {n_buildings}\n")
        else:
            n_buildings = 0
        
        n_pages = self.wait_element(L.N_PAGES)
        if n_pages:
            n_pages = int(n_pages.text)
            print(f"Número de páginas: {n_pages}\n")
        else:
            n_pages = 2

        buildings_ids = set()
        for n in range(1, n_pages):
            print(f'Lendo página {n}/{n_pages}\n')    
            try:
                ids = self.get_cards_from_locators()
                buildings_ids.update(ids)

            except TimeoutException as ex:
                print("\nTimeout Exception: ", str(ex))
            
            finally:
                self.next_page()

        n_cards = n_buildings - len(buildings_ids)
        ids = self.get_cards_from_locators(n_cards)
        buildings_ids.update(ids)

        print("Leitura concluida. IDs coletados: ", len(buildings_ids))
        print(f'\n{buildings_ids}')
        self.save_ids(buildings_ids)
    
    def next_page(self) -> None:
        try:
            next_page_button = WebDriverWait(self, 5)\
                .until(EC.element_to_be_clickable(L.NEXT_PAGE_BUT))
            next_page_button.click()
        except ElementClickInterceptedException:
            self.check_cookies()
            self.next_page()
        except:
            self.check_push()
    
    def check_cookies(self) -> None:
        if self.cookies:
            try: 
                accept_cookies = WebDriverWait(self, self.max_timeout)\
                .until(EC.element_to_be_clickable(L.COOKIE_ACCEPT_BUT))
                accept_cookies.click()
                self.cookies = False
                print('\nCookies aceitos.\n')
            except:
                pass

    def check_push(self) -> None:
        if self.push:                    
            time.sleep(1)
            try:
                close_push = WebDriverWait(self, self.max_timeout)\
                    .until(EC.element_to_be_clickable(L.PUSH_ACCEPT))
                close_push.click()
                self.push = False
            except TimeoutException:
                close_push = WebDriverWait(self, 20)\
                    .until(EC.element_to_be_clickable(L.PUSH_DENY))
                if close_push:
                    close_push.click()
                    self.push = False  
            finally:
                if not self.push: 
                    self.close_popup_window(self.current_window_handle)
                    print("Pop-up fechado.")
    
    def check_marked_price(self) -> list:
        method, loc = L.MARKED_PRICE
        try:
            marked_price = self.find_elements(method, loc)
            result = [mkp.text for mkp in marked_price]
        except: 
            result = []
        
        return result
    
    def download_files(self, building_id, max_retries=10) -> dict:
        self.implicitly_wait(2)
        method, loc = L.LINK_FILES
        folderpath = L.DOWNLOAD_FOLDER  # Caminho para as pastas de downloads do navegador

        try:
            link_files = self.find_elements(method, loc)
            filenames = [f.text for f in link_files]
            id_folder = os.path.join(folderpath, building_id) # Caminho para o subpasta do imóvel
            print("Arquivos: ", filenames)
            print(f"Baixando {len(filenames)} arquivos encontrados para ID: {building_id}")
        
        except:
            print("\nNenhum download disponível.")
            return {"Pasta" : ''}
        
        if not os.path.isdir(id_folder):
            os.makedirs(id_folder)                                                                
            for file, name in zip(link_files, filenames):                    
                filepath = os.path.join(id_folder,
                                     f'{building_id}_{name}')  # Localização do arquivo final
                down_filepath = os.path.join(folderpath, name) # Nome do arquivo padrão na pasta de downloads

                if os.path.isfile(filepath):
                    print("/nArquivo já existe.")
                    continue

                n_files = len(os.listdir(folderpath))
                file.click()
                download_button = self.wait_element(L.DOWNLOAD_BUT)
                download_button.click()                 
                
                # Aguardando download ser concluído
                self.wait_download(folderpath, n_files)

                if os.path.exists(down_filepath):
                    os.rename(down_filepath, filepath)
                    print(f"nArquivo {name} salvo com sucesso.")

                exit_download = self.wait_element(L.EXIT_DOWNLOAD_BUT)
                exit_download.click()                           
        
        else:
            print(f"\nPasta já existe.")

        return {"Pasta" : id_folder}
    
    def wait_download(self, folder, n_files, max_retries=10) -> None:
        counter = 0
        i = 0
        while counter <= n_files:
            time.sleep(0.5)
            counter = len(os.listdir(folder))
            i += 1
            if i == max_retries: break

    def close_popup_window(self, parent):
        time.sleep(1)
        uselessWindows = self.window_handles
        try:
            for winId in uselessWindows:
                if winId != parent: 
                    self.switch_to.window(winId)
                    self.close()
                    self.switch_to.window(parent)
        except NoSuchWindowException:
            print('\nJanela ja fechada.')
            self.refresh()

    def load_ids(self, filename=L.IDS_FILE) -> list:
        assert os.path.isfile(L.IDS_FILE)
        with open(filename, 'r') as f:
            read = csv.reader(f, delimiter = ',')
            data = [r for r in read]
            print(f"Arquivo {filename} carregado com sucesso.\n")
            f.close()
            return data[0]
    
    def save_ids(self, ids, filename=L.IDS_FILE) -> None:
        assert not os.path.isfile(filename)	
        with open(filename, 'w') as f:
            write = csv.writer(f, delimiter = ',')
            ids = list(ids)
            write.writerow(ids)
            print(f"\nArquivo {filename} salvo com sucesso.")
            f.close()     

    def save_data(self, data, filename='dados_orulo2.xlsx') -> None:
        assert data
        df = pd.DataFrame(data)
        filepath = L.DATA_FOLDER + filename
        df.to_excel(filepath, index=False)
        print("\nArquivo salvo com sucesso.")