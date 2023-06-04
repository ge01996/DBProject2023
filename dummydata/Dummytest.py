
import random
content= [];

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

print('book ids per school')
for i in range (1,6):
     print('school: ',i,' ',schoolbookdict[str(i)],'\n\n')

'''
DUMMY_DATA_NUMBER = 50;
TABLE_NAME = "schooluser";
TABLE_COLUMNS = ["user_id", "school_id"]
schooluserdict = {'1':[],'2':[],'3':[],'4':[],'5':[]}

for i in range(DUMMY_DATA_NUMBER):
    user_id = str(i)
    school_id = str(random.randint(1,5))
    schooluserdict[(school_id)].append((user_id))
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{user_id}", "{school_id}");\n'

print('user ids per school')
for i in range (1,6):
     print('school: ',i,' ',schooluserdict[str(i)],'\n\n')
     '''
