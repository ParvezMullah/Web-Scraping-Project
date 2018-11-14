from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from .serilalizers import PostSerializer

from selenium import webdriver
from bs4 import BeautifulSoup
import requests 
from collections import OrderedDict
import json

container = None


def get_top_links(tag, post_number):
    global container
    size = 0
    top_posts = {}

    if container is None or post_number == 0:
        url = 'https://medium.com/tag/' + tag
        source = requests.get(url).text
        driver = webdriver.PhantomJS('C:\\Users\\parvez\\Desktop\\Scraping Project\\mediumscrapingapp\\phantomjs')
        # Load Twitter page and click to view all results
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        container = soup.findAll('div', class_ ='streamItem streamItem--postPreview js-streamItem')
        size = len(container)

    try:
        div = container[post_number]
    except  IndexError:
        top_posts['post_link'] = "None"
        top_posts['post_title'] = "None"
        top_posts['post_author'] = "None"
        top_posts['post_details'] = "None"
        return top_posts
    anchor_tag = div.find('a', class_='link link--darken')
    post_link = (anchor_tag.get('data-action-value')).split('?source')[0]
    post_title = div.find('h3', class_='graf graf--h3 graf-after--figure graf--trailing graf--title')
    if post_title == None:
        post_title = div.find('h3', class_="graf graf--h3 graf-after--figure graf--title")
    nonBreakSpace = u'\xa0'
    if post_title is None:
        post_title = div.find('h3', class_="graf graf--h3 graf--leading graf--title")
    post_title = (post_title.text).replace(nonBreakSpace, ' ')
    post_author = (div.find('a', class_='ds-link ds-link--styleSubtle link link--darken link--accent u-accentColor--textNormal u-accentColor--textDarken')).text
    post_read = (div.find('span', class_='readingTime')).get('title')
    post_details = div.find('time').text +', ' + str(post_read)
    top_posts['post_link'] = post_link
    top_posts['post_title'] = post_title
    top_posts['post_author'] = post_author
    top_posts['post_details'] = post_details

    if post_number == 9 or post_number == size - 1:
        container = []
    return top_posts




def get_post_details(url):
    post_detail_view = {}
    # source = requests.get(post_link).text
    source = url.split('details/')[-1]
    post_title = (source.split('/')[-1]).split('-')[:-1]
    post_detail_view['title'] = ' '.join(post_title)  
    post_detail_view['source_url'] = source  
    
    driver = webdriver.PhantomJS('C:\\Users\\parvez\\Desktop\\Scraping Project\\mediumscrapingapp\\phantomjs')
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    soup = BeautifulSoup(driver.page_source, 'html5lib')

    post_detail_view['details'] = soup.find('span',attrs={'class':'readingTime'})['title']
    post_detail_view['blog'] = soup.find('div', class_='section-content')
    print(post_detail_view['blog'])
    #post_detail_view['title'] = (soup.find('h1', class_='graf graf--h3 graf--leading graf--title')).text
    # (soup.find('h1')).decompose()
    tags = soup.findAll('a', class_='link u-baseColor--link')
    post_detail_view['tags'] = [a.text for a in tags]
    return post_detail_view




def home(request):
    global top_posts_list
    template_name = 'mediumscrapingapp/index.html'
    # tag = request.GET.get('txtSearch', None)
    # if request.method == 'GET' and tag is not None:
    #     get_top_links(tag)  
    #     posts = json.dumps(top_posts_list)
    #     print(posts)  
    #     return render(request, template_name, {'data': posts})
    return render(request, template_name)


class Home(APIView):
    serializer_class = PostSerializer
    template_name = 'mediumscrapingapp/index.html'
    
    def get(self, request, format=None):
        tag = request.GET.get('txtSearch')
        post_number = int(request.GET.get('post_number'))
        top_posts = get_top_links(tag, post_number)
        serializer = PostSerializer(top_posts)
        return Response(serializer.data, template_name = 'mediumscrapingapp/index.html')
    

def details(request, post):
     template_name = 'mediumscrapingapp/details.html'
     source_url = (request.get_full_path()).split('details/')[1]
     post = get_post_details(source_url)
     return render(request, template_name, {'post': post})

