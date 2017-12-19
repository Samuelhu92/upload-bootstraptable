# -*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from .models import Fund,Trade,TreeNode
from django.views.decorators.csrf import csrf_exempt
from .forms import UploadFileForm
from django.views.generic.edit import FormView
from datetime import date
from xlrd import XLRDError

import json
import xlrd

def upload(request):
    if request.method == 'GET':
        return render(request, 'fund/upload.html')

def FileFieldView(request):
    if request.is_ajax() and request.method == 'POST':
        files = request.FILES.getlist('file')
        totall = len(files)
        is_valid = True
        invalid = []
        for f in files:
            try:
                wb = xlrd.open_workbook(
                            filename=None,
                            file_contents=f.read()
                                    )
                table = wb.sheet_by_name(u'今日成交')
                nrows = table.nrows
                datemode = int(wb.datemode)
                for row in range(1,nrows):
                    id = int(table.row(row)[0].value)
                    try:
                        Trade.objects.get(id=id)
                        continue
                    except Trade.DoesNotExist:
                        year,month,day = xlrd.xldate.xldate_as_tuple(int(table.row(row)[1].value),datemode)[0:3]
                        accountid = table.row(row)[2].value
                        type = table.row(row)[3].value
                        code = table.row(row)[4].value
                        name = table.row(row)[5].value
                        dealprice = table.row(row)[6].value
                        amount = table.row(row)[7].value
                        tradeinfo = Trade(
                            id=id,
                            date=date(year,month,day),
                            accountid=accountid,
                            type=type,
                            code=code,
                            name=name,
                            dealprice=dealprice,
                            amount=amount,
                        )
                        tradeinfo.save(force_insert=True)
            except XLRDError:
                is_valid=False
                invalid.append(f.name)
        if not is_valid:
            if totall > len(invalid):
                return HttpResponse(u"除了非法文件(%s)，剩余文件成功上传。" % invalid)
            else:
                return HttpResponse("文件非法，上传失败。")
        else:
            return HttpResponse("上传成功。%s")
    else:
        return render(request, 'fund/upload.html')


# class FileFieldView(FormView):
#     form_class = UploadFileForm
#     template_name = 'fund/upload.html'
#     success_url = '../upload/success/'
#
#     def post(self,request,*args,**kwargs):
#
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         files = request.FILES.getlist('excel')
#         is_valid=True
#         invalid=[]
#
#         if files:
#             for f in files:
#                 try:
#                     wb = xlrd.open_workbook(
#                         filename=None,
#                         file_contents=f.read()
#                     )
#                     table = wb.sheet_by_name(u'今日成交')
#                     nrows = table.nrows
#                     datemode = int(wb.datemode)
#                     for row in range(1,nrows):
#                         id = int(table.row(row)[0].value)
#                         try:
#                             Trade.objects.get(id=id)
#                             continue
#                         except Trade.DoesNotExist:
#                             year,month,day = xlrd.xldate.xldate_as_tuple(int(table.row(row)[1].value),datemode)[0:3]
#                             accountid = table.row(row)[2].value
#                             type = table.row(row)[3].value
#                             code = table.row(row)[4].value
#                             name = table.row(row)[5].value
#                             dealprice = table.row(row)[6].value
#                             amount = table.row(row)[7].value
#                             tradeinfo = Trade(
#                                 id=id,
#                                 date=date(year,month,day),
#                                 accountid=accountid,
#                                 type=type,
#                                 code=code,
#                                 name=name,
#                                 dealprice=dealprice,
#                                 amount=amount,
#                             )
#                             tradeinfo.save(force_insert=True)
#                 except XLRDError:
#                     is_valid=False
#                     invalid.append(f.name)
#             if not is_valid:
#                 return HttpResponse(u"除了非法文件(%s)，剩余文件成功上传。" % invalid)
#             else:
#                 return self.form_valid(form)
#         else:
#             return self.form_invalid(form)


def successful(request):
    return render(request,'fund/success.html')




def get_tree(parents):
    tree = []
    for p in parents:
        node = TreeNode()
        node.id = p.id
        node.text = p.name
        childrenid = p.childfund
        if childrenid:
            node.isParent = True
            children = [Fund.objects.get(fundid=id) for id in childrenid.strip().split(',')]
            node.nodes = get_tree(children)
        tree.append(node.to_dict())
    return tree


def get_table(parents):
    table = []
    for p in parents:
        id = p.id
        fundid = p.fundid
        name = p.name
        fundtype = p.fundtype
        dateinception = p.dateinception
        datedue = p.datedue
        childfund = p.childfund
        channel = p.channel
        custodian = p.custodian
        producttype = p.producttype
        share = p.share
        nvmultipleier = p.nvmultipleier
        nvplus = p.nvplus
        manager = p.manager
        team = p.team
        priority = p.priority
        sortindex = p.sortindex
        splitratio = p.splitratio
        splitratio_pr = p.splitratio_pr
        splitration_temp = p.splitration_temp
        bonusthisyear = p.bounusthisyear
        table.append({
            'id': id,
            'fundid': fundid,
            'name': name,
            'fundtype': fundtype,
            'dateinception': dateinception,
            'datedue': datedue,
            'childfund': childfund,
            'channel': channel,
            'custodian': custodian,
            'producttype': producttype,
            'share': share,
            'nvmultipleier': nvmultipleier,
            'nvplus': nvplus,
            'manager': manager,
            'team': team,
            'priority': priority,
            'sortindex': sortindex,
            'splitratio': splitratio,
            'splitratio_pr': splitratio_pr,
            'splitration_temp': splitration_temp,
            'bonusthisyear': bonusthisyear,
             })
    return table





def fundtree(request):
    root = Fund.objects.filter(parentfund='')
    tree = get_tree(root)
    return JsonResponse(tree,safe=False)
@csrf_exempt
def fundchild(request,pk):
    pageSize = json.loads(request.body)["pageSize"]
    pageNo = json.loads(request.body)["pageNo"]
    root = Fund.objects.get(pk=pk)
    try:
        childs = [Fund.objects.get(fundid=id) for id in root.childfund.strip().split(',')]
        children = get_table(childs)
    except:
        children = []
    l = len(children)
    d = dict()
    d["total"] = l
    d["rows"] = children[(pageNo-1)*pageSize:pageNo*pageSize]
    return JsonResponse(d,safe=False)


@csrf_exempt
def fundparent(request):
    pageSize = json.loads(request.body)["pageSize"]
    pageNo = json.loads(request.body)["pageNo"]
    name = json.loads(request.body)["name"]
    id = json.loads(request.body)["id"]
    root = Fund.objects.filter(parentfund='')
    table = get_table(root)
    l = len(table)
    d = dict()
    d["total"] = l
    d["rows"] = table[(page-1)*pageSize:pageNo*pageSize]
    return JsonResponse(d,safe=False)

def fundinfo(request,pk):
    fund = Fund.objects.get(pk=pk)
    return render(request,'fund/fundinfo.html',{'fund':fund})


def show(request):
    parentfund = Fund.objects.filter(parentfund='')
    return render(request,'fund/show.html',{'fund':parentfund})






