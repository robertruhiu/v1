from django.contrib import admin

from servermanagement.models import Job, Server, ServerConfig, CandidateSetup, IdeFactory
    # , EnterpriseCandidateSetup, EnterpriseJob


# Project

# Register your models here

class JobAdmin(admin.ModelAdmin):
    pass
    # readonly_fields = ('time',)


# class ProjectAdmin(admin.ModelAdmin):
#     pass
class ServerAdmin(admin.ModelAdmin):
    pass


class ServerConfigAdmin(admin.ModelAdmin):
    pass


class CandidateSetupAdmin(admin.ModelAdmin):
    pass


class IdeFactoryAdmin(admin.ModelAdmin):
    pass


class EnterpriseJobAdmin(admin.ModelAdmin):
    pass


class EnterpriseCandidateSetupAdmin(admin.ModelAdmin):
    pass


admin.site.register(Job, JobAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(ServerConfig, ServerConfigAdmin)
admin.site.register(CandidateSetup, CandidateSetupAdmin)
admin.site.register(IdeFactory, IdeFactoryAdmin)
# admin.site.register(EnterpriseJob, EnterpriseJobAdmin)
# admin.site.register(EnterpriseCandidateSetup, EnterpriseCandidateSetupAdmin)
