import re
import requests
import json
import time

Sum = 0 
pattern = '"next_query":\[[a-zA-Z0-9._",]+\]'
pattern1 = '"20_P.[a-zA-Z0-9._"]+\"'
i = 0
Kartebis_massivi = ['Ac','Ad','Ah','As','2c','2d','2h','2s','3c',
                  '3d','3h','3s','4c','4d','4h','4s','5c','5d',
                  '5h','5s','6c','6d','6h','6s','7c','7d','7h',
                  '7s','8c','8d','8h','8s','9c','9d','9h','9s',
                  'Tc','Td','Th','Ts','Jc','Jd','Jh','Js',
                  'Qc','Qd','Qh','Qs','Kc','Kd','Kh','Ks']

ids = ''

############################################################################### Login

def login(username, password):
    global session
    global headers
    session = requests.Session()
    payload = {
        'username': username,
        'password': password 
    }
    res = session.post('https://api.gtobase.com/v2/login', json=payload)
    print(res)

############################################################################### Axali payloadi

def CheckQuery(query, st):
    payload_list = []
    query = '{' + query + '}'
    data = json.loads(query)
    for item in data['next_query']:
        if item.startswith(st):
            print(item)
            payload_list.append(item)
    return payload_list

def SaveNodeCount(payload, sum, id):
    data = {"id": id, "payload": payload, "sum": sum}
    p = re.compile('(?<!\\\\)\'')
    purifyData = p.sub('\"', str(data))
    with open('NodeCountDb.txt', 'a') as f:
        f.write(str(purifyData))
        f.write('\n')

def GetNodeCount(id, payload):
    with open('NodeCountDb.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                return 0
            if len(line) == 0:
                continue
            jsonData = json.loads(line)
            if jsonData['payload'] == payload and jsonData['id'] == id:
                return int(jsonData['sum'])

############################################################################### Flop, Turn, RIVER

def Axali_Kartebi(payload):
    k_c = ''
    if re.findall('c_$', payload):
        k_c = 'c_'
    elif re.findall('k_$', payload):
        k_c = 'k_'
        
    if len(re.findall('_F.', payload)) == 0:
        new_payload = payload + 'F.Th4h3h'
        return new_payload          
        
    elif len(re.findall('_F.', payload)) == 1 and len(re.findall('_T.', payload)) == 0:
        axali_karti = ''
        f = '_F.' 
        patternf = f + '.[a-zA-Z0-9]+\_' 
        pre_Kartebif = re.search(patternf, payload)
        Kartebif = pre_Kartebif.group()[3:9]
        for k in Kartebis_massivi:
            if len(re.findall(k, Kartebif)) == 0:
                axali_karti = k
        new_payload = payload + 'T.' + axali_karti
        return new_payload

    elif len(re.findall('_F.', payload)) == 1 and len(re.findall('_T.', payload)) == 1 and len(re.findall(k_c + '_R', payload)) == 0:
        axali_karti = ''
        f = '_F.'
        patternf = f + '.[a-zA-Z0-9]+\_' 
        pre_Kartebif = re.search(patternf, payload)
        Kartebif = pre_Kartebif.group()[3:9]
        
        t = '_T.'
        patternt = t + '.[a-zA-Z0-9]+\_'
        pre_Kartebit = re.search(patternt, payload)
        Kartebit = pre_Kartebit.group()[3:5]
        
        for k in Kartebis_massivi:
            if len(re.findall(k, Kartebif + Kartebit)) == 0:
                axali_karti = k
        new_payload = payload + 'R.' + axali_karti        
        return new_payload

################################################################################ Mtavari

def NodeCount(payload, id_, st):
    global i
    sum = 0 

    if payload.endswith('_'):
        payload = Axali_Kartebi(payload)
        print('axali karti')  
        sum += 1  # es is ponti ra Flop, Turn, RIVER tu gamoidzaga egec datvalos
    
    response = session.post('https://api.gtobase.com/v2/get_strategy', headers=headers, json={'id': id_, 'q': payload})
    if response.status_code == 401:
        try:
            login(username, password)
            return NodeCount(payload, id_, st)
        except:
            return NodeCount(payload, id_, st)
    elif response.status_code == 429:
        i += 1
        print("Out of limits")
        if i < 10:
            time.sleep(15)
        else:
            i = 0
            time.sleep(2000)
        return NodeCount(payload, id_, st)
    elif response.status_code == 500:
        print(response.content)
        time.sleep(2)
        return NodeCount(payload, id_, st)
    else:
        result = re.findall(pattern, str(response.content))
        payload_list = CheckQuery(result[len(result) - 1], st)
        print(payload_list)
        if len(payload_list) != 0:
            sum += len(payload_list)
            for p in payload_list:
                sum += NodeCount(p, id_, st)
            # insert into db
            SaveNodeCount(payload, sum, id_)
            return sum
        else:
            # insert into db
            SaveNodeCount(payload, 0, id_)
            return 0

################################################################################ yleoba

def main():
    print('---------------------------IDs-----------------------------')  
    print('')
    print('Spin & Go: BTNvsBB-105 , BTNvsSB-103 , HU-101 , SBvsBB-104 , SBvsBB no Limp-108')
    print('Hu ante: Hu Ante-106')
    print('6-Max Cash: Nl500-111')         
    print('MTT: MTT 8max-110 , MTT 9max-109')
    print('HU Cash: Hu Cash-107 ')  
    print('')
    print('-----------------------------------------------------------')       

    global username
    global password
    username = input('Enter username: ')
    password = input('Enter password: ')

    # login
    login(username, password)                  

    # main loop
    while True: 
        id_ = input('Enter id of position (see IDs): ')
        Stacks = input('Enter list of Stacks separated by space (E.g: 25 22 20 18): ')
        Stackss = re.split('\s', Stacks)
        
        for st in Stackss:
            print(st)   
            sum = NodeCount(st, id_, st)
            print(f'final sum: {sum}')


if __name__ == '__main__':
    main()
