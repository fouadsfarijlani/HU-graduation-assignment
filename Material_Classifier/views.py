from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ItemClassificationPicture, ItemClassificationResults, NewsFeed, Profile, IncentiveOffers, UsefulLinks, Inquieries
from .forms import ImageClassificationForm, UserRegisterForm, ImageClassificationRectifiedResults
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os
from .tf_functions import prepare_images, load_candidate_models, combined_prediction
from .misc_functions import open_json, write_json, move_images, DisposalBin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime

#def home(request):
#    return HttpResponse('<h1>Material Classifier Page</h1>')


densenet_path = "Material_Classifier/static/Material_Classifier/tf_models/densenet169_model.h5"
inceptionresnet_path = "Material_Classifier/static/Material_Classifier/tf_models/inceptionresnet_model.h5"
nasnetlarge_path = "Material_Classifier/static/Material_Classifier/tf_models/nasnetlarge_model.h5"

densenet169, inceptionresnet, nasnetlarge = load_candidate_models(densenet_path, inceptionresnet_path, nasnetlarge_path)

material_labels = {0:'Cardboard', 1:'Chips Bag', 2:'Drinking Carton', 3:'Glass Bottle',
                   4:'Glass Cup', 5:'Metal Can', 6:'Organic', 7:'Paper', 8:'Plastic Bag',
                   9:'Plastic Bottle', 10:'Plastic Box', 11:'Plastic Round Container'}




def useful_locations(request):
    option_selected = ""
    if request.method == "POST":
        option_selected = request.POST.get("location-selection")
        return render(request, 'Material_Classifier/useful_locations.html', {"option_selected":option_selected})
    return render(request, 'Material_Classifier/useful_locations.html')

def settings_page(request):
    if request.method == "POST":
        messages.success(request, f'Your preferences has been saved. Now its your turn to save the world')
        return HttpResponseRedirect(reverse('home-page'))
    return render(request, 'Material_Classifier/settings_page.html')

def social_main(request):
    #print(request.user.first_name)
    #print(request.user.profile.city_of_residence)
    #print(request.user.Profile.address_line_1)
    user_news_feed = NewsFeed.objects.filter(region = request.user.profile.city_of_residence)
    useful_links = UsefulLinks.objects.filter(region = request.user.profile.city_of_residence)
    inquieries = Inquieries.objects.all()
    if request.method == "POST":
        #print(request.POST.get("region-selection"))
        if request.POST.get("region-selection") == request.user.profile.city_of_residence:
            user_news_feed = NewsFeed.objects.filter(region = request.user.profile.city_of_residence).order_by("-date_posted")
        else:
            user_news_feed = NewsFeed.objects.order_by("-date_posted")
    #print(user_news_feed)
    return render(request, 'Material_Classifier/social_main.html', {'user_news_feed' : user_news_feed, "useful_links": useful_links, "inquieries":inquieries})

def incentive_main(request):
    inc_obj = IncentiveOffers.objects.filter(offer_region = request.user.profile.city_of_residence)
    if request.method == "POST":
        messages.success(request, f'Congratulations on claiming your rewards, keep up the good work and lets save the planet')
        print("Redirecting user to home page")
        return HttpResponseRedirect(reverse('home-page'))
    #print(inc_obj)
    else:
        return render(request, 'Material_Classifier/incentive_main.html', {"incentive_offers" : inc_obj})

@login_required
def profile(request):
    return render(request, 'Material_Classifier/profile.html')


def register(request):
    if request.method == "POST":
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are able to log in')
            return HttpResponseRedirect(reverse('login-page'))
    else:
        form=UserRegisterForm()
    return render(request,'Material_Classifier/register.html', {'form':form})


def home(request):
    return render(request,'Material_Classifier/home.html', {"title": "Home Page"})


@login_required
def classifier(request):
    mat_classification = {}
    predictions = {}
    pred = ""
    history_path = "media/history_images"
    
    
    if request.method == "POST":
        form = ImageClassificationForm(request.POST,request.FILES)
        
        
        if  form.is_valid():
            print(request.POST.dict)
            print (request.FILES['picture'])
            form.save()
            #print(str(form["picture"]))
            os.rename("media/images/"+str(request.FILES['picture']), "media/images/image.jpg")
            img_taken = "media/images/image.jpg"
            img_densenet, img_inceptionresnet, img_nasnetlarge = prepare_images(img_taken)
            predictions = combined_prediction(img_densenet, img_inceptionresnet, img_nasnetlarge, densenet169, inceptionresnet, nasnetlarge)
            pred = predictions["Combined Predicted Label"]
            print(pred)

            history_path, img_title = move_images(img_taken, history_path)
            # creating an ItemClassification instance to save the details of the image saved
            print("Creating object instace for ItemClassification and saveing data")

            try:
                print("Creating object instace for ItemClassification and saveing data")
                obj_item_img = ItemClassificationPicture.objects.create(picture_title = img_title, picture_path = history_path)
                obj_item_img.save()
            except Exception as e:
                print(e)
            
            print ("image is stored in:", history_path)
            print(predictions)
            request.session["img_title"] = img_title
            request.session["history_path"] = history_path
            request.session["pred"] = pred
            request.session["predictions_dict"] = predictions
            return HttpResponseRedirect(reverse('classifier-results'))

    else:
        pred = ""
        form = ImageClassificationForm()
        return render(request, 'Material_Classifier/classifier.html', {"form": form, "pred":pred})


def classifier_results(request):
    
    # print on server terminal for performance checking
    print("Prediction from page classifier is:",request.session["pred"])
    print("Image source is as follows:", request.session["history_path"])
    img_taken = request.session["history_path"]
    predictions_dict = request.session["predictions_dict"]
    prediction_results = request.session["pred"]
    img_title = request.session["img_title"]
    print(img_taken)

    # get the object with the same image title from db
    obj_item_img = ItemClassificationPicture.objects.get(picture_title = img_title)
    print("Predictions dictionary as follows:")
    print(predictions_dict)

    if request.method == "POST":
        print("Creating object instance for results")
        # creating an instance of ItemClassificationResults to save them in DB
        obj_resutls = ItemClassificationResults.objects.create(
                combined_predicted_label = predictions_dict["Combined Predicted Label"],
                densenet169_predicted_label = predictions_dict["DenseNet169 Predicted Label"],
                inceptionresnet_predicted_label = predictions_dict["InceptionResNet Predicted Label"],
                nasnetlarge_predicted_label = predictions_dict["NASNetLarge Predicted Label"],
                combined_votes = predictions_dict["Combined Votes"],
                item_picture = obj_item_img,
                item_results_user = request.user
            )
        print("Saving results in database")
        messages.success(request, f'Item has been saved successfuly')
        obj_resutls.save()
        print("Redirecting user to home page")
        return HttpResponseRedirect(reverse('home-page'))
        
    
    
    disposal_bin = DisposalBin(prediction_results, request.user.profile.city_of_residence)
    return render(
        request, 'Material_Classifier/classifier_results.html',
     {'title': 'Classification Results', 'prediction_results': prediction_results, 'image_taken_path':img_taken, "disposal_bin": disposal_bin}
     )


def classifier_non_correct_results(request):
    img_taken = request.session["history_path"]
    img_taken = request.session["history_path"]
    predictions_dict = request.session["predictions_dict"]
    prediction_results = request.session["pred"]
    img_title = request.session["img_title"]
    obj_item_img = ItemClassificationPicture.objects.get(picture_title = img_title)

    if request.method == "POST":
        print(request.POST.get("materia-selection"))
        print(request.POST.get("user-authorisation-for-image-reuse"))
        print(type(request.POST.get("user-authorisation-for-image-reuse")))
        if request.POST.get("user-authorisation-for-image-reuse") is not None:
            print("Creating object instance for results")
            # creating an instance of ItemClassificationResults to save them in DB
            obj_resutls = ItemClassificationResults.objects.create(
                    combined_predicted_label = predictions_dict["Combined Predicted Label"],
                    densenet169_predicted_label = predictions_dict["DenseNet169 Predicted Label"],
                    inceptionresnet_predicted_label = predictions_dict["InceptionResNet Predicted Label"],
                    nasnetlarge_predicted_label = predictions_dict["NASNetLarge Predicted Label"],
                    combined_votes = predictions_dict["Combined Votes"],
                    item_picture = obj_item_img,
                    item_results_user = request.user,
                    is_correct = False,
                    rectified_label = request.POST.get("materia-selection"),
                    marked_for_futur_training = True
                    )
        else:
            print("Creating object instance for results")
            # creating an instance of ItemClassificationResults to save them in DB
            obj_resutls = ItemClassificationResults.objects.create(
                    combined_predicted_label = predictions_dict["Combined Predicted Label"],
                    densenet169_predicted_label = predictions_dict["DenseNet169 Predicted Label"],
                    inceptionresnet_predicted_label = predictions_dict["InceptionResNet Predicted Label"],
                    nasnetlarge_predicted_label = predictions_dict["NASNetLarge Predicted Label"],
                    combined_votes = predictions_dict["Combined Votes"],
                    item_picture = obj_item_img,
                    item_results_user = request.user,
                    is_correct = False,
                    rectified_label = request.POST.get("materia-selection"),
                    marked_for_futur_training = False
                    )
        messages.success(request, f'Item has been saved successfuly, sorry for the miss-identification')
        obj_resutls.save()
        print("Redirecting user to home page")
        return HttpResponseRedirect(reverse('home-page'))
    else:
        return render(request, 'Material_Classifier/classifier_non_correct_results.html', {'image_taken_path':img_taken})

def progress_main(request):

    material_labels = {0:'Cardboard', 1:'Chips Bag', 2:'Drinking Carton', 3:'Glass Bottle',
                   4:'Glass Cup', 5:'Metal Can', 6:'Organic', 7:'Paper', 8:'Plastic Bag',
                   9:'Plastic Bottle', 10:'Plastic Box', 11:'Plastic Round Container'}


    mat_labels_list = []
    user_material_total = []

    mat_labels_list_today = []
    user_material_total_today = []

    #user_items_classifiction_results = ItemClassificationResults.objects.all()
    user_items_classification_results = ItemClassificationResults.objects.filter(item_results_user = request.user)
    user_items_classification_results_today = ItemClassificationResults.objects.filter(item_results_user = request.user, date_disposed = datetime.date.today())
    
    # get the count of plastic and non-plastic materials for display purposes
    cnt_overall_plastic = 0
    cnt_overall_non_plastic = 0
    # get the overall results
    for material in material_labels.values():
        cnt = user_items_classification_results.filter(combined_predicted_label = material).count()
        mat = material
        if "Plastic" in material:
            cnt_overall_plastic += cnt
        else:
            cnt_overall_non_plastic +=cnt
        if cnt > 0:
            mat_labels_list.append(mat)
            user_material_total.append(cnt)

    # get today's results
    for material in material_labels.values():
        cnt = user_items_classification_results_today.filter(combined_predicted_label = material).count()
        mat = material
        if cnt > 0:
            mat_labels_list_today.append(mat)
            user_material_total_today.append(cnt)

    #get the timeline results
    user_unique_dates = []
    user_plastic_bag_list = []
    user_plastic_bottle_list = []
    user_plastic_box_list = []
    user_plastic_round_container_list = []
    user_glass_bottle_list = []
    user_glass_cup_list = []
    user_metal_can_list = []
    user_carboard_list = []
    user_paper_list = []
    user_drinking_carton_list = []
    user_chips_bag_list = []
    user_organic_list = []

    for item in user_items_classification_results:
        user_unique_dates.append(item.date_disposed)
    user_unique_dates = list(set(user_unique_dates)) # getting distinct values from queried list
    print(user_unique_dates)
    
    for dt in user_unique_dates:
        cnt = user_items_classification_results.filter(combined_predicted_label = "Plastic Bag", date_disposed = dt).count()
        user_plastic_bag_list.append(cnt)
        cnt = user_items_classification_results.filter(combined_predicted_label = "Plastic Bottle", date_disposed = dt).count()
        user_plastic_bottle_list.append(cnt)
        cnt = user_items_classification_results.filter(combined_predicted_label = "Plastic Box", date_disposed = dt).count()
        user_plastic_box_list.append(cnt)
        cnt = user_items_classification_results.filter(combined_predicted_label = "Plastic Round Container", date_disposed = dt).count()
        user_plastic_round_container_list.append(cnt)
        cnt = user_items_classification_results.filter(combined_predicted_label = "Glass Bottle", date_disposed = dt).count()
        user_glass_bottle_list.append(cnt)
        cnt = user_items_classification_results.filter(combined_predicted_label = "Glass Cup", date_disposed = dt).count()
        user_glass_cup_list.append(cnt)
        cnt = user_items_classification_results.filter(combined_predicted_label = "Metal Can", date_disposed = dt).count()
        user_metal_can_list.append(cnt)
        cnt = user_items_classification_results.filter(combined_predicted_label = "Cardboard", date_disposed = dt).count()
        user_carboard_list.append(cnt)
        cnt = user_items_classification_results.filter(combined_predicted_label = "Paper", date_disposed = dt).count()
        user_paper_list.append(cnt)
        cnt = user_items_classification_results.filter(combined_predicted_label = "Drinking Carton", date_disposed = dt).count()
        user_drinking_carton_list.append(cnt)
        cnt = user_items_classification_results.filter(combined_predicted_label = "Chips Bag", date_disposed = dt).count()
        user_chips_bag_list.append(cnt)
        cnt = user_items_classification_results.filter(combined_predicted_label = "Organic", date_disposed = dt).count()
        user_organic_list.append(cnt)

    print(user_plastic_bag_list)
    
    if request.method == "POST":
        print(request.POST.get("chart-type-selection"))
        chart_type = request.POST.get("chart-type-selection")
        return render(request, 'Material_Classifier/progress_main.html', {'title': 'Progress Main Page', "mat_labels": mat_labels_list, 
                    "mat_total": user_material_total, "mat_dict": material_labels,
                    "mat_labels_today": mat_labels_list_today, "mat_total_today":user_material_total_today, "today": datetime.date.today(), "chart_type": chart_type,
                    "user_unique_dates": user_unique_dates, "user_plastic_bag_list":user_plastic_bag_list, "user_plastic_bottle_list":user_plastic_bottle_list,
                     "user_plastic_box_list":user_plastic_box_list, "user_plastic_round_container_list":user_plastic_round_container_list,"user_glass_bottle_list":user_glass_bottle_list,
                      "user_glass_cup_list":user_glass_cup_list, "user_metal_can_list":user_metal_can_list, "user_carboard_list":user_carboard_list, "user_paper_list":user_paper_list,
                       "user_drinking_carton_list":user_drinking_carton_list, "user_chips_bag_list":user_chips_bag_list, "user_organic_list":user_organic_list, "cnt_overall_plastic":cnt_overall_plastic, "cnt_overall_non_plastic":cnt_overall_non_plastic })
    else:
        return render(request, 'Material_Classifier/progress_main.html', {'title': 'Progress Main Page', "mat_labels": mat_labels_list, 
                    "mat_total": user_material_total, "mat_dict": material_labels,
                    "mat_labels_today": mat_labels_list_today, "mat_total_today":user_material_total_today, "today": datetime.date.today(),
                    "user_unique_dates": user_unique_dates, "user_plastic_bag_list":user_plastic_bag_list, "user_plastic_bottle_list":user_plastic_bottle_list,
                    "user_plastic_box_list":user_plastic_box_list, "user_plastic_round_container_list":user_plastic_round_container_list,"user_glass_bottle_list":user_glass_bottle_list,
                    "user_glass_cup_list":user_glass_cup_list, "user_metal_can_list":user_metal_can_list, "user_carboard_list":user_carboard_list, "user_paper_list":user_paper_list,
                    "user_drinking_carton_list":user_drinking_carton_list, "user_chips_bag_list":user_chips_bag_list, "user_organic_list":user_organic_list, "cnt_overall_plastic":cnt_overall_plastic, "cnt_overall_non_plastic":cnt_overall_non_plastic})
        

    

def about(request):
    #print("this is a test for sessions, variable stored is:",request.session["history_path"])
    return render(request, 'Material_Classifier/about.html', {'title':'About Page'})
