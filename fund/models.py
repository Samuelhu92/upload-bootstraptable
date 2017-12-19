#-*- coding:utf-8 -*-
from django.db import models

# Create your models here.
class Fund(models.Model):
    #编号
    id = models.IntegerField(primary_key=True)
    #基金编号
    fundid = models.CharField(max_length=100,blank=True)
    #基金名称
    name = models.CharField(max_length=100,blank=True)
    #基金类型0 一般基金1 母基金（物理切分类）10 子基金（物理切分类）2 母基金（虚拟切分类）20 子基金（虚拟切分类）
    fundtype = models.IntegerField(null=True,blank=True)
    #母基金
    parentfund = models.CharField(max_length=100,blank=True)
    #子基金列表
    childfund = models.CharField(max_length=100,blank=True)
    #基金成立日
    dateinception = models.DateField(null=True,blank=True)
    #基金到期日
    datedue = models.DateField(null=True,blank=True)
    #通道机构
    channel = models.CharField(max_length=100,blank=True)
    #托管人
    custodian = models.CharField(max_length=100,blank=True)
    #产品类型 对冲、纯多
    producttype = models.CharField(max_length=100,blank=True)
    #份额
    share = models.DecimalField(max_digits=18,decimal_places=2,null=True,blank=True)
    #净值乘数
    nvmultipleier = models.DecimalField(max_digits=18,decimal_places=6,null=True,blank=True)
    #净值加数
    nvplus = models.DecimalField(max_digits=18,decimal_places=6,null=True,blank=True)
    #基金经理
    manager = models.CharField(max_length=100,blank=True)
    #业务组 1,2,3,4,
    team = models.IntegerField(null=True,blank=True)
    #优先级
    priority = models.IntegerField(null=True,blank=True)
    #排序编号
    sortindex = models.IntegerField(null=True,blank=True)
    #子基金占比
    splitratio = models.DecimalField(max_digits=18,decimal_places=8,null=True,blank=True)
    #申赎分割比例
    splitratio_pr = models.DecimalField(max_digits=18, decimal_places=8,null=True,blank=True)
    #临时申赎分割比例
    splitration_temp = models.DecimalField(max_digits=18, decimal_places=8,null=True,blank=True)
    #今年分红
    bounusthisyear = models.DecimalField(max_digits=18, decimal_places=8,null=True,blank=True)

class Trade(models.Model):
    #编号
    id = models.IntegerField(primary_key=True)
    #交易日期
    date = models.DateField(null=True,blank=True)
    #基金编号
    accountid = models.CharField(max_length=100,blank=True)
    #证券类型
    type = models.CharField(max_length=100,blank=True)
    #证券编码
    code = models.CharField(max_length=100,blank=True)
    #证券名称
    name = models.CharField(max_length=100,blank=True)
    #成交价格
    dealprice = models.DecimalField(max_digits=18,decimal_places=6,null=True,blank=True)
    #成交数量
    amount  =models.IntegerField(null=True,blank=True)


class TreeNode:
    def __init__(self):
        self.id = 0
        self.isParent = False
        self.text = "Node 1"
        self.href = "#node-1"
        self.selectable = True
        self.state = {
            'checked':False,
            'disabled': True,
            'expanded': False,
            'seleced': False,
        }
        self.tag = ['available']
        self.nodes = []

    def to_dict(self):
        icon = (self.isParent and 'glyphicon glyphicon-home' or 'glyphicon glyphicon-user')
        l = str(len(self.nodes))
        return {
            'id':self.id,
            'text': self.text,
            'icon': icon,
            'href': self.href,
            'tags': [l],
            'nodes':self.nodes,
        }

class FundNode():
    def __init__(self):
        self.id = 0
        self.isParent = False
        self.text = "Node 1"
        self.href = "#node-1"
        self.selectable = True
        self.state = {
            'checked': False,
            'disabled': True,
            'expanded': False,
            'seleced': False,
        }
        self.tag = ['available']
        self.nodes = []

    def to_dict(self):
        l = str(len(self.nodes))
        return {
            'id': self.id,
            'text': self.text,
            'icon': icon,
            'href': self.href,
            'tags': [l],
            'nodes': self.nodes,
        }
