import csv
import psycopg2

def getProduct(artno, suppid):
    sql = f"""
    SELECT id FROM app.products WHERE artno= '{artno}' AND supplier_id= {suppid};
    """
    cur.execute(sql)

def getParams(prodID):
    sql = f"""
    SELECT name, value FROM app.parameters WHERE product_id= '{prodID}';
    """
    cur.execute(sql)

def getSubs(prodID):
    sql = f"""
    SELECT supplier_name, value FROM app.substitutes WHERE product_id= '{prodID}';
    """
    cur.execute(sql)

with open('results.csv', 'r') as fout:
    offer_artno_suppid= {x[-1]:[x[1], x[2]] for x in csv.reader(fout)}

savePath = './opisy/'

conn = psycopg2.connect(
    host="192.168.1.50",
    database="csv_tecdoc",
    user="ms_user_1",
    password="ms_user_1")

for offerID in offer_artno_suppid:

    offerID_prodID = {}

    suppid = offer_artno_suppid[offerID][0]
    artno = offer_artno_suppid[offerID][1]

    cur = conn.cursor()
    
    all = getProduct(artno, suppid)

    prods = cur.fetchall()

    
    

    try:
        offerID_prodID[offerID] = prods[0][0]
        params = getParams(prods[0][0])
        parameters = cur.fetchall()

        parametryLI ='<h1>:name:</h1><ul>'
        zamiennikiLI = '<h1>NUMERY ZAMIENNIKÓW I OEM:</h1><ul>'

        for parSET in parameters:
            parametryLI+=(f"<li><b>{parSET[0]}:</b>{parSET[1]}</li>")
        parametryLI += '</ul>'

        subs = getSubs(prods[0][0])
        substitutes = cur.fetchall()

        
        subDIC = {}
        for subSET in substitutes:
            if subSET[0] not in subDIC:
                subDIC[subSET[0]] = [subSET[1]]
            else:
                subDIC[subSET[0]].append(subSET[1])
        
        for subNAME in subDIC:
            zamiennikiLI +=(f"<li>{subNAME}:")
            for code in subDIC[subNAME]:
                zamiennikiLI += f" {code}"
                if subDIC[subNAME].index(code) +1 != len(subDIC[subNAME]):
                    zamiennikiLI += ','
            zamiennikiLI += "</li>"
        zamiennikiLI += "</ul>"

        with open(f"{savePath}{offerID}", "w") as fout:
            fout.write(f"{parametryLI}\n")
            fout.write(f"{zamiennikiLI}\n")

    except:
        f = open('BRAK_W_TECDOCU.csv', 'a')
        f.write(f"{offerID}\n")


    print(offerID_prodID)
    



conn.commit()

conn.close()
