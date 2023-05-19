import re
import json

def GetNodeCount(id, payload, F, T, R):
    with open('NodeCountDb.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                return 0
            if len(line) == 0:
                continue
            jsonData = json.loads(line)
            jsp = jsonData['payload']
            F1 = re.findall('F\.......', jsonData['payload'])
            T1 = re.findall('T\...', jsonData['payload'])
            R1 = re.findall('R\...', jsonData['payload'])
            if F1 and F:
                jsp = jsonData['payload'].replace(F1[0], F[0])
                if T1 and T:
                    jsp = jsonData['payload'].replace(T1[0], T[0])
                    if R1 and R:
                        jsp = jsonData['payload'].replace(R1[0], R[0])
            if jsp == payload and jsonData['id'] == id:
                return int(jsonData['sum'])

def main():
    print('---------------------------IDs-----------------------------')
    print('')
    print('Spin & Go: BTNvsBB-105, BTNvsSB-103, HU-101, SBvsBB-104, SBvsBB no Limp-108')
    print('Hu ante: Hu Ante-106')
    print('6-Max Cash: Nl500-111')
    print('MTT: MTT 8max-110, MTT 9max-109')
    print('HU Cash: Hu Cash-107')
    print('')
    print('-----------------------------------------------------------')

    str = '25_P.r2.00_P.c_F.Th4h3h_P.k_P.k_T.Ks_P.k_P.k_R.Kh_P.k_P.r1.12_P.r4.50_P.r11.25_P.r23.00'
    print(str.__contains__(' '))

    while True:
        id_input_payload = input('Enter id and input link: ')
        id = re.split('\s', id_input_payload)[0]
        input_payload = re.split('\s', id_input_payload)[1]
        
        F = re.findall('F\.......', input_payload)
        T = re.findall('T\...', input_payload)
        R = re.findall('R\...', input_payload)
     
        print(GetNodeCount(id, input_payload, F, T, R))

if __name__ == '__main__':
    main()
