from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
import time
from .models import Config
from .forms import ConfigForm
import subprocess
from topo_proxy.tunnels.facebook import FacebookAPI


def home(request):
    return render(request, "pages/home.html")


def about(request):
    return render(request, "pages/about.html")


def ping(request):

    last_ping = request.session.get('last_ping', 0)

    # proxies = {'http': '127.0.0.1:5000'}
    delay = 60 - int(time.time() - last_ping)

    if delay > 0:
        response = {
            "message": (
                f"Please, you should wait for {delay}s"
                "before your next ping!"
            ),
            "type": "is-warning"
        }
    else:
        url = request.GET.get('url', 'http://neverssl.com')

        if url.startswith('http://'):

            try:
                response = requests.head(url)
                request.session['last_ping'] = time.time()
            except Exception as err:
                response = {
                    'message': str(err),
                    'type': 'is-danger'
                }
            else:
                response = {
                    'message': '\n'.join([
                        ': '.join(i)
                        for i in response.headers.items()
                    ]),
                    'type': 'is-normal'
                }
        else:
            response = {
                'message': 'Only HTTP url allowed!',
                'type': 'is-warning',
            }

    return JsonResponse(response)


@login_required
def get_config(request):
    configs = Config.objects.filter(owner=request.user)

    return render(
        request, 'pages/index.html', {'configs': configs})


@login_required
def new_config(request):

    if request.POST:
        form = ConfigForm(request.POST)

        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            messages.success(request, 'New configuration added.')

            return redirect(get_config)
        else:
            messages.error(request, 'Configuration invalid.')
    else:
        form = ConfigForm()

    return render(
        request, 'pages/new_config.html', {'form': form})


@login_required
def drop_config(request, pk):
    Config.objects.filter(pk=pk).delete()

    return redirect(get_config)


@login_required
def reload_config(request, pk):
    config = get_object_or_404(Config, pk=pk)

    if config.process_id:
        subprocess.Popen(f'kill {config.process_id}', shell=True)
        config.process_id = 0
    else:
        conf = config.remote_account.split(':')
        fb = FacebookAPI()
        friend_id = fb.login(*config.local_account.split(':'))
        process = subprocess.Popen(
            f'LOGFILENAME="{request.user}.log"'
            f' FB_USERNAME="{conf[0]}"'
            f' FB_PASSWORD="{conf[1]}"'
            f' FB_FRIEND="{friend_id}"'
            ' python -m topo_proxy'
            f' facebook -td {config.txdelay} -rd {config.rxdelay}'
            f' -t {config.timeout}',
            shell=True, stderr=subprocess.STDOUT)
        config.process_id = process.pid
    config.save()

    return redirect(get_config)
