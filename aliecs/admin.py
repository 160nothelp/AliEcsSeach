from django.contrib import admin


from .models import AliUserAccessKey, OtherPlatforms, OtherPlatformsHosts


# 设置admin后台只读字段
@admin.register(OtherPlatforms)
class OtherPlatformsAdmin(admin.ModelAdmin):
    readonly_fields = ['the_other', ]
    actions = None


admin.site.register(AliUserAccessKey)
admin.site.register(OtherPlatformsHosts)

