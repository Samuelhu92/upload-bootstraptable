# -*- coding:utf-8 -*-
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_excel_file(value):
    suffix = value.name.split('.')[-1]
    if suffix not in ['xls', 'xlsx']:
        raise ValidationError(
            _('%(value)s 不是一个合法的excel文件 '),
            params={'value':value}
        )

