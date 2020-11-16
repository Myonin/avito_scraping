from selenium import webdriver
from tqdm import tqdm
import pandas as pd


def parser_phone(DIR_DATA, NAME_JSON, NAME_DF):

    regions = [
        'https://www.avito.ru/belgorodskaya_oblast/telefony?cd={}',
        'https://www.avito.ru/bryanskaya_oblast/telefony?cd={}',
        'https://www.avito.ru/vladimirskaya_oblast/telefony?cd={}',
        'https://www.avito.ru/voronezhskaya_oblast/telefony?cd={}',
        'https://www.avito.ru/ivanovskaya_oblast/telefony?cd={}',
        'https://www.avito.ru/kaluzhskaya_oblast/telefony?cd={}',
        'https://www.avito.ru/kostromskaya_oblast/telefony?cd={}',
        'https://www.avito.ru/kurskaya_oblast/telefony?cd={}',
        'https://www.avito.ru/lipetskaya_oblast/telefony?cd={}',
        'https://www.avito.ru/moskovskaya_oblast/telefony?cd={}',
        'https://www.avito.ru/orlovskaya_oblast/telefony?cd={}',
        'https://www.avito.ru/ryazanskaya_oblast/telefony?cd={}',
        'https://www.avito.ru/smolenskaya_oblast/telefony?cd={}',
        'https://www.avito.ru/tambovskaya_oblast/telefony?cd={}',
        'https://www.avito.ru/tverskaya_oblast/telefony?cd={}',
        'https://www.avito.ru/tulskaya_oblast/telefony?cd={}',
        'https://www.avito.ru/yaroslavskaya_oblast/telefony?cd={}',
        'https://www.avito.ru/moskva/telefony?cd={}'
    ]

    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')

    phones = {}
    for region in regions:
        smarts = []
        for page in range(1, 101):
            driver.get(region.format(page))
            element = driver.find_elements_by_class_name('item__line')
            smarts.extend([i.text for i in element])
        phones[re.sub('^.*.ru/|/telefony.*$', '', region)] = smarts

    with open(os.path.join(DIR_DATA, NAME_JSON), 'w', encoding='utf8') as outfile:
        json.dump(phones, outfile, ensure_ascii=False, indent=2)
        outfile.close()

    with open(os.path.join(DIR_DATA, NAME_JSON)) as json_file:
        phones = json.load(json_file)

    col_names = ['region', 'phones', 'prices', 'city', 'date']
    df = pd.DataFrame(columns=col_names)

    for region, text in phones.items():
        strings = phones[region]
        for string in range(len(strings)):
            string = re.sub('Компания\n','', strings[string])
            parts = string.split('\n')
            if len(parts) == 4:
                df_temp = pd.DataFrame(parts).T
                df_temp.columns = col_names[1:]
                df_temp['region'] = region
                df = pd.concat([df, df_temp])

    df.to_csv(os.path.join(DIR_DATA, NAME_DF), index=False)
