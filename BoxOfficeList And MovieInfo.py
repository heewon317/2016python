# -*- coding: utf-8 -*-
from xml.etree import ElementTree
from http.client import HTTPConnection
loopFlag = 1
xmlFD = -1
##global
conn = None
regKey = 'bb48880c629b0289e1b1fea9d38c09a5'
# 박스오피스 OpenAPI 접속 정보 information
server = "kobis.or.kr"
itemElements = None

#####영화코드 저장 리스트
movieTop10 = []
movieTop10d = dict()


def userURIBuilder(server,**user):  #**은 사전형식으로 반환해주는
    str = "http://" + server + "/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml" + "?"
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str
    
def userURIBuilder_2(server,**user):  #**은 사전형식으로 반환해주는
    str = "http://" + server + "/kobisopenapi/webservice/rest/movie/searchMovieInfo.xml" + "?"
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str

def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)
    
def getBookDataFromISBN(date):
    global server, regKey, conn, req
    if conn == None :
        connectOpenAPIServer()
    uri = userURIBuilder(server, key=regKey, targetDt=date)
    conn.request("GET", uri)

    req = conn.getresponse()
    print (req.status)
    if int(req.status) == 200 :
        print("BoxOffice data downloading complete!")
        extractBookData(req.read())
    else:
        print("OpenAPI request has been failed!! please retry")
        return None
        
def getBookDataFromISBN_2(Cd):
    global server, regKey, conn, req
    if conn == None :
        connectOpenAPIServer()
    uri = userURIBuilder_2(server, key=regKey, movieCd=Cd)
    conn.request("GET", uri)

    req = conn.getresponse()
    print (req.status)
    if int(req.status) == 200 :
        print("BoxOffice data downloading complete!")
        extractBookData_2(req.read())
    else:
        print("OpenAPI request has been failed!! please retry")
        return None


def extractBookData(strXml):
    global itemElements    
 
    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("dailyBoxOffice")  # return list type
    movieTop10.clear()
    for item in itemElements:
        date = item.find("rank")
        strTitle = item.find("movieNm")
        movieCd = item.find("movieCd").text     #movieCd를 찾아서 movieCd에넣어줌
        movieTop10.append(movieCd)      #리스트에 넣는다
        if len(strTitle.text) > 0 :
           print(date.text,"위 : ",strTitle.text)
          
    for x in range(10): #사전에 리스트 넣어주기
        movieTop10d[x+1] = movieTop10[x]
    print("\n-----------------------------------------\n")
    for k,v in movieTop10d.items():
        print(k,"위 Code : ",v)     #시험 출력
        

def extractBookData_2(strXml):
    global itemElements    

    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("movieInfo")  # return list type
    itemElements2 = tree.getiterator("nation")
    itemElements3 = tree.getiterator("genre")
    itemElements4 = tree.getiterator("director")
    itemElements5 = tree.getiterator("actor")
    
    
    for item in itemElements:
        strTitle = item.find("movieNm")
        date = item.find("openDt")
        time = item.find("showTm")

    for item in itemElements2:
        nation = item.find("nationNm")
    for item in itemElements3:
        genres = item.find("genreNm")
    for item in itemElements4:
        director = item.find("peopleNm")
        
        
    if len(strTitle.text) > 0 :           
        #print(date.text,"위 : ",strTitle.text)
        print("영화 제목: ", strTitle.text)
        print("개봉 날짜: ", date.text)
        print("상영 시간: ", time.text, "분")
        print("국적: ", nation.text)
        print("장르: ", genres.text)
        print("감독: ", director.text)
        
    for item in itemElements5:
            actor = item.find("peopleNm")    
            if len(strTitle.text) > 0 :  
                print("배우: ", actor.text)
        
          
    



#### Menu  implementation
def printMenu():
    print("\nWelcome! BoxOffice Movie Manager Program (xml version)") 
    print("========Menu==========")
    print("Quit program: q")
    print("print movie list: p")
    print("sEarch Daily BoxOffice list: e")
    print("Search movieCd: c")
    print("==================")
    
def launcherFunction(menu):
    global itemElements
    if menu == 'e':
        date = str(input ('조회할 날짜 입력(yyyymmdd):'))
        getBookDataFromISBN(date)
      #  printBookList(SearchBookTitle(keyword))
    elif menu == 'p':
        print(itemElements)
    elif menu == 'c':
        Cd = str(input('input movieCd to search : '))        
        #keyword = str(input ('input keyword to search :'))
        getBookDataFromISBN_2(Cd)
        #SearchBookTitle(keyword)
    elif menu == 'q':
        QuitBookMgr()
    else:
        print ("error : unknow menu key")        
        
    
     
def PrintBookList(tags):
    global BooksDoc
#    if not checkDocument():
 #      return None
        
    booklist = BooksDoc.childNodes
    book = booklist[0].childNodes
    for item in book:
        if item.nodeName == "dailyBoxOffice":
            subitems = item.childNodes
            for atom in subitems:
               if atom.nodeName in tags:
                   print("title=",atom.firstChild.nodeValue)
                   
                   
def SearchBookTitle(keyword):
    global BooksDoc
#    if not checkDocument():
 #       return None
    retlist = []
        
    try:
        tree = ElementTree.fromstring(str(BooksDoc.toxml()))
    except Exception:
        print ("Element Tree parsing Error : maybe the xml document is not corrected.")
        return None
    
    itemElements = tree.getiterator(keyword)  # return list type
    for item in itemElements:
        strTitle = item.find("movieNm").text
        if len(strTitle.text) > 0 :
           print(strTitle.text,": ",item.attrib["movieCd"].text)
    return retlist
    
    
                   
def printBookList(retlist):
    for res in retlist:
        print (res)
        
        
def QuitBookMgr():
    global loopFlag
    loopFlag = 0
    
##### run #####
while(loopFlag > 0):
    printMenu()
    menuKey = str(input ('select menu :'))
    launcherFunction(menuKey)
else:
    print ("Thank you! Good Bye")