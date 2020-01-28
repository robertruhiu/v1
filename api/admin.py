from django.contrib import admin

from  rest_framework_api_key.admin import APIKeyModelAdmin

from api.models import Enterprise, EnterpriseAPIKey, EnterpriseProject, EnterpriseDeveloper, EnterpriseDeveloperReport, \
    WebHookSubscriber


# Register your models here.

@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    pass


@admin.register(EnterpriseAPIKey)
class EnterpriseAPIKeyAdmin(APIKeyModelAdmin):
    pass


@admin.register(EnterpriseProject)
class EnterpriseProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(EnterpriseDeveloper)
class EnterpriseDeveloperAdmin(admin.ModelAdmin):
    pass


@admin.register(EnterpriseDeveloperReport)
class EnterpriseDeveloperReportAdmin(admin.ModelAdmin):
    pass


@admin.register(WebHookSubscriber)
class WebHookSubscriberAdmin(admin.ModelAdmin):
    pass
