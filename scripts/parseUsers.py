from config import *
import json
import pymysql



class UserParser:
    def __init__(self):
        self.db = pymysql.connect("localhost", "ejudge", "ejudge", "ejudge", charset="utf8")
        self.cursor = self.db.cursor()

    def get_user_by_login(self, login):
        self.cursor.execute('select users.user_id, logins.login, users.username from users, logins where users.user_id=logins.user_id and logins.login="{}"'.format(login))
        data = self.cursor.fetchall()
        if len(data) != 1:
            raise Exception(str(len(data)) + " users found, 1 expected")
        userid, login, username = data[0]
        return {"uid": userid, "login": login, "name": username}

    def set_username(self, user):
        assert("uid" in user)
        assert("login" in user)
        assert("name" in user)
        self.cursor.execute('update users set username="{}" where user_id={}'.format(user["name"], user["uid"]))
        self.cursor.fetchall()


def parse_user_from_stdin():
    """
    format:
    surname name login parallel 
    """

    info = json.load(open(info_path))
    for parallel in info:
        info[parallel]["Users"] = []
        
    up = UserParser()
    while (True):
        try:
            data = input().strip().split()
        except Exception as e:
            break
        if len(data) != 5:
            print("wrong data, skipping: ", data)
            continue
        surname, name, login, parallel, group = data
        user = up.get_user_by_login(login)
        user["name"] = surname + ' ' + name
        user["group"] = group
        print(user)
        up.set_username(user)
        info[parallel]["Users"].append(user)

        
        # print(json.dumps(info, open(info_path, 'w'), indent=4, sort_keys=True, ensure_ascii=False)
    print(json.dumps(info, indent=4, sort_keys=True, ensure_ascii=False))
    json.dump(info, open(info_path, 'w'), indent=4, sort_keys=True, ensure_ascii=False)
    



if __name__ == "__main__":
    parse_user_from_stdin()



    




