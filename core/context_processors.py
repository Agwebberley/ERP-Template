from django.conf import settings

def cfg_assets_root(request):

    return { 'ASSETS_ROOT' : settings.ASSETS_ROOT }

def cfg_version(request):

    return { 'APP_VERSION' : settings.APP_VERSION, 'CORE_VERSION' : settings.CORE_VERSION }
