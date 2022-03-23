# from django.http import HttpResponseRedirect
# from django.shortcuts import render
#
# from amkimdb import models
# from amkimdb.models import Comment
# from amkimdb.models import Movie
# from ibm_watson import LanguageTranslatorV3
# from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# from ibm_watson import SpeechToTextV1
# from ibm_watson import NaturalLanguageUnderstandingV1
# from amkimdb.forms import UploadFileForm
#
# authenticator = IAMAuthenticator('osSz1O6PII94iofskhrzpevpqYpL6nj5oNS063Jqatot')
# natural_language_understanding = NaturalLanguageUnderstandingV1(
#     version='2021-08-01',
#     authenticator=authenticator
# )
# natural_language_understanding.set_service_url(
#     'https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/e6c7355b-5a9f-4860-8299-39bc0154ec6d')
#
# authenticator = IAMAuthenticator('zym51ZvCVd35WSHBj1Aat24nfp9LM-X322VW2WQEs4Zw')
# language_translator = LanguageTranslatorV3(
#     version='2018-05-01',
#     authenticator=authenticator
# )
# language_translator.set_service_url(
#     'https://api.eu-de.language-translator.watson.cloud.ibm.com/instances/04dcff24-9a00-4d29-a11e-8ddd9bae0d23')
#
# authenticator = IAMAuthenticator('cGCFGDJJTAB_3TKCH7VOPXff4XDPrteJNkLg3WjvD7ew')
# speech_to_text = SpeechToTextV1(
#     authenticator=authenticator
# )
#
# speech_to_text.set_service_url(
#     'https://api.eu-de.speech-to-text.watson.cloud.ibm.com/instances/f10d3685-06e7-4386-aba2-c632b53ddfeb')
#
#
# def home_page(request):
#     movies = models.Movie.objects.all()
#     return render(request, 'index.html', {'movies': movies})
#
#
# def language_page(request, movie_id):
#     return render(request, 'index2.html', {'movie_id': movie_id})
#
#
# def comment_page(request, movie_id, language):
#     form = UploadFileForm()
#     comments = models.Movie.objects.get(id=movie_id).movie_comments
#     if language == 1:
#         return render(request, 'index3.html', {'comments': comments, 'form': form, 'movie_id': movie_id})
#     lang = 'en'
#     if language == 2:
#         lang = 'fr'
#     elif language == 3:
#         lang = 'es'
#     for comment in comments:
#         translation = language_translator.translate(text=comment.text, source='en', target=lang).get_result()
#         print(translation)
#         comment.text = translation['translations'][0]['translation']
#     return render(request, 'index3.html', {'comments': comments, 'form': form, 'movie_id': movie_id})
#
#
# # def handle_uploaded_file(f):
# #     with open('some/file/name.txt', 'wb+') as destination:
# #         for chunk in f.chunks():
# #             destination.write(chunk)
#
#
# def upload_file(request, movie_id):
#     form = UploadFileForm(request.POST, request.FILES)
#     if form.is_valid():
#         result = speech_to_text.recognize(request.FILES['file'], content_type='audio/mp3').get_result()
#         text = result['results'][0]['alternatives'][0]['transcript']
#         movie = Movie.objects.get(id = movie_id)
#         comment = Comment(user=request.POST['user'],text=text,movie=movie)
#         comment.save()
#     return HttpResponseRedirect('/')
#
#


from django.http import HttpResponseRedirect
from django.shortcuts import render

from amkimdb import models
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import SpeechToTextV1
from ibm_watson import NaturalLanguageUnderstandingV1
from amkimdb.forms import UploadFileForm
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions

authenticator = IAMAuthenticator('osSz1O6PII94iofskhrzpevpqYpL6nj5oNS063Jqatot')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=authenticator
)
natural_language_understanding.set_service_url(
    'https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/e6c7355b-5a9f-4860-8299-39bc0154ec6d')

authenticator = IAMAuthenticator('zym51ZvCVd35WSHBj1Aat24nfp9LM-X322VW2WQEs4Zw')
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator
)
language_translator.set_service_url(
    'https://api.eu-de.language-translator.watson.cloud.ibm.com/instances/04dcff24-9a00-4d29-a11e-8ddd9bae0d23')

authenticator = IAMAuthenticator('cGCFGDJJTAB_3TKCH7VOPXff4XDPrteJNkLg3WjvD7ew')
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)

speech_to_text.set_service_url(
    'https://api.eu-de.speech-to-text.watson.cloud.ibm.com/instances/f10d3685-06e7-4386-aba2-c632b53ddfeb')


def home_page(request):
    movies = models.Movie.objects.all()
    return render(request, 'index.html', {'movies': movies})


def language_page(request, movie_id):
    return render(request, 'index2.html', {'movie_id': movie_id})


def comment_page(request, movie_id, language):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            result = speech_to_text.recognize(request.FILES['file'], content_type='audio/mp3').get_result()
            text = result['results'][0]['alternatives'][0]['transcript']
            result2 = natural_language_understanding.analyze(text=text, features=Features(emotion=EmotionOptions())).get_result()
            anger = result2['emotion']['document']['emotion']['anger']
            if anger < 0.4:
                print(anger)
                movie = models.Movie.objects.get(id=movie_id)
                models.Comment(user=request.POST['username'], text=text, movie=movie).save()
        return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
        comments = models.Movie.objects.get(id=movie_id).movie_comments
        if language == 1:
            return render(request, 'index3.html', {'comments': comments, 'form': form, 'movie_id': movie_id})
        lang = 'en'
        if language == 2:
            lang = 'fr'
        elif language == 3:
            lang = 'es'
        for comment in comments:
            translation = language_translator.translate(text=comment.text, source='en', target=lang).get_result()
            print(translation)
            comment.text = translation['translations'][0]['translation']
        return render(request, 'index3.html', {'comments': comments, 'form': form, 'movie_id': movie_id})

# def handle_uploaded_file(f):
#     with open('some/file/name.txt', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


# def upload_file(request, movie_id):
#     form = UploadFileForm(request.POST, request.FILES)
#     if form.is_valid():
#         result = speech_to_text.recognize(request.FILES['file'], content_type='audio/mp3').get_result()
#         text = result['results'][0]['alternatives'][0]['transcript']
#         movie = models.Movie.objects.get(id = movie_id)
#         comment = models.Comment(user=request.POST['user'],text=text,movie=movie)
#         comment.save()
#     return HttpResponseRedirect('/')
