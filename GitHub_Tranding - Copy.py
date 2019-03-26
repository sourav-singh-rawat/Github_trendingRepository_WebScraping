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
#Tranding_(Today,Weekly,Montly)
def repositorys_listing(url,sheet):
    url_souped=url_connection(url)
    listed_repositorys=url_souped.findAll("li",{"class":"col-12 d-block width-full py-4 border-bottom"})
    i=0
    repository_name_list=[]
    owner_name_list=[]
    repository_commit_list=[]
    repository_link_list=[]
    repository_review_list=[]
    for repositorys in listed_repositorys:
        #repository name
        full_name_str=listed_repositorys[i].div.a["href"]
        repository_name_list_temp=full_name_str.split("/")
        #print("repository Name: "+repository_name_list_temp[1])
        #for file
        repository_name_list.append(repository_name_list_temp[-1])
        owner_name_list.append(repository_name_list_temp[1])
        #repository commits
        url_souped1=url_connection(full_name_str)
        no_commits=url_souped1.findAll("li",{"class":"commits"})

        commit_value_temp=no_commits[0].a.span.text
        temp1=commit_value_temp.split("\n")
        final_commit_value_temp2=temp1[1].split(" ")
        #print("Commits: "+final_commit_value_temp2[-1])
        #convert string commits to int
        temp_0=final_commit_value_temp2[-1].split(",")
        temp_0="".join(temp_0)
        # for file
        #comments
        if int(temp_0)>=500:
            repository_review_list.append("Excellent")
        elif (int(temp_0)<=500 and int(temp_0)>=200):
            repository_review_list.append("Good")
        else:
            repository_review_list.append("Bad")

        repository_commit_list.append(int(temp_0))

        #print("repository Link: https://github.com"+full_name_str+"\n")
        #for file
        repository_link_list.append("https://github.com"+full_name_str)

        i+=1
    #for file
    dictionary_for_data={'Repository Name':repository_name_list,'Owner Name':owner_name_list,'Commits':repository_commit_list,'Review':repository_review_list,'repository Links':repository_link_list}
    data_frame=pd.DataFrame(dictionary_for_data)
    dictionary_modifyed_for_sheets[sheet]=data_frame
    #print(dictionary_modifyed_for_sheets)
def file_saving():
    # for file
    # print(dictionary_modifyed_for_sheets)
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