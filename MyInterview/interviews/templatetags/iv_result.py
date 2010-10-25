from django.template import Library
from interviews.models import Message
from candidates.views import get_candidate_feature_list

register = Library()

def resume_detail(user, iv_record):
    return {'user': user,
            'iv_record': iv_record,
            'candidate': iv_record.candidate, 
            'pos': iv_record.position}
resume_detail = register.inclusion_tag("candidates/resume.html")(resume_detail)

def message_list(user, iv_record):
    last_msg_list = iv_record.message_set.all().order_by('-pub_date')[:20]
    return {'user': user,
            'iv_record': iv_record,
            'last_msg_list': last_msg_list}
resume_list = register.inclusion_tag("interviews/message_list.html")(message_list)
    
def submit_row(context):
    opts = context['opts']
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    return {
        'onclick_attrib': (False#opts.get_ordered_objects() and change
                            and 'onclick="submitOrderForm();"' or ''),
        'show_delete_link': (not is_popup and context['has_delete_permission']
                              and (change or context['show_delete'])),
        'show_save_as_new': not is_popup and change and save_as,
        'show_save_and_add_another': context['has_add_permission'] and 
                            not is_popup and (not save_as or context['add']),
        'show_save_and_continue': not is_popup and context['has_change_permission'],
        'is_popup': is_popup,
        'show_save': True
    }
submit_row = register.inclusion_tag('interviews/submit_line.html', takes_context=True)(submit_row)
    
def feature_list(user, iv_record, host):
    c = iv_record.candidate
    candidate_feature_list = get_candidate_feature_list(c)
    return {'user': user,
            'iv_record': iv_record,
            'host': host,
            'candidate_feature_list': candidate_feature_list,}
feature_list = register.inclusion_tag("candidates/feature_list.html")(feature_list)

    
    