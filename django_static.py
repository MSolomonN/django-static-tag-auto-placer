def clean_value(value):
    value = value.replace('../', '')     
    value = value.replace('./', '')
    return value
    
def edit_line(line, assets_folder):
    # split the line into a list and loop through 
    # to find src and href tags for editing 
    line_list = line.split() 

    for count in range(0, len(line_list)):
        section = line_list[count]

        # change section only if it has src or href
        if not section.startswith('href') and not section.startswith('src'): continue
        
        # get the value inside the quotes
        section_list = section.split('"') 
        value = section_list[1]

        if value.startswith('#'): continue
        if value.endswith('.html'): continue
        if value.startswith('http'): continue
        if value.startswith('javascript'): continue
        
        # insert the value in our static tags
        value = clean_value(value)
        tag = "{! static '%s/%s' !}" % (assets_folder, value)
        tag = tag.replace('!', '%')

        # replace the section of the line with our new content
        section_list[1] = tag
        line_list[count] = ('"').join(section_list)
        
        print('Changed to', line_list[count])

    return (" ").join(line_list)

def main():
    assets_folder = input("> Enter assets folder. Example 'assets' (leave blank if none): ")
    source_file = input("> Enter html file path: ") 

    # clean assets folder
    assets_folder.replace(' ', '')                  
    assets_folder = assets_folder.replace('/', '')     
    print("\n\nmaking changes...\n\n")
    
    # read source file
    file = open(source_file, 'r', encoding='utf8')
    edited_html = ['{% load static %}']
    
    for line in file.read().split('\n'):
        nwline = edit_line(line, assets_folder)
        edited_html.append(nwline)

    file.close()

    # write new file
    new_file = 'new.html'
    file = open(new_file, 'w', encoding='utf8')
    file.write(('\n').join(edited_html))
    file.close()

    print("\n\nA new file has been created '%s', copy and paste its contents." % new_file)

if __name__ == "__main__":
    main()
