def is_empty_param(request, param_name):
    param = request.query_params.get(param_name, None)
    return param is None or (isinstance(param, str) and len(param.strip()) == 0)


def get_param(request, param):
    """

    :param request:
    :param param:
    :return: param value or None if doesn't exist or is empty
    """
    return None if is_empty_param(request, param) else request.query_params.get(param)


def get_int_param(request, param):
    param = get_param(request, param)
    if isinstance(param, int) or (isinstance(param, str) and param.isnumeric()):
        return int(param)
    else:
        return None
