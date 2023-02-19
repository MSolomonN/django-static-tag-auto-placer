from bs4 import BeautifulSoup

def read_file(source_file):
    file = open(source_file, 'r', encoding='utf8')
    html = file.read()
    file.close()
    return html

def write_file(soup, new_file):
    file = open(new_file, 'w', encoding='utf8')
    file.write(str(soup))
    file.close()

def clean_src(src):
    if not src or src.startswith('http'):
        return None

    elif src.startswith('./'):
        return src.replace('./', '', 1)

    elif src.startswith('/'):
        return src.replace('/', '', 1)

    else:
        return src
                
def get_static_url(src, assets_folder):
    if assets_folder: src = f'{assets_folder}/{src}'

    static_url = f"<% static '{src}' %>"
    static_url = static_url.replace('<', '{')
    static_url = static_url.replace('>', '}')
    print(static_url)
    
    return static_url

def replace_css(soup, assets_folder):
    els = soup.find_all('link')

    for el in els:
        src = clean_src(el.get('href'))
        if not src: continue
        el['href'] = get_static_url(src, assets_folder)

def replace_js(soup, assets_folder):
    els = soup.find_all('script')

    for el in els:
        src = clean_src(el.get('src'))
        if not src: continue
        el['src'] = get_static_url(src, assets_folder)
    
def replace_images(soup, assets_folder):
    els = soup.find_all('img')

    for el in els:
        src = clean_src(el.get('src'))
        if not src: continue
        el['src'] = get_static_url(src, assets_folder)

def main(assets_folder, source_file):
    assets_folder = assets_folder.replace(' ', '')
    soup = BeautifulSoup(read_file(source_file), 'html.parser')
    
    # replace to use static tag
    replace_css(soup, assets_folder)
    replace_js(soup, assets_folder)
    replace_images(soup, assets_folder)

    write_file(soup, 'new.html')

if __name__ == "__main__":
    assets_folder = input("> Enter assets folder. Example 'assets' (leave blank if none): ")
    source_file = input("> Enter html file path: ") 
    main(assets_folder, source_file)
