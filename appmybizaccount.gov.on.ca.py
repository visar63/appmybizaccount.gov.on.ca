import requests
import re
import csv  

from itertools import product
import string

header = ['Business_Name_Type','BName' , 'Address' , 'Incorporation Date', 'RegistrationDate' , 'Business Type' , 'Status' , 'Previously known as', 'Registrant']


with open('Corporations.csv', 'at', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    Letters = [''.join(i) for i in product(string.ascii_lowercase + string.digits, repeat=2)]
    counterr = 1
    for lettr in Letters:
        print (f'*** Kerkimi me shkronjen {lettr}')

        ### NOTEE: response is generated with POSTMAN
        url = "https://www.appmybizaccount.gov.on.ca/onbis/master/viewInstance/update.pub"

        querystring = {"id":"3abd3bce3cc0ad2a19fad9d93acce992eb4d059ffc840bef"}

        payload = f"QueryString={lettr}&_CBASYNCUPDATE_=true&_CBHTMLFRAGID_=1643817697788&_CBHTMLFRAGNODEID_=W58&_CBHTMLFRAG_=true&_CBNAME_=SortRecent&_CBNODE_=W82&_CBVALUE_=true&_CBNAME_=pageSizeChange&_CBVALUE_=4&_VIKEY_=9639a0e1x170bx493ax999dx1ddc43f68f0d&nodeW71-Advanced=N"
        headers = {
            'sec-ch-ua': "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"97\", \"Chromium\";v=\"97\"",
            'x-catalyst-secured': "true",
            'sec-ch-ua-mobile': "?0",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
            'x-catalyst-session-global': "a395ed33f05934737be4956e8c13cf6cdfd1fe585e1d777ed952f3385679f1a733ffdca7c35cbe28",
            'content-type': "application/x-www-form-urlencoded",
            'x-security-token': "null",
            'accept': "text/html, */*; q=0.01",
            'x-requested-with': "XMLHttpRequest",
            'x-catalyst-async': "true",
            'sec-ch-ua-platform': "\"Windows\"",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'cache-control': "no-cache",
            'postman-token': "2b6de585-91d2-8f69-40d6-9f1a296e1be9"
            }
        try:
            response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

            # print(response.text)

            with open('file.html', 'w') as aa:
                aa.write(response.text)


            ### PARSIMIII ####

            BName = Address = IncorporationDate = BusinessType = Status = pka = pkaaa = Registrant = Business_Name_Type = RegistrationDate =''

            for record in re.findall(r'((?:Corporations|Business Names)</div>.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>)', response.text, re.I|re.S):
                
                pttr_btype = re.search(r'(.*?)</div>', record, re.I|re.S)
                if pttr_btype:
                    Business_Name_Type = pttr_btype.group(1)
                
                pttr_name = re.search(r'return false;}\(this\)"><span class="left"></span><span>(.*?)</span>', record, re.I|re.S)
                if pttr_name:
                    BName = pttr_name.group(1)
                    print (f'{counterr}) Name: {BName}')
                    counterr += 1
                    # with open('names.txt', 'at') as aa:
                    #     aa.write(BName + "\n")
                pttr_addr = re.search(r'<div class="appAttrValue">(.*?)</div>', record, re.I|re.S)
                if pttr_addr:
                    Address = pttr_addr.group(1)
                pttr_date = re.search(r'appMinimalLabel">(?:Incorporation(?:/Amalgamation)?|Amalgamation) Date</span><span class="appMinimalValue" aria-hidden="true">(.*?)<', record, re.I|re.S)
                if pttr_date:
                    IncorporationDate = pttr_date.group(1)
                pttr_type = re.search(r'Business Type</span><span class="appMinimalValue">(.*?)<', record, re.I|re.S)
                if pttr_type:
                    BusinessType = pttr_type.group(1)
                pttr_status = re.search(r'Status</span><span class="appMinimalValue">(.*?)<', record, re.I|re.S)
                if pttr_status:
                    Status = pttr_status.group(1)
                pttr_reg = re.search(r'Registrant<.span><.div>.*?class=.left.><.span><span>([^<]+)</span>', record, re.I|re.S)
                if pttr_reg:
                    Registrant = pttr_reg.group(1)
                    # print (f'aaa {Registrant}')
                pttr_date2 = re.search(r'appMinimalLabel">Registration Date</span><span class="appMinimalValue" aria-hidden="true">(.*?)<', record, re.I|re.S)
                if pttr_date2:
                    RegistrationDate = pttr_date2.group(1)
                pttr_PKA = re.search(r'Previously known as</span>(.*?)</div>\s+</div>\s+</div>', record, re.I|re.S)
                if pttr_PKA:
                    pka = pttr_PKA.group(1)
                    pkaaa = ''
                    for pkaa in re.findall(r'appMinimalValue">(.*?)</span>', pka, re.I|re.S):
                        pkaaa += str(pkaa) + ", "
                    pkaaa = pkaaa[:-2]
                    print (f'\tPKA: {pkaaa}')
                
                # else:
                #     print ('wtffff')

                contenttt = f'<Fillimi>{record}<Fundi><br>\n'
                with open('kontenti.txt', 'at') as aa:
                    aa.write(contenttt + "\n")

                data = [Business_Name_Type, BName , Address , IncorporationDate, RegistrationDate , BusinessType , Status , pkaaa, Registrant]
                writer.writerow(data)
                BName = Address = IncorporationDate = BusinessType = Status = pka = pkaaa = Registrant = Business_Name_Type = RegistrationDate = ''
        except Exception as e:
            print (e)