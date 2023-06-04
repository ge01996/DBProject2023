import faker
import random


fake = faker.Faker()

DUMMY_DATA_NUMBER = 4;
TABLE_NAME = "role";
TABLE_COLUMNS = ["id", "role_desc"]
content = "";
role_list = ['student' , 'teacher' , 'librarian' , 'admin']
for i in range(DUMMY_DATA_NUMBER):
    id = i
    role_desc = role_list[i] 
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{id}", "{role_desc}");\n'



DUMMY_DATA_NUMBER = 80;
TABLE_NAME = "users";
TABLE_COLUMNS = ["id"," username","password","first_name", "last_name","birthdate","address","zip_code","role_id","curr_rnt"]

list = [0,0,0,0,1,2,3]
for i in range(DUMMY_DATA_NUMBER):

    username = fake.unique.user_name()
    password = fake.password()
    firstName = fake.first_name()
    lastName = fake.last_name()
    birthdate = fake.date()
    address = fake.address()
    zip_code = fake.postalcode()
    role_id = int(random.choice(list))
    curr_rnt = 0
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES (default,"{username}","{password}","{firstName}","{lastName}","{birthdate}","{address}","{zip_code}","{role_id}","{curr_rnt}");\n'



DUMMY_DATA_NUMBER = 5;
TABLE_NAME = "school";
TABLE_COLUMNS = ["id", "name", "email","principal","librarian","city","address","zip_code","phone"]


for i in range(DUMMY_DATA_NUMBER):

    name = 'School No ' + str(i+1)
    email = fake.unique.ascii_safe_email()
    principal = fake.unique.name()
    librarian = fake.unique.name()
    city = fake.city()
    address = fake.unique.address()
    zip_code = fake.postalcode()
    phone = fake.unique.phone_number()
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES (default,"{name}", "{email}", "{principal}", "{librarian}", "{city}", "{address}", "{zip_code}", "{phone}");\n'



DUMMY_DATA_NUMBER = 100;
TABLE_NAME = "book";
TABLE_COLUMNS = ["id", "isbn", "title","publisher","summary","lang","pages","coverurl"]

bookdict = {}

for i in range(DUMMY_DATA_NUMBER):
    
    isbn = fake.unique.isbn13()
    title = 'Book Title ' + str(i+1)
    publisher = fake.unique.name()
    summary = fake.text()
    lang = fake.language_code()
    pages = random.randint(30,500)
    bookdict[str(i+1)] = []
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES (default,"{isbn}", "{title}", "{publisher}", "{summary}", "{lang}", "{pages}",default);\n'

bookdict2 = bookdict
bookdict3 = bookdict

DUMMY_DATA_NUMBER = 120;
TABLE_NAME = "schoolbook";
TABLE_COLUMNS = ["school_id", "book_id", "curr_copies","tot_copies"]
schoolbookdict = {'1':[],'2':[],'3':[],'4':[],'5':[]}

for _ in range(DUMMY_DATA_NUMBER):
    school_id = random.randint(1,5)
    book_id = str(random.randint(1,100))
    while (book_id in schoolbookdict[str(school_id)]):
        book_id = str(random.randint(1,100))
    copies = random.randint(1,10)
    schoolbookdict[str(school_id)].append(str(book_id))
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{school_id}", "{book_id}", "{copies}", "{copies}");\n'

'''print('book ids per school')
for i in range (1,6):
     print('school: ',i,' ',schoolbookdict[str(i)],'\n\n')'''


DUMMY_DATA_NUMBER = 80;
TABLE_NAME = "schooluser";
TABLE_COLUMNS = ["user_id", "school_id"]
schooluserdict = {'1':[],'2':[],'3':[],'4':[],'5':[]}

for i in range(DUMMY_DATA_NUMBER):
    user_id = str(i+1)
    school_id = str(random.randint(1,5))
    schooluserdict[(school_id)].append((user_id))
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{user_id}", "{school_id}");\n'

'''print('user ids per school')
for i in range (1,6):
     print('school: ',i,' ',schooluserdict[str(i)],'\n\n')'''

DUMMY_DATA_NUMBER = 40;
TABLE_NAME = "writer";
TABLE_COLUMNS = ["id", "name"]


for _ in range(DUMMY_DATA_NUMBER):
    name = fake.unique.name()
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES (default, "{name}");\n'



DUMMY_DATA_NUMBER = 180;
TABLE_NAME = "bwriter";
TABLE_COLUMNS = ["book_id", "writer_id"]


for i in range(DUMMY_DATA_NUMBER):
    book_id = random.randint(1,100)
    writer_id = random.randint(1,40)
    while (str(writer_id) in bookdict2[str(book_id)]):
            book_id = str(random.randint(1,100))
    bookdict2[str(book_id)].append(str(writer_id))
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{book_id}", "{writer_id}");\n'



DUMMY_DATA_NUMBER = 10;
TABLE_NAME = "category";
TABLE_COLUMNS = ["id", "name"]

list = ['History','Novel','Poetry','Sci-Fi','Fantasy','Foreign','Lecture Specific','For young kids','Romance','Mystery']
for i in range(DUMMY_DATA_NUMBER):
    
    name = list[i]
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES (default, "{name}");\n'



DUMMY_DATA_NUMBER = 150;
TABLE_NAME = "bookcat";
TABLE_COLUMNS = ["book_id", "cat_id"]


for _ in range(DUMMY_DATA_NUMBER):

    book_id = (random.randint(1,100))
    cat_id = str(random.randint(1,10))
    while (cat_id in bookdict[str(book_id)]):
        cat_id = str(random.randint(1,10))
    bookdict[str(book_id)].append(str(cat_id))
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{book_id}", "{cat_id}");\n'


DUMMY_DATA_NUMBER = 150;
TABLE_NAME = "keyword";
TABLE_COLUMNS = ["book_id", "word"]


for _ in range(DUMMY_DATA_NUMBER):
    book_id =  random.randint(1,100)
    word = 'Keyword ' + str(random.randint(1,20))
    while (word in bookdict3[str(book_id)]):
        word = str(random.randint(1,20))
    bookdict3[str(book_id)].append(str(word))
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{book_id}", "{word}");\n'



DUMMY_DATA_NUMBER = 70;
TABLE_NAME = "rental";
TABLE_COLUMNS = ["user_id", "book_id", "trdate","status","libr_id"]
TABLE_NAME2 = "rating";
TABLE_COLUMNS2 = ["user_id", "book_id", "trdate","ratetext","likert"]

for _ in range(DUMMY_DATA_NUMBER):
        school_id = str(random.randint(1,5))
        if (len(schooluserdict[school_id])==0): continue
        user_id = schooluserdict[school_id].pop()
        book_id = schoolbookdict[school_id].pop()
        ratetext = fake.text()
        likert = random.randint(1,5)
        trdate = fake.date()
        content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{user_id}", "{book_id}","{trdate}",0,default);\n'
        content += f'INSERT INTO {TABLE_NAME2} ({",".join(TABLE_COLUMNS2)}) VALUES ("{user_id}", "{book_id}","{trdate}", "{ratetext}","{likert}");\n'
with open("insertdata.sql", 'w') as f:
        f.write(content)




'''DUMMY_DATA_NUMBER = 0;
TABLE_NAME = "reservation";
TABLE_COLUMNS = ["user_id", "book_id", "trdate","status"]
content = "";

for _ in range(DUMMY_DATA_NUMBER):
    user_id = random.randint(1,30)
    book_id = random.randint(1,100)
    
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{user_id}", "{book_id}", default,"0");\n'

with open(f"dummy_data_{TABLE_NAME}.txt", 'w') as f:
    f.write(content)'''




