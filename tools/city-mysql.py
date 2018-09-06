import json
import pymysql

# 链接数据库
db = pymysql.Connect(host='127.0.0.1', port=3306, user='root', password='123456', database='PTT', charset='utf8')
# 数据库游标
cursor = db.cursor()

# 打开文件
with open('city.json', 'r') as f:
    # json对象
    city_collection = json.load(f)
    # print(city_collection)

    # 获取所有returnValue
    returnValue= city_collection.get('returnValue')
    # 获取所有的键
    letters = returnValue.keys()
    # print(letters)



    # 遍历keys
    for letter_key in letters:
        # print(letter_key)

        # 写入字母模型类 >> letter表
        # INSERT INTO letter(name) VALUES('A')
        db.begin()
        cursor.execute("INSERT INTO letter(name) VALUES('{}')".format(letter_key))
        db.commit()

        # 根据letter_key 获取对应的 id
        # SELECT * FROM letter WHERE name='A'
        db.begin()
        cursor.execute("SELECT * FROM letter WHERE name='{}'".format(letter_key))
        db.commit()
        result = cursor.fetchone()
        letter_id = result[0]
        # print(letter_id)

        # 'A': []
        # 获取每个字母对应的value
        citys = returnValue[letter_key]
        for city in citys:
            # c_letter  >> leter.id
           # INSERT INTO city(id,regionName,cityCode,pinYin,c_letter) VALUES('110', '西安', 123, 'xian', 3)

            db.begin()
            cursor.execute("INSERT INTO city(id,regionName,cityCode,pinYin,c_letter) VALUES({}, '{}', {}, '{}', {})".format(city.get('id'), city.get('regionName'), city.get('cityCode'), city.get('pinYin'), letter_id))
            db.commit()
