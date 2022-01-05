from django.contrib import admin
from .models import Profile, ItemClassificationPicture, ItemClassificationResults, NewsFeed,IncentiveOffers, UsefulLinks, Inquieries
# Register your models here.

admin.site.register(Profile)
admin.site.register(ItemClassificationResults)
admin.site.register(ItemClassificationPicture)
admin.site.register(NewsFeed)
admin.site.register(IncentiveOffers)
admin.site.register(UsefulLinks)
admin.site.register(Inquieries)