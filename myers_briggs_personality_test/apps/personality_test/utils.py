from django.http import Http404

from .models import DescriptorType, DescriptorInfo, Question


def get_descriptor_info_by_test(test_result):
    """
    TODO add description
    """
    descriptor_info = {'consciousness_orientation': False, 'situation_orientation': False,
                       'decision_making_basis': False, 'preparing_solutions_method': False}
    for descriptor_type_str, result in test_result.items():
        # Get descriptor type enum member
        descriptor_type = DescriptorType(descriptor_type_str)
        # Get attr name
        attr_name = descriptor_type.name.lower()
        # Get question queryset of description type elements
        questions = Question.objects.filter(answer_options__descriptor_increase=descriptor_type)
        # Bool result is more than half of all questions with this descriptor type
        attr_value = result > (questions.count() / 2)
        # Set attr by name
        descriptor_info[attr_name] = attr_value
    try:
        descriptor_instance = DescriptorInfo.objects.get(**descriptor_info)
    except DescriptorInfo.DoesNotExist:
        raise Http404
    return descriptor_instance