import urllib.request as url_request
from bs4 import BeautifulSoup as soup
import pandas as pd
import xlsxwriter
dictionary_modifyed_for_sheets={}
def url_connection(url):
    url_open=url_request.urlopen("https://github.com"+url)
    url_read=url_open.read()
    url_open.close()
    url_souped = soup(url_read, 'html.parser')
    return url_souped
#Tranding_(Today,Weekly)
def repositorys_listing(url,sheet):
    url_souped=url_connection(url)
    listed_repositorys=url_souped.findAll("li",{"class":"col-12 d-block width-full py-4 border-bottom"})
    i=0
    repository_name_list=[]
    owner_name_list=[]
    repository_commit_list=[]
    repository_link_list=[]
    repository_watch_list = []
    repository_star_list = []
    for repositorys in listed_repositorys:
        # Repository name
        full_name_str=listed_repositorys[i].div.a["href"]
        repository_name_list_temp=full_name_str.split("/")
        #for file
        repository_name_list.append(repository_name_list_temp[-1])

        # Owner Name
        #for file
        owner_name_list.append(repository_name_list_temp[1])

        url_souped1 = url_connection(full_name_str)
        # Repository commits
        no_commits = url_souped1.findAll("li", {"class": "commits"})
        # Convert String To Int{
        temp_0 = no_commits[0].a.span.text.split("\n")
        temp_0 = temp_0[1].split(" ")
        temp_0 = temp_0[-1].split(",")
        commit_value = "".join(temp_0)
        # }
        # for file
        repository_commit_list.append(int(commit_value))

        # Repository Watch
        no_watch = url_souped1.findAll("ul", {"class": "pagehead-actions"})
        # print(no_watch[0].li.text)
        # Convert String To Int{
        temp_1 = no_watch[0].li.text.split("\n")
        temp_1=temp_1[-3].split(" ")
        temp_1=temp_1[-1].split(",")
        watch_value = "".join(temp_1)
        # }
        # for file
        repository_watch_list.append(int(watch_value))

        # Repository Star
        no_star = url_souped1.findAll("a", {"class": "social-count js-social-count"})
        # Convert String To Int{
        temp_2 = no_star[0].text.split("\n")
        temp_2 = temp_2[-2].split(" ")
        temp_2 = temp_2[-1]..split(",")
        star_value = "".join(temp_2)
        # }
        # for file
        repository_star_list.append(int(star_value))

        # Repository Link
        #for file
        repository_link_list.append("https://github.com"+full_name_str)

        i+=1
    #for file
    dictionary_for_data={'Repository Name':repository_name_list,'Owner Name':owner_name_list,'Commits':repository_commit_list,'Watch':repository_watch_list,'Star':repository_star_list,'repository Links':repository_link_list}
    data_frame=pd.DataFrame(dictionary_for_data)
    dictionary_modifyed_for_sheets[sheet]=data_frame
def file_saving():
    # Writing Data To Excel Sheet
    writer = pd.ExcelWriter('GitHub_Tranding.xlsx', engine='xlsxwriter')
    for sheet_name in dictionary_modifyed_for_sheets.keys():
        dictionary_modifyed_for_sheets[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()
def Today_Tranding():
    url="/trending?since=daily"
    sheet='Today'
    print("-------------------------------\nToday Tranding\n-------------------------------\n\n")
    repositorys_listing(url,sheet)
def Weekly_Tranding():
    url="/trending?since=weekly"
    sheet='Weekly'
    print("-------------------------------\nWeekly Tranding\n-------------------------------\n\n")
    repositorys_listing(url,sheet)
#main
Today_Tranding()
Weekly_Tranding()
file_saving()
