from django.http import HttpResponse, JsonResponse
from tarot_app.models import *
from rest_framework.decorators import api_view
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from twilio.rest import Client
import json
import random
import requests
from decouple import config

twillio_account_sid=config('twillio_account_sid')
twillio_auth_token=config('twillio_auth_token')
twillio_number=config('twillio_number')
def index(request):
    theIndex = open('static/index.html').read()
    return HttpResponse(theIndex)
@api_view(['POST'])
def set2fa(request):
    phone_number=request.data['phoneNumber']
    client = Client(twillio_account_sid,twillio_auth_token)
    auth_number =random.randint(100000, 999999)
    message = client.messages.create(
            body=f'Your authentication number is: {auth_number}',
            from_=twillio_number,
            to=f'+1{phone_number}'
                )
    return JsonResponse({'OTP':auth_number})
@api_view(["GET"])
def load_cards(request):
    if request.method == "GET":
        cards = TarotCard.objects.all()
        cards_json = serializers.serialize('json', cards)

        return HttpResponse(cards_json)


@api_view(["POST"])
def register_user(request):
    if request.method == "POST":
        email = request.data['email']
        password = request.data['password']
        first_name=request.data['firstName']
        last_name=request.data['lastName']
        phone_number=request.data['phoneNumber']
        try:
            SiteUser.objects.create_user(email=email, password=password, username=email,cell_phone_number=phone_number,first_name=first_name,last_name=last_name)
            return JsonResponse({'success': True})
        except Exception as e:
            return HttpResponse("A user with that email already exists.", status=409)


@api_view(["POST"])
def login_user(request):
    if request.method == "POST":
        email = request.data['email']
        password = request.data['password']
        user = authenticate(username=email, password=password)
        print(user)
        if user is not None:
            try:
                login(request._request, user)
                print(request.session)
                return JsonResponse({'success': True})
            except Exception as e:
                print(e)
                return (HttpResponse("Invalid Credentials", status=401))
        return (HttpResponse("Invalid Credentials", status=401))


def logout_user(request):
    try:
        logout(request)
        return JsonResponse({'logout': True})
    except Exception as e:
        print(e)
        return JsonResponse({'logout': False})


@api_view(["GET"])
def current_user(request):
    if request.user.is_authenticated:
        data = {request.user}
        return HttpResponse(data)
    else:
        return JsonResponse(None, safe=False)
@api_view(['PUT'])
def set_name(request):
    first_or_last_name=next(iter(request.data))
    setattr(request.user, first_or_last_name,request.data[first_or_last_name])
    request.user.save()
    return HttpResponse('ok')

@api_view(['PUT'])
def set_password(request):
    user=SiteUser.objects.get(cell_phone_number=request.data['phoneNumber'])
    user.set_password(request.data['password'])
    try:
        user.save()
        return JsonResponse({"message":"password changed"})
    except Exception as e:
        return JsonResponse({"message":e})

@api_view(['POST'])
def set_cell(request):
   
    if request.data["code"] == False:
        phone_number=request.data['phoneNumber']
        client = Client(twillio_account_sid,twillio_auth_token)
        auth_number =random.randint(100000, 999999)
        request.user.phone_code=auth_number
        request.user.save()
        message = client.messages.create(
                body=f'Your authentication number is: {auth_number}',
                from_=twillio_number,
                to=f'+1{phone_number}'
                    )
        return HttpResponse('')
    else:
        if (int(request.data["code"])==request.user.phone_code):
            request.user.cell_phone_number=request.data['phoneNumber']
            request.user.save()
            message="new phone saved"
            return JsonResponse({'message':message})
            
        else:
            message="incorrect code"
            return JsonResponse({'message':message}, status=400)

@api_view(["GET"])
def user_account(request):
    user=request.user
    accountDetails={
        "first_name":None,
        "last_name":None,
        "email":None,
        "cell_phone_number":None
    }
    for key, val in accountDetails.items():
        try:
            accountDetails[key] = getattr(user, f'{key}')
        except:
            accountDetails[key] = None

    return JsonResponse(accountDetails)


@api_view(["POST"])
def get_reading(request):
    user = request.user
    card_name = request.data['card']
    reverse = request.data['reverse']
    if request.user.is_authenticated:

        card = TarotCard.objects.get(name=card_name)
        user = SiteUser.objects.get(username=user)

        spread = Spread(user=user, type="Single Card")
        spread.save()

        card_in_spread = CardInSpread(
            spread=spread, tarot_card=card, position=1, reverse=reverse)
        card_in_spread.save()

        note = Note(card_in_spread=card_in_spread,
                    description="", interpretation="")
        note.save()

        data = {
            'spread_type': spread.type,
            'position': card_in_spread.position,
            'reverse': card_in_spread.reverse,
            'tarot_name': card.name,
            'number': card.number,
            'arcana': card.arcana,
            'suit': card.suit,
            'img': card.img,
            'keywords': card.keywords,
            'questions_to_ask': card.questions_to_ask,
            'note_id': note.pk,
            'note_description': note.description,
            'note_interpretation': note.interpretation

        }

        response_data = json.dumps(data)

        return HttpResponse(response_data, content_type='application/json')

    return JsonResponse({'success': False})


@api_view(["PUT"])
def update_note(request):
    description = request.data['description']
    interpretation = request.data['interpretation']
    note_id = request.data['note_id']
    Note.objects.filter(pk=note_id).update(
        description=description, interpretation=interpretation)
    return JsonResponse({'success': True})


@api_view(["GET"])
def third_party_api(request):

    res_quote = requests.get('https://zenquotes.io/api/random').json()
    quote = res_quote[0]['q']

    res_cat = requests.get('https://api.thecatapi.com/v1/images/search').json()
    cat = res_cat[0]['url']

    data = {'quote': quote, 'cat': cat}
    response_data = json.dumps(data)

    return HttpResponse(response_data)


@api_view(["GET"])
def get_user_notes(request, number):
    if request.user.is_authenticated:
        user = SiteUser.objects.get(username=request.user)

        spreads = Spread.objects.filter(user=user).order_by('-date_created')

        if not spreads:
            return (HttpResponse("No user spreads created", status=404))

        active_spread = spreads[number]
        card_in_spread = CardInSpread.objects.get(spread=active_spread.pk)
        card = card_in_spread.tarot_card
        active_note = Note.objects.get(card_in_spread=card_in_spread)

        spreads_length = len(spreads)

        data = {
            'spread_id': active_spread.pk,
            'number_of_notes': spreads_length,
            'tarot_name': card.name,
            'position': card_in_spread.position,
            'reverse': card_in_spread.reverse,
            'img': card.img,
            'keywords': card.keywords,
            'questions_to_ask': card.questions_to_ask,
            'note_id': active_note.pk,
            'note_description': active_note.description,
            'note_interpretation': active_note.interpretation
        }

        response_data = json.dumps(data)

        return HttpResponse(response_data)

    return JsonResponse({'success': False})


@api_view(["DELETE"])
def delete_spread(request, spread_id):
    spread_to_delete = Spread.objects.get(pk=spread_id)
    spread_to_delete.delete()

    return JsonResponse({'success': True})

@api_view(["GET", "POST"])
def dream_entries(request):
    if request.method == "POST":
        try:
            data = request.data
            description = data["params"]["description"]
            associations = data["params"]["association"]
            inner_dynamics = data["params"]["inner_dynamics"]
            interpretation = data["params"]["interpretation"]
            ritual = data["params"]["ritual"]

            new_image = DreamEntry1(
                user=request.user,
                description=description, associations=associations, inner_dynamics=inner_dynamics, interpretation=interpretation, ritual=ritual)

            new_image.save()
            return JsonResponse({'success': True})

        except Exception as e:
            print(e)
            return HttpResponse(e)

    if request.method == "GET":
        user = SiteUser.objects.get(email=request.user)

        dream_entries = DreamEntry1.objects.filter(user=user).order_by('-created_at')

        dreams_json = serializers.serialize('json', dream_entries)

        return HttpResponse(dreams_json)

@api_view(["GET"])
def user_tarot_entries(request):
    if request.method == "GET":

        user = SiteUser.objects.get(email=request.user)

        spreads = Spread.objects.filter(user=user).order_by('-date_created')

        spreads_json = serializers.serialize('json', spreads)

        return HttpResponse(spreads_json)