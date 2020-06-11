import sqlite3
import cv2
import base64

password = '1'
password_input = input('enter your password: \n')

while password_input != password:
   password_input = input('enter correct password: \n')

if password_input == password:
   conn = sqlite3.connect("database.db")
   cursor = conn.cursor()

   try:
      cursor.execute("""CREATE TABLE SecretFiles
                     (FULL_NAME text, FILE_NAME text, EXTENSION text, FILES text)""")
   except:
      print('You have your safety!') 

while True:
   print('#' * 15)
   print('What you want to do?')
   print('q - quit \n' + 'o - open file \n' + 's - save file')
   print('#' * 15)
   choose_input = input(': ').title()

   if choose_input == 'Q':
      break




   if choose_input == 'S':
      types = {
      'py' : 'TEXT',
      'docx' : 'TEXT',
      'txt' : 'TEXT',
      'png' : 'IMAGE'
      }
      path = input('Enter the path to file: \n')
      file_name = path.split('\\')
      file_name = file_name[len(file_name)-1]
      file_extension = path.split('.')[1]
      inside = ""
      try:
         file_extension = types[file_extension]
      except:
         Exception()

      if file_extension == 'TEXT':
         with open(path, "rb") as output:
            d = output.read()
            inside = base64.b64encode(d)

      if file_extension == 'IMAGE':
         image = cv2.imread(path)
         inside = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()

         
      full_info = [path, file_name, file_extension, inside]
      cursor.execute(" INSERT INTO SecretFiles VALUES (?,?,?,?)", full_info)
      conn.commit()



   if choose_input == 'O':
      file_name = input('What name of a file? \n:')
      file_extension = input('What type of a file? \n:')
      FILE = file_name + '.' + file_extension
      choosen = ("SELECT * from SecretFiles WHERE FILE_NAME=" + '"' + FILE + '"')
      cursor.execute(choosen)
      for row in cursor:
         inside = row[3]
         print(inside)
         with open(FILE, 'wb') as output:
            output.write(base64.b64decode(inside))
               
      
