from django.shortcuts import render

from bs4 import BeautifulSoup
import requests 
from collections import OrderedDict
import json



def get_top_links(tag):
    post_links = OrderedDict()
    url = 'https://medium.com/tag/' + tag
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    container = soup.find('div', class_ ='js-tagStream')
    i = 0
    for div in container:
        anchor_tag = div.find('a', class_='link link--darken')
        post_link = anchor_tag.get('data-action-value')
        post_author = (div.find('a', class_='ds-link ds-link--styleSubtle link link--darken link--accent u-accentColor--textNormal u-accentColor--textDarken')).text
        read = (div.find('span', class_='readingTime')).get('title')
        details = div.find('time').text +', ' + str(read)
        post_links[post_link] = [post_author, details]
        i += 1
        if i == 10:
            break
    return post_links



def get_post_details(link, author):
    details = {}
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml')
    details['author_name'] = author[0]
    nonBreakSpace = u'\xa0'
    title = (soup.find('h1')).text
    details['title'] = title.replace(nonBreakSpace, ' ')
    details['details'] = author[1]
    details['blog'] = (soup.find('div', class_='section-inner sectionLayout--insetColumn')).text
    (soup.find('h1')).decompose()
    tags = soup.findAll('a', class_='link u-baseColor--link')
    details['tags'] = [a.text for a in tags]
    try:
        details['responses'] = (soup.find('button', class_='button button--chromeless u-baseColor--buttonNormal')).text
    except:
        details['responses'] = 0
    return details



def get_all_post_details(top_posts_links):
    post_details = OrderedDict()
    for link in top_posts_links.keys():
        post_details[link] = get_post_details(link, top_posts_links[link])
    return post_details



def home(request):
    template_name = 'mediumscrapingapp/index.html'
    if request.method == 'GET':
        all_post = ''
        tag = request.GET.get('txtSearch', None)
        if tag is not None:
            top_posts_links = get_top_links(tag)
            top_posts_details = get_all_post_details(top_posts_links)
            return render(request, template_name, {'posts' : top_posts_details})
    return render(request, template_name)