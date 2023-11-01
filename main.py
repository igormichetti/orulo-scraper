import re, os, time
from driver import Driver
from locators import Locators as L

def address_split(address_section, bid):
    if address_section:
        address_section = re.split(' , |\n', address_section)
        address_section = address_section[0:3]
        # print("\nFull list address section: ", address_section)
        names =  address_section[0].split(' - ')
        # print("\nNames: ", names)
        # print("\nNames Len: ", len(names))
        if len(names) == 2:
            name, developer = names
            step = ''
        elif len(names) == 3:
            name, step, developer = names
        else: 
            name, step, developer = [' '] * 3

        address_list = address_section[1].split(' - ')
        if len(address_list) == 2:
            address, city_state = address_list
            city, state = city_state.split('/')
        else:
            address = address_section[1]
            city, state = '', ''
        
        id_type = address_section[2].split(' - ')
        if len(id_type) > 0:
            btype = id_type[-1]
        else:
            btype = ''


        result_dict = {'ID' :  bid,
                        'Nome' : name,
                          'Fase' : step,
                            'Empresa' : developer,
                              'Endereço' : address,
                                'Cidade' : city,
                                  'Estado' : state,
                                    'Tipo' : btype}
    else:
        result_dict = {'ID': "",'Nome' : "", 'Fase' : "" ,
                        'Empresa' : "", 'Endereço' : "",
                          'Cidade' : "", 'Estado' : "",
                            'Tipo' : ""}
    assert (len(result_dict.keys()) == 8) #Dicionário com tamanho errado.
    return result_dict

def get_typology_cols() -> list:
    cols = driver.get_elements(L.TYPO_COLUMNS)
    cols_titles = [c.get_attribute("title") for c in cols[1:]] #type: ignore
    
    return ['Preço'] + cols_titles

def process_string_list(list_strings, mkp : list):
    trimmed = list_strings.split('\n')
    list_strings = [s for s in trimmed[1:-1] if "m²" not in s]
    
    if mkp:
        list_strings = [s for s in list_strings if s not in mkp]
    result = {}
    current_name = None
    current_values = []
    
    for item in list_strings:
        has_numbers = bool(re.search(r'\d', item))
        if not has_numbers:
            if current_name is not None:
                result[current_name] = current_values
                current_values = []
            current_name = item
        else:
            if item.startswith("R$"):
                current_values.append(item[3:])
            else:
                item_list = item.split()
                n = len(item_list)
                current_values.append(item_list)
    
    if current_name is not None:
        result[current_name] = current_values

    return flatten_dict_values(result)

def flatten_dict_values(input_dict):
    result_dict = {}
    for key, value in input_dict.items():
        flattened_values = []
        for item in value:
            if isinstance(item, list):
                flattened_values.extend(item)
            else:
                flattened_values.append(item)
        result_dict[key] = flattened_values

    for key, value in result_dict.items():
        result_dict[key] = to_chunk(value)

    return result_dict

def to_chunk(values) -> list:
    result = []
    cdict = ['Preço', 'Área Privativa', 'Quartos', 'Suítes', 'Vagas']                     
    cols = get_typology_cols()
    n = len(cols)
    chunked =  [values[i:i + n] for i in range(0, len(values), n)]
    for items in chunked:
        chunk_dict = {}
        for col, item in zip(cdict, items):
            if col in cols:
                chunk_dict[col] = item
            else:
                chunk_dict[col] = ''
            
        result.append(chunk_dict)
    
    return result

def info_dict(input_list):
    result_dict = {}
    if input_list:
        input_list = input_list.split('\n')
        for item in input_list:
            item_split = item.split(': ')
            if len(item_split) == 2:
                key = item_split[0]
                value = item_split[1]
                result_dict[key] = value
    else:
        result_dict = {'Estágio': '', 'Lançamento': '',
                        'Entrega': '', 'Total de unidades': '',
                          'Estoque': '', 'Unidades por andar': '',
                            'Número de andares': '', 'Atualizado em': ''}

    return result_dict

if __name__ == '__main__':
    driver = Driver()
    #assert os.path.isdir(L.DOWNLOAD_FOLDER)
    if not os.path.isfile(L.IDS_FILE):
       driver.login()
       driver.get_all_ids()
    
    ids = driver.load_ids()
    
    n_buildings = len(ids)
    buildings_url = [L.BUILDINGS_URL + '/' + i for i in ids]
    all_rows = []
    for n, i in enumerate(ids):
        url = L.BUILDINGS_URL + '/' + i
        driver.get(url)
        driver.implicitly_wait(2)
        print(f"\n-- Acessando a página: {n+1}/{n_buildings}\n")
        
        print(driver.current_url)
        
        # Checking for login redirect
        if L.AUTH_URL in driver.current_url:
            print("\nRealizando o login na conta...\n")
            # Check for banner, modals and pop-ups
            driver.login()
            time.sleep(2)
            if driver.current_url in L.AUTH_URL:
                driver.login()
                driver.get(url)
        
        if driver.push:
            driver.check_push()

        # Getting name and address of current building
        address = driver.wait_element(L.ADDRESS_SECT)
        if address:
            address_dict = address_split(address.text, i)
        else: address_dict = address_split(None, i)
        #print("\n- Address:", address_dict)

        # Getting type, price and size info of current building
        cols = get_typology_cols()
        typologies_info = driver.wait_element(L.INFO_TYPO)
        marked_price = driver.check_marked_price()
        if typologies_info and cols:
            typologies_info = typologies_info.text
            typologies_dict = process_string_list(typologies_info, marked_price)
        else: typologies_dict = {"NaN" : [dict(zip(cols, [""]*len(cols)))]}
        #print("\n- Typologies:", typologies_dict)

        # Getting comission value of current building
        commission_value = driver.get_elements(L.COMISION_VAL)
        if commission_value:
            commission_value = commission_value[0].text[:-1]
            commission_value_dict = {"Comissão" : commission_value}
        else: 
            commission_value_dict = {"Comissão" : ""}
        #print("\n- Comission: ", commission_value)

        # Getting more info of current building
        more_info = driver.wait_element(L.MORE_INFO, retry=False)
        if more_info:
            more_info = more_info.text
            more_info_dict = info_dict(more_info)
        else: more_info_dict = info_dict(None)
        #print("\n- Mais Informações: ", more_info_dict)

        ## Downloading available building files
        # filepaths = driver.download_files(i)
        # print("\n- Arquivos: ", more_info_dict)

        # Writting rows for each distinct typology element
        row = {**address_dict, **more_info_dict, **commission_value_dict}
        kys = []
        for tname, tinfo in typologies_dict.items():
            for info in tinfo:
                irow = row.copy()
                irow["Tipologia"] = tname
                print("\ninfo", info)
                irow.update(info)
                #irow.update(filepaths)
                for ky in irow:
                    if ky not in kys:
                        kys.append(ky)
                        print(kys)
                all_rows.append(irow)
    
    print(kys)
    print("/nTamanho de cada linha: ", [len(row) for row in all_rows])      
    driver.save_data(all_rows) 
    driver.quit()












