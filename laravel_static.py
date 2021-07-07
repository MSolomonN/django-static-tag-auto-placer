def clean_location(loc):
    loc = loc.replace('../', '')
    
    if loc.startswith('/'):
        loc = loc[1:]
        
    return loc
    
def check_line(line, assets_folder):
    line_list = line.split(" ") # split the line into a list
    count = 0 # save the index of an object in the list

    # for each object in the list analyze it and change it if neccessary
    for obj in line_list:
      if obj.startswith("href") or obj.startswith("src"): # change only if it is src or href
        another_list = obj.split('"') # split the section again into a list to get the plain text inside quotes
        loc = another_list[1]
        if loc != '#' and loc.endswith(".html") == False and loc.startswith("http") == False: # avoid # and .html
          loc = clean_location(loc)
          header = "{{ asset('%s%s') }}" % (assets_folder,loc)
          #header = header.replace('!', '%')
          another_list[1] = header
          line_list[count] = ('"').join(another_list) # after replacing content join the list
      count += 1

    line = (" ").join(line_list) # join the line
    return line # return edited line

def main():
  assets_folder = input("> Enter assets folder. Example 'assets' (leave blank if none): ")
  # make sure assets_folder is correct
  if assets_folder.startswith('/'):
    assets_folder = assets_folder.replace('/', '')     
  if assets_folder.endswith('/') == False:
    assets_folder = "%s/" % assets_folder
  assets_folder.replace(' ', '') # important to remove added spaces

  edit_file = input("> Enter html file location: ") # html file location
  file = open(edit_file, 'r')

  final_html = []
  if assets_folder == "/":
    assets_folder = ""
  
  print(("\nPlacing {! static '%s...' !}" % assets_folder).replace('!', '%'))
  for line in file.readlines():
    l = check_line(line, assets_folder)
    final_html.append(l) # append edited line

  # write a new file
  new_file = 'new.blade.php'
  file2 = open(new_file, 'w')
  new_html = ("").join(final_html)
  file2.write(new_html)
  file2.close()
  print("\nA new file has been created '%s', copy and paste its contents." % new_file)

"""
try:
  main()
except Exception as e:
  print(e)
  print("\nAn error has occured! Make sure the html file location is correct.")
"""
main()