from django.contrib import admin
from tikets import models


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'status')
    list_filter = ('status',)


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('support', 'created_at')


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('answer', 'user')
