from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name = 'home-page'),
    #path('', views.home, name = 'home-page'),
    path('classifier', views.classifier, name = 'classifier-page'),
    path('about', views.about, name = 'about-page'),
    path('classifier_results', views.classifier_results, name = 'classifier-results'),
    path('classifier_non_correct_results', views.classifier_non_correct_results, name = 'classifier-non-correct-results'),
    path('progress_main', views.progress_main, name = 'progress-main'),
    path('register', views.register, name = 'register-page'),
    path('login', auth_views.LoginView.as_view(template_name = 'Material_Classifier/login.html'), name = 'login-page'),#alternative ways of using built-in classbsaed views
    path('logout', auth_views.LogoutView.as_view(template_name = 'Material_Classifier/logout.html'), name = 'logout-page'),
    path('profile', views.profile, name = 'profile-page'),
    path('incentive_main', views.incentive_main, name = 'incentive-main-page'),
    path('social_main', views.social_main, name = 'social-main-page'),
    path('settings_page', views.settings_page, name = 'settings-page'),
    path('useful_locations', views.useful_locations, name = 'useful-locations-page'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)