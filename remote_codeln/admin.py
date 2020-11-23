from django.contrib import admin

# Register your models here.

from remote_codeln.models import RemoteProject, EscrowPayment, Bid, Issue, Comment, Chat

@admin.register(RemoteProject)
class RemoteProject(admin.ModelAdmin):
    pass

@admin.register(EscrowPayment)
class EscrowPaymentAdmin(admin.ModelAdmin):
    pass

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    pass

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass