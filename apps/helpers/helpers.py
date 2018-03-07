from django.http import QueryDict
from rest_framework.request import Request
from rest_framework.exceptions import ParseError


def get_query_param_or_400(request: Request, key: str, _list=False):
    """
    Returns a query parameter and raises a 400 if it is malformed or missing

    """
    if _list and isinstance(request.query_params, QueryDict):
        value = request.query_params.getlist(key)
    else:
        value = request.query_params.get(key)
    if value is None or value == []:
        raise ParseError(_("'%s' is a required query parameter." % key))

    return value


def get_query_param_list_or_400(request: Request, key: str):
    """
    Shortcut for get_query_param_or_400 with _list=True
    """
    return get_query_param_or_400(request, key, _list=True)


def get_data_field_or_400(request: Request, key: str, _list=False):
    """
    Returns a body data field and raises a 400 if it is malformed or missing

    """
    if _list and isinstance(request.data, QueryDict):
        value = request.data.getlist(key)
    else:
        value = request.data.get(key)
    if value is None or value == []:
        raise ParseError(_("'%s' is a required body field." % key))

    return value


def get_data_list_or_400(request: Request, key: str):
    return get_data_field_or_400(request, key, _list=True)