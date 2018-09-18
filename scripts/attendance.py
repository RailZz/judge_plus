import datetime
import pickle
import json

from config import *

def get_attendance(begin, end):
    info = json.load(open(info_path))
    all_submits = pickle.load(open(submits_path, 'rb'))
    submits = [i for i in all_submits if begin <= i[5] <= end]
    print('submit\'s amount', len(submits))
    user_by_uid = dict()
    total = dict()
    for parallel in info:
        
        for user in info[parallel]["Users"]:
            user["parallel"] = parallel
            user['total_id'] = parallel + ' ({})'.format(user["group"])
            total[user['total_id']] = []
            user_by_uid[user["uid"]] = user
            user_by_uid[user["uid"]]['submit'] = 0
    
    errs = 0
    for contestID, problemID, runID, uid, result, t in submits:
        if uid in user_by_uid:
            user_by_uid[uid]['submit'] += 1
        else:
            errs += 1
            # print("Error uid ", uid, contestID, runID)
            pass

    # print(*[user_by_uid[i] for i in user_by_uid], sep = '\n') 
    # print(len(user_by_uid))
    # print(len(submits))
    # print(errs)

    for uid in user_by_uid:
        if user_by_uid[uid]["submit"] > 0:
            # print("append to ", user_by_uid[uid]["parallel"])
            total[user_by_uid[uid]["total_id"]].append(user_by_uid[uid])

    # print([i["name"] for i in total["B"]])
    

    result = ""
    for parallel in sorted(total.keys()):
        # print(*total[parallel], sep = '\n')
        # print(total[parallel][0]])
        names = sorted([i["name"] + ' ' + str(i['submit']) for i in total[parallel]])
        result += "Параллель " + parallel + '\n' + '\n'.join([str(index + 1) + '. ' + value for index, value in enumerate(names)]) + '\n\n'
    
    print(result)
    



if __name__ == "__main__":
    #begin = datetime.datetime(2018, 8, 22, 15, 30)
    #end = datetime.datetime(2018, 8, 22, 19, 30)

    begin = datetime.datetime(2018, 8, 23, 9, 30)
    end = datetime.datetime(2018, 8, 23, 13, 30)

    #begin = datetime.datetime(2018, 8, 20, 9, 30)
    #end = datetime.datetime(2018, 8, 20, 21, 30)
    get_attendance(begin, end)


    
    
