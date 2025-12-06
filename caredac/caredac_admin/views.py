from django.utils import translation
from django.utils.translation import gettext as _
from rest_framework.decorators import api_view
from rest_framework.response import Response
from caredac_admin.models import SystemLanguage, ServicesOffered , NeedHelp , LanguageOptions
from caredac_admin.serializers import SystemLanguageSerializer, ServicesOfferedSerializer , NeedHelpSerializer , LanguageOptionsSerializer


# --- Helper: Set current system language dynamically ---
def set_current_language():
    """Activate the current system language from the database."""
    system_lang = SystemLanguage.objects.first()  # Or your logic to select active language
    if not system_lang:
        translation.activate('en')
        return 'en'

    lang = system_lang.language.lower()
    if 'chinese' in lang:
        translation.activate('zh-hans')
        return 'zh-hans'
    elif 'thai' in lang:
        translation.activate('th')
        return 'th'
    else:
        translation.activate('en')
        return 'en'


# --- Admin API root ---
@api_view(['GET'])
def admin_home(request):
    set_current_language()
    return Response({"message": _("Caredac Admin API Root")})


# --- System Languages List & Create ---
@api_view(['GET', 'POST'])
def system_languages(request):
    set_current_language()

    if request.method == 'GET':
        languages = SystemLanguage.objects.all()
        serializer = SystemLanguageSerializer(languages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SystemLanguageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            set_current_language()  # Activate newly created language immediately
            return Response({"message": _("System language created successfully"), "data": serializer.data}, status=201)
        return Response({"error": serializer.errors}, status=400)


# --- System Language Detail, Update, Delete ---
@api_view(['GET', 'PUT', 'DELETE'])
def system_language_detail(request, language_id):
    set_current_language()
    try:
        language = SystemLanguage.objects.get(language_id=language_id)
    except SystemLanguage.DoesNotExist:
        return Response({"error": _("System language not found")}, status=404)

    if request.method == 'GET':
        serializer = SystemLanguageSerializer(language)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SystemLanguageSerializer(language, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            set_current_language()  # Activate updated language immediately
            return Response({"message": _("System language updated successfully"), "data": serializer.data})
        return Response({"error": serializer.errors}, status=400)

    elif request.method == 'DELETE':
        language.delete()
        return Response({"message": _("System language deleted successfully")}, status=200)


# --- Services Offered List & Create ---
@api_view(['GET', 'POST'])
def services_offered(request):
    set_current_language()

    if request.method == 'GET':
        services = ServicesOffered.objects.all()
        serializer = ServicesOfferedSerializer(services, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ServicesOfferedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": _("Service created successfully"), "data": serializer.data}, status=201)
        return Response({"error": serializer.errors}, status=400)


# --- Services Offered Detail, Update, Delete ---
@api_view(['GET', 'PUT', 'DELETE'])
def services_offered_detail(request, services_id):
    set_current_language()
    try:
        service = ServicesOffered.objects.get(services_id=services_id)
    except ServicesOffered.DoesNotExist:
        return Response({"error": _("Service not found")}, status=404)

    if request.method == 'GET':
        serializer = ServicesOfferedSerializer(service)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ServicesOfferedSerializer(service, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": _("Service updated successfully"), "data": serializer.data})
        return Response({"error": serializer.errors}, status=400)

    elif request.method == 'DELETE':
        service.delete()
        return Response({"message": _("Service deleted successfully")}, status=200)

# --- Need Help List & Create ---
@api_view(['GET', 'POST'])
def need_help(request):
    set_current_language()
    if request.method == 'GET':
        help_items = NeedHelp.objects.all()
        serializer = NeedHelpSerializer(help_items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = NeedHelpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": _("Help item created successfully"), "data": serializer.data}, status=201)
        return Response({"error": serializer.errors}, status=400)

# --- Need Help Detail, Update, Delete ---
@api_view(['GET', 'PUT', 'DELETE'])
def need_help_detail(request, help_id):
    set_current_language()
    try:
        help_item = NeedHelp.objects.get(help_id=help_id)
    except NeedHelp.DoesNotExist:
        return Response({"error": _("Help item not found")}, status=404)

    if request.method == 'GET':
        serializer = NeedHelpSerializer(help_item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = NeedHelpSerializer(help_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": _("Help item updated successfully"), "data": serializer.data})
        return Response({"error": serializer.errors}, status=400)

    elif request.method == 'DELETE':
        help_item.delete()
        return Response({"message": _("Help item deleted successfully")}, status=200)


@api_view(['GET','POST','DELETE'])
def language_options(request):
    if request.method == 'GET':
        options = LanguageOptions.objects.all()
        serializer = LanguageOptionsSerializer(options, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = LanguageOptionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": _("Language option created successfully"), "data": serializer.data}, status=201)
        return Response({"error": serializer.errors}, status=400)
    else:  # DELETE
        LanguageOptions.objects.all().delete()
        return Response({"message": _("All language options deleted successfully")}, status=200)

@api_view(['GET','PUT','DELETE'])
def language_options_detail(request, option_id):
    try:
        option_detail = LanguageOptions.objects.get(option_id=option_id)
    except LanguageOptions.DoesNotExist:
        return Response({"error": _("Language option not found.")}, status=404)

    if request.method == 'GET':
        serializer = LanguageOptionsSerializer(option_detail)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LanguageOptionsSerializer(option_detail, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": _("Language Options updated successfully"), "data": serializer.data})
        return Response({"error": serializer.errors}, status=400)

    elif request.method == 'DELETE':
        option_detail.delete()
        return Response({"message": _("Language Option deleted successfully")}, status=200)
