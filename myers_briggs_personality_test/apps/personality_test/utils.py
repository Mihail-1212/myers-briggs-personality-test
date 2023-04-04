from django.http import Http404

from .models import DescriptorType, DescriptorInfo, Question


def calculate_test_result_by_descriptor_type(result, descriptor_type):
    # Get descriptor max weight
    descriptor_count_weight = Question.get_max_weight_descriptor_type(descriptor_type)
    # Bool result is more than half of all questions with this descriptor type
    attr_value = result > (descriptor_count_weight / 2)
    return attr_value


def get_descriptor_info_by_test(test_result):
    """
    Get test_result as dict, process answers and return DescriptorInfo instance
    """
    descriptor_info = {'consciousness_orientation': False, 'situation_orientation': False,
                       'decision_making_basis': False, 'preparing_solutions_method': False}
    for descriptor_type_str, result in test_result.items():
        # Get descriptor type enum member
        descriptor_type = DescriptorType(descriptor_type_str)
        # Get attr name
        attr_name = descriptor_type.name.lower()

        # Get attr value
        attr_value = calculate_test_result_by_descriptor_type(result, descriptor_type)

        # Set attr by name
        descriptor_info[attr_name] = attr_value
    try:
        descriptor_instance = DescriptorInfo.objects.get(**descriptor_info)
    except DescriptorInfo.DoesNotExist:
        raise Http404
    return descriptor_instance


def get_user_result_answers(user_result):
    """
    Return dict of results for user
    descriptor_type: (user_result, max_result, descriptor_type_item)
    """
    result_weights = {choice: 0 for choice in DescriptorType}
    for user_response in user_result.user_responses.all():
        answer = user_response.answer
        descriptor_weight = answer.descriptor_count
        try:
            descriptor_type = DescriptorType(answer.descriptor_increase)
        except ValueError:
            # If descriptor_type is not a valid DescriptorType or is Null
            continue
        result_weights[descriptor_type] += descriptor_weight

    result_answers = {}
    for descriptor_type_str, result_weight in result_weights.items():
        descriptor_type = DescriptorType(descriptor_type_str)
        attr_name = descriptor_type.name.lower()
        # Get descriptor max weight
        descriptor_max_weight = Question.get_max_weight_descriptor_type(descriptor_type)

        descriptor_result_bool = calculate_test_result_by_descriptor_type(result_weight, descriptor_type)

        # descriptor_info[attr_name] = attr_value
        descriptor_object = DescriptorInfo(**{attr_name: descriptor_result_bool})
        descriptor_type_result = getattr(descriptor_object, "get_%s" % attr_name)()

        result_answers[descriptor_type] = (result_weight, descriptor_max_weight, descriptor_type_result)

    return result_answers
