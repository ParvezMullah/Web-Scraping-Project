from django.shortcuts import render
from django.http import HttpResponse


from bs4 import BeautifulSoup
import requests 
from collections import OrderedDict
import json


top_posts_list = OrderedDict()

def get_top_links(tag):
    global top_posts_list
    top_posts_list = OrderedDict()
    url = 'https://medium.com/tag/' + tag
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    container = soup.find('div', class_ ='js-tagStream')
    for div in container:
        anchor_tag = div.find('a', class_='link link--darken')
        post_link = (anchor_tag.get('data-action-value')).split('?source')[0]
        post_title = div.find('h3', class_='graf graf--h3 graf-after--figure graf--trailing graf--title')
        if post_title == None:
            post_title = div.find('h3', class_="graf graf--h3 graf-after--figure graf--title")
        nonBreakSpace = u'\xa0'
        if post_title is None:
            continue
        post_title = (post_title.text).replace(nonBreakSpace, ' ')
        post_author = (div.find('a', class_='ds-link ds-link--styleSubtle link link--darken link--accent u-accentColor--textNormal u-accentColor--textDarken')).text
        post_read = (div.find('span', class_='readingTime')).get('title')
        post_details = div.find('time').text +', ' + str(post_read)
        top_posts_list[post_link]= (post_link, post_title, post_author, post_details)
    return top_posts_list



def get_post_details(post_list_detail):
    (post_link, post_title, post_author, post_detail) = (post_list_detail)
    post_detail_view = {}
    source = requests.get(post_link).text
    soup = BeautifulSoup(source, 'lxml')
    post_detail_view['source_url'] = post_link
    post_detail_view['author_name'] = post_author
    post_detail_view['title'] = post_title
    post_detail_view['details'] = post_detail
    post_detail_view['blog'] = (soup.find('div', class_='section-inner sectionLayout--insetColumn')).text
    (soup.find('h1')).decompose()
    tags = soup.findAll('a', class_='link u-baseColor--link')
    post_detail_view['tags'] = [a.text for a in tags]
    try:
        post_detail_view['responses'] = (soup.find('button', class_='button button--chromeless u-baseColor--buttonNormal')).text
    except:
        post_detail_view['responses'] = 0
    return post_detail_view



def home(request):
    global top_posts_list
    paginate_by = 10
    template_name = 'mediumscrapingapp/index.html'
    tag = request.GET.get('txtSearch', None)
    if request.method == 'GET' and tag is not None:
        get_top_links(tag)    
        return render(request, template_name, {'posts': top_posts_list})
    return render(request, template_name)



def details(request, post):
     global top_posts_list
     template_name = 'mediumscrapingapp/details.html'
     source_url = (request.get_full_path()).split('details/')[1]
     post = get_post_details(top_posts_list[source_url])
     return render(request, template_name, {'post': post})