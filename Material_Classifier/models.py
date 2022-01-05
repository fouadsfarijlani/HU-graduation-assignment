from django.db import models
from  django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
import datetime




# Create your models here.

class ItemClassificationPicture(models.Model):
    picture_title = models.CharField(blank=True, null=True, max_length=250)
    picture = models.ImageField(null = True, blank = True, upload_to = "images/")
    picture_path = models.CharField(null = True, blank = True, max_length=250)
 

    def __str__(self):
        return self.picture_path



class ItemClassificationResults(models.Model):
    combined_predicted_label = models.CharField(max_length=150,blank=True, null=True)
    densenet169_predicted_label = models.CharField(max_length=150,blank=True, null=True)
    inceptionresnet_predicted_label = models.CharField(max_length=150,blank=True, null=True)
    nasnetlarge_predicted_label = models.CharField(max_length=150,blank=True, null=True)
    combined_votes = models.IntegerField()
    item_picture = models.OneToOneField(ItemClassificationPicture, blank=True, null=True, on_delete=models.CASCADE)
    item_results_user = models.ForeignKey(User, blank=True, null = True, on_delete = models.CASCADE)
    is_correct = models.BooleanField(default=True)
    #added later by Fouad
    rectified_label = models.CharField(max_length = 150, default = 'N/A')
    marked_for_futur_training = models.BooleanField(default = False)
    #date_disposed = models.DateTimeField(default = timezone.now)
    date_disposed = models.DateField(default = datetime.date.today)
    #date_disposed = models.DateField(default = timezone.now)

    def __str__(self):
        return self.combined_predicted_label


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    address_line_1 = models.CharField(max_length = 200)
    address_line_2 = models.CharField(max_length = 200)
    city_of_residence = models.CharField(max_length = 150)
    zip_code = models.CharField(max_length = 100)
    

    def __str__(self):
        return f'{self.user.username} Profile'

class NewsFeed(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    region = models.CharField(max_length=100)
    is_governmental = models.BooleanField(default = False)
    is_event = models.BooleanField(default = False)

    def __str__(self):
        return self.title

class IncentiveOffers(models.Model):
    
    offer_title = models.CharField(max_length=150)
    offer_image_path = models.CharField(max_length = 200, blank = True)
    offer_type = models.CharField(max_length=150)
    offer_content = models.TextField()
    offer_region = models.CharField(max_length=150)
    offer_date_start = models.DateField()
    offer_date_end = models.DateField()
    offer_is_active = models.BooleanField()
    #offer_users = models.ForeignKey(User, on_delete = models.CASCADE, blank =True)

    def __str__(self):
        return self.offer_title


class UsefulLinks(models.Model):
    
    region = models.CharField(max_length=150)
    municipality_link = models.CharField(max_length=250)
    extra_link_1 = models.CharField(max_length = 250, blank=True)
    extra_link_1 = models.CharField(max_length = 250, blank=True)

    def __str__(self):
        return self.region

class Inquieries(models.Model):
    inquery_title = models.CharField(max_length = 250)
    inquery_content = models.TextField()
    inquery_post_date = models.DateTimeField(default = timezone.now)
    is_open = models.BooleanField(default = True)

    def __str__(self):
        return self.inquery_title

#class Post(models.Model):
#    title = models.CharField(max_length = 100)
#    content = models.TextField()
#    date_posted = models.DateTimeField(default=timezone.now)
#    author = models.ForeignKey(User, on_delete=models.CASCADE)

 #   def __str__(self):
 #       return self.title

    