def check_line(line, path):
    line_list = line.split(" ") # split the line into a list
    count = 0 # save the index of an object in the list

    # for each object in the list analyze it and change it if neccessary
    for obj in line_list:
      if obj.startswith("href") or obj.startswith("src"): # change only if it is src or href
        another_list = obj.split('"') # split the section again into a list to get the plain text inside quotes
        loc = another_list[1]
        if loc is not '#' and loc.endswith(".html") == False and loc.startswith("http") == False: # avoid # and .html
          header = ">! static '%s%s' !<" % (path,loc)
          header = header.replace('>', '{')
          header = header.replace('<', '}')
          header = header.replace('!', '%')
          another_list[1] = header
          line_list[count] = ('"').join(another_list) # after replacing content join the list
      count += 1

    line = (" ").join(line_list) # join the line
    print(line.replace('/n', ''))
    return line # return edited line

def main():
  path = input("Assets folder example 'assets/' (leave blank if none): ") # static path
  edit_file = input("Enter html file location: ") # html file location
  file = open(edit_file, 'r')

  final_html = []
  for line in file.readlines():
    print(line)
    l = check_line(line, path)
    final_html.append(l) # append edited line

  # write a new file
  file2 = open('new.html', 'w')
  new_html = ("").join(final_html)
  file2.write(new_html)
  file2.close()

main()
