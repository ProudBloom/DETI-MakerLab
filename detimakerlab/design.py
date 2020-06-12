import cgi
import json

import oauth2 as oauth
from django.shortcuts import render, redirect

# Views for the HTML pages
from detimakerlab import settings
from detimakerlab.technician_api.models import Equipments

consumer = oauth.Consumer(settings.KEY, settings.SECRET)
client = oauth.Client(consumer)

request_token_url = 'http://identity.ua.pt/oauth/request_token'
authenticate_url = 'http://identity.ua.pt/oauth/authorize'
access_token_url = 'http://identity.ua.pt/oauth/access_token'
get_data_url = 'http://identity.ua.pt/oauth/get_data'


def homepage(request):
    if 'oauth_token' in request.GET and 'oauth_verifier' in request.GET:
        token = oauth.Token(request.session['request_token']['oauth_token'],
                            request.session['request_token']['oauth_token_secret'])
        token.set_verifier(request.GET['oauth_verifier'])
        new_client = oauth.Client(consumer, token)
        resp, content = new_client.request(access_token_url, "GET")
        if resp['status'] != '200':
            print(content)
            raise Exception("Invalid response from identity.ua.pt")
        session = dict(cgi.urllib.parse.parse_qsl(content))
        access_token = {x.decode("utf8"): session[x].decode("utf8") for x in session.keys()}
        print(access_token)

        # Get data
        token.key = access_token['oauth_token']
        token.secret = access_token['oauth_token_secret']
        print(get_data(new_client))
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


########################################################################################

def all_equipment(request):
    data = Equipments.objects.all()
    return render(request, 'all_equipment.html', {"equipmentData": data})


def create_project(request):
    return render(request, 'create_project.html')


def nav_bar(request):
    return render(request, 'navbar.html')


def rent_equipment(request):
    return render(request, 'rent_equipment.html')


def return_equipment(request):
    return render(request, 'return_equipment.html')


def student(request):
    return render(request, 'student.html')


def technician(request):
    return render(request, 'technician.html')


def requests(request):
    return render(request, 'requests.html')


def edit_equipment(request):
    return render(request, 'edit_equipment.html')


def statistics(request):
    return render(request, 'statistics.html')


def my_projects(request):
    return render(request, 'my_projects.html')


def team(request):
    return render(request, 'team.html')


def login(request):
    resp, content = client.request(request_token_url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response from identity.ua.pt")

    session = dict(cgi.urllib.parse.parse_qsl(content))
    # cast bytes to str
    request.session['request_token'] = {x.decode("utf8"): session[x].decode("utf8") for x in session.keys()}

    url = "%s?oauth_token=%s" % (authenticate_url,
                                 request.session['request_token']['oauth_token'])
    return redirect(url)


def get_data(c=client):
    """
    :param c: Client
    :return: email , (name, username)
    """
    url = "%s?scope=uu&format=json" % get_data_url
    resp, content = c.request(url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response from identity.ua.pt")

    email = json.loads(content)['email']

    url = "%s?scope=name&format=json" % get_data_url
    resp, content = c.request(url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response from identity.ua.pt")

    name, surname = json.loads(content)['name'], json.loads(content)['surname']
    return email, (name, surname)
