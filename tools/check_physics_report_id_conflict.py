import sqlite3,json
ids=['real_1402_n2in_phys_075','real_1404_n2in_phys_075','real_1402_n2in_phys_070','real_1402_n2in_phys_073','real_1402_n2in_phys_056','real_1403_n1in_phys_063','real_1403_n1in_phys_074']
c=sqlite3.connect('/home/ubuntu/physics-review/radiology1405_bank_v6_1.db'); c.row_factory=sqlite3.Row
for i in ids:
 r=c.execute('select id,subject,full_json from question where id=?',(i,)).fetchone(); q=json.loads(r['full_json'])
 print(i, '\n stem=',q.get('stem','')[:250], '\n analysis=',q.get('correct_analysis','')[:350], '\n key=',q.get('correct_index'))
