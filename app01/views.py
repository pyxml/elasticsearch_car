from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from app01.models import News, Tag
from bs4 import BeautifulSoup
import requests
from elasticsearch import Elasticsearch
from utils import es
import uuid
from utils.pagination import Pagination


def home(request):
	return redirect(reverse("search"))


def spider(request):
	''' 爬虫存数据'''
	for i in range(31, 41):
		response = requests.get(url="https://www.autohome.com.cn/news/{}/#liststart".format(i))
		soup = BeautifulSoup(response.text, "html.parser")
		div_obj = soup.find(name="div", attrs={"id": "auto-channel-lazyload-article"})
		li_obj = div_obj.find_all(name="li")
		tag = Tag.objects.filter(pk=4).first()

		for items in li_obj:
			title_obj = items.find(name="h3")
			if not title_obj: continue
			a_url = "https" + items.find(name='a').get("href")
			title = items.find(name="h3").text
			summery = items.find(name="p").text.split()[-1]
			action_type = tag.tag
			a_uuid = uuid.uuid4()
			News.objects.create(a_url=a_url, title=title, desc=summery, action_type=tag, a_uuid=a_uuid)
			es.add_es(title, a_url, summery, action_type, a_uuid)

	return HttpResponse("OK")


def search(request):
	tags = Tag.objects.all()
	if request.method == "POST":

		search_msg = request.POST.get("search_msg")
		action_type = request.POST.get("action_type")
		page = request.POST.get("page_num")

		if action_type == "全部":
			action_type = "文章 新闻 问答 头条"

		res = es.filter_es(action_type, search_msg)

		pager = Pagination(page, res["hits"]["total"], 10)
		data = {"total_num": res["hits"]["total"],
				"total_data": res["hits"]["hits"][pager.start:pager.end],
				"page_data": pager.page_html
				}

		return JsonResponse(data)

	return render(request, "search.html", {"tags": tags})


def detail(request, detail):
	news_obj = News.objects.filter(a_uuid=detail).first()

	return render(request, "detail.html", {"obj": news_obj})


def my_suggest(request):
	if request.method == "POST":
		search_msg = request.POST.get("search_msg")
		res = es.suggest_es(search_msg)
		return JsonResponse({"res": res})
	return HttpResponse("nonono")
