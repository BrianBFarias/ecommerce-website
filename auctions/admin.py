from django.contrib import admin
from .models import User, Item, Watchlist, Bid, Message, Item_Message_Group

class WatchlistAdmin(admin.ModelAdmin):
    filter_horizontal = ("watchlist",)

class MessagesAdmin(admin.ModelAdmin):
    filter_horizontal = ("messages",)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'closed')

admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Item)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Item_Message_Group, MessagesAdmin)
admin.site.register(Message)

# Register your models here.
