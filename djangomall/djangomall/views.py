# -*- coding: utf-8 -*-
# __author__="jiajun.zhu"
# DATE:2020/4/24
from django.shortcuts import render_to_response


def index(request):
    return render_to_response("index.html")