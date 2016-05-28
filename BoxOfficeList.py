# -*- coding: utf-8 -*-
from xml.dom.minidom import parse, parseString
from xml.etree import ElementTree

from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer

loopFlag = 1
xmlFD = -1
BooksDoc = None

##global
conn = None
regKey = 'bb48880c629b0289e1b1fea9d38c09a5'
# 박스오피스 OpenAPI 접속 정보 information
server = "kobis.or.kr"

def userURIBuilder(server,**user):  #**은 사전형식으로 반환?해주는
    str = "http://" + server + "/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml" + "?"
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str


def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)
    
    
def getBookDataFromISBN(date):
    global server, regKey, conn
    if conn == None :
        connectOpenAPIServer()
    uri = userURIBuilder(server, key=regKey, targetDt=date)
    conn.request("GET", uri)
    
    req = conn.getresponse()
    print (req.status)
    if int(req.status) == 200 :
        print("BoxOffice data downloading complete!")
        print("qqqqqqqqqqqqqqqqqqqqq!!")
        return extractBookData(req.read())
    else:
        print("OpenAPI request has been failed!! please retry")
        return None


def extractBookData(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    print (strXml)
    # Book 엘리먼트를 가져옵니다.
    itemElements = tree.getiterator("dailyBoxOffice")  # return list type
    print(itemElements)
    for item in itemElements:
        date = item.find("rank")
        strTitle = item.find("movieNm")
        print (strTitle)
        if len(strTitle.text) > 0 :
           print("rank:",date.text,"movieNm:",strTitle.text)
           

#### Menu  implementation
def printMenu():
    print("\nWelcome! BoxOffice Movie Manager Program (xml version)") 
    print("========Menu==========")
    print("Load xml:  l")
    print("Print dom to xml: p")
    print("Quit program: q")
    print("print movie list: b")
    print("sEarch Daily BoxOffice list: e")
    print("Make html: m")
    print("==================")
    
def launcherFunction(menu):
    global BooksDoc
    if menu ==  'l':
       # extractBookData(strXml)
        BooksDoc = LoadXMLFromFile()
    elif menu == 'q':
        QuitBookMgr()
    elif menu == 'p':
        PrintDOMtoXML()
    elif menu == 'b':
       PrintBookList(["publisher",])
   # elif menu == 'a':
    #    ISBN = str(input ('insert ISBN :'))
     #   title = str(input ('insert Title :'))
    #    AddBook({'ISBN':ISBN, 'title':title})
    elif menu == 'e':
        date = str(input ('input date to search :'))
        getBookDataFromISBN(date)
      #  printBookList(SearchBookTitle(keyword))
    elif menu == 'm':
        keyword = str(input ('input keyword code to the html  :'))
        html = MakeHtmlDoc(SearchBookTitle(keyword))
        print("-----------------------")
        print(html)
        print("-----------------------")
    else:
        print ("error : unknow menu key")        
        
        
 #### xml function implementation
def LoadXMLFromFile():
    fileName = str(input ("please input file name to load :"))  # 읽어올 파일경로를 입력 받습니다.
    global xmlFD
 
    try:
        xmlFD = open(fileName)   # xml 문서를 open합니다.
    except IOError:
        print ("invalid file name or path")
        return None
    else:
        try:
            dom = parse(xmlFD)   # XML 문서를 파싱합니다.
        except Exception:
            print ("loading fail!!!")
        else:
            print ("XML Document loading complete")
            return dom
    return None       
        
        
def QuitBookMgr():
    global loopFlag
    loopFlag = 0
    BooksFree()
    
def BooksFree():
    if checkDocument():
        BooksDoc.unlink()
    
def PrintDOMtoXML():
    if checkDocument():
        print(BooksDoc.toxml())
     
     
def PrintBookList(tags):
    global BooksDoc
    if not checkDocument():
       return None
        
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
    retlist = []
    if not checkDocument():
        return None
        
    try:
        tree = ElementTree.fromstring(str(BooksDoc.toxml()))
    except Exception:
        print ("Element Tree parsing Error : maybe the xml document is not corrected.")
        return None
    
    #get Book Element
    bookElements = tree.getiterator("book")  # return list type
    for item in bookElements:
        strTitle = item.find("title")
        if (strTitle.text.find(keyword) >=0 ):
            retlist.append((item.attrib["ISBN"], strTitle.text))
    
    return retlist
    
    
                   
def printBookList(blist):
    for res in blist:
        print (res)
        
        
def checkDocument():
    global BooksDoc
    if BooksDoc == None:
        print("Error : Document is empty")
        return False
    return True
        
        
def MakeHtmlDoc(BookList):
    from xml.dom.minidom import getDOMImplementation
    #get Dom Implementation
    impl = getDOMImplementation()
    
    newdoc = impl.createDocument(None, "html", None)  #DOM 객체 생성
    top_element = newdoc.documentElement
    header = newdoc.createElement('header')
    top_element.appendChild(header)

    # Body 엘리먼트 생성.
    body = newdoc.createElement('body')

    for bookitem in BookList:
        #create bold element
        b = newdoc.createElement('b')
        #create text node
        ibsnText = newdoc.createTextNode("ISBN:" + bookitem[0])
        b.appendChild(ibsnText)

        body.appendChild(b)
    
        # BR 태그 (엘리먼트) 생성.
        br = newdoc.createElement('br')

        body.appendChild(br)

        #create title Element
        p = newdoc.createElement('p')
        #create text node
        titleText= newdoc.createTextNode("Title:" + bookitem[1])
        p.appendChild(titleText)

        body.appendChild(p)
        body.appendChild(br)  #line end
         
    #append Body
    top_element.appendChild(body)
    
    return newdoc.toxml()
        
        
        
        
##### run #####
while(loopFlag > 0):
    printMenu()
    menuKey = str(input ('select menu :'))
    launcherFunction(menuKey)
else:
    print ("Thank you! Good Bye")