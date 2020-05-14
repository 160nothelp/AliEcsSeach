from django.contrib import admin

from .models import GtmCheckDomain, AliRamLink, GtmDefaultLine, TmpCytMerchNginx, CreateShadowSocketTemplate, \
    CreateForwardTemplate


admin.site.register(GtmCheckDomain)
admin.site.register(AliRamLink)
admin.site.register(GtmDefaultLine)
admin.site.register(TmpCytMerchNginx)
admin.site.register(CreateShadowSocketTemplate)
admin.site.register(CreateForwardTemplate)
