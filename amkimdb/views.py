import os

from django.shortcuts import render

from amkimdb import models
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('zym51ZvCVd35WSHBj1Aat24nfp9LM-X322VW2WQEs4Zw')
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator
)
language_translator.set_service_url('https://api.eu-de.language-translator.watson.cloud.ibm.com/instances/04dcff24-9a00-4d29-a11e-8ddd9bae0d23')


def home_page(request):
    movies = models.Movie.objects.all()
    return render(request, 'index.html', {'movies': movies})


def language_page(request, movie_id):
    return render(request, 'index2.html', {'movie_id': movie_id})


def comment_page(request, movie_id, language):
    comments = models.Movie.objects.get(id=movie_id).movie_comments
    if language == 1:
        return render(request, 'index3.html', {'comments': comments})
    lang = 'en'
    if language == 2:
        lang = 'fr'
    elif language == 3:
        lang = 'es'
    for comment in comments:
        translation = language_translator.translate(text=comment.text, source='en', target=lang).get_result()
        print(translation)
        comment.text = translation['translations'][0]['translation']
    return render(request, 'index3.html', {'comments': comments})


