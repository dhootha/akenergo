from models import TopMenu

#def get_current_path(request):
#    return {
#        'current_path': request.get_full_path()
#    }

def getTopMenu(request):
    #cache.add('top_menu_nodes', TopMenu.objects.all(), 3600)
    #resolver = resolve(request.path_info)
    #print resolver.kwargs.get('link'), request.path_info

    return {
        'top_menu_nodes': TopMenu.objects.filter(level=0, published=True),
        }
