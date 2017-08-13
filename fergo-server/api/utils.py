import logging

logger = logging.getLogger(__name__)


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


def create_relation(relation_class, relation_serializer,
                    object_id, user_id, relation_type=None):
    logger.debug("Creating relation: class(%s):obj(%s):user(%s):reltype(%s)"
                 % (relation_class, object_id, user_id, relation_type))
    # TODO use serializer instead of directly creating the model, using a serializer needs RIO instead of just the id
    relation_object = relation_class(object_id=object_id, user_id=user_id)
    if relation_type is not None:
        relation_object.relation_type = relation_type
    relation_object.save()
