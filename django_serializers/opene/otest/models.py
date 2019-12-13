from django.db import models



class Test(models.Model):
    name = models.CharField(u'名称', max_length=50, null=False, blank=False, unique=True)
    name2 = models.CharField(u'名称2', max_length=50, null=True, blank=True, default='')
    email = models.CharField(u'邮箱', max_length=50, null=False, blank=False, db_index=True)
    order_no = models.CharField(u'订单号', max_length=50, null=False, blank=False, db_index=True)
    province = models.CharField(u'省/州',max_length=50, null=True, default='', blank=True)  # 省/州
    amount = models.DecimalField(u'订单金额', default=0, decimal_places=2, max_digits=10)  # 订单金额
    permmisson = models.IntegerField(u'权限', default=1, choices=((1, u"查看"), (2, u"编辑")))
    disabled = models.IntegerField(u'模式', default=0)
    created = models.DateTimeField(u'创建时间', auto_now_add=True)
    updated = models.DateTimeField(u'更新时间', auto_now=True)

    class Meta:
        # managed = False
        db_table = 'test'
        unique_together = (('email', 'order_no'),)
        verbose_name = u'测试'
