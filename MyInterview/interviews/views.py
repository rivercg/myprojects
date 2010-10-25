from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from models import IvRecord, Message
from django.template import RequestContext
from django.contrib import messages
import datetime

@login_required
def index(request):
    active_record_list = IvRecord.objects.exclude(status="Closed").order_by('-open_date')
    closed_record_list = IvRecord.objects.filter(status="Closed").order_by('-open_date')
    has_add_permission = True
    return render_to_response('interviews/index_list.html', 
                              {'user': request.user, 'title': 'Interview records', 
                               'active_record_list': active_record_list,
                               'closed_record_list': closed_record_list,
                               'has_add_permission': has_add_permission})
    
@login_required
def active_list(request):
    record_list = IvRecord.objects.exclude(status="Closed").order_by('-open_date')
    return render_to_response('interviews/long_list.html', 
                              {'user': request.user, 'title': 'Active records', 
                               'record_list': record_list})
@login_required
def closed_list(request):
    record_list = IvRecord.objects.filter(status="Closed").order_by('-open_date')
    return render_to_response('interviews/long_list.html', 
                              {'user': request.user, 'title': 'Closed records', 'is_close': True,
                               'record_list': record_list})

@login_required
def detail(request, iv_id):
    has_close_permission = True
    has_reopen_permission = True
    iv_record = IvRecord.objects.get(pk=iv_id)
    context = {'user': request.user, 
               'title': 'View record', 
               'iv_record': iv_record,}
    context.update({ 
            'is_popup': False,
            'add': False,                                                                              
            'change': False,                                                                        
            'has_add_permission': False, #self.has_add_permission(request),                                  
            'has_change_permission': False, #self.has_change_permission(request, obj),                       
            'has_delete_permission': False,#self.has_delete_permission(request, obj),                       
            'has_file_field': True, # FIXME - this should check if form or formsets have a FileField,
            'has_absolute_url': False,                             
            'ordered_objects': None,                                                      
            'form_url': '', #mark_safe(form_url),                                                         
            'opts': None, #opts,                                                                            
            #'content_type_id': ContentType.objects.get_for_model(self.model).id,                     
            'save_as': '', #self.save_as,                                                                 
            #'save_on_top': self.save_on_top,                                                         
            #'root_path': self.admin_site.root_path,    
            'has_close_permission': has_close_permission,
            'has_reopen_permission': has_reopen_permission,
            })     
    return render_to_response('interviews/detail.html', context,
                               context_instance=RequestContext(request))

@login_required
def operate(request, iv_id, action):
    iv_record = IvRecord.objects.get(pk=iv_id)
    return render_to_response('interviews/detail.html', 
                              {'user': request.user, 
                               'title': 'Change record', 
                               'iv_record': iv_record, 
                               'has_add_permission': False,
                               'change': True,
                               'is_popup': False,
                               'save_as': '',
                               },
                               context_instance=RequestContext(request))

@csrf_protect
@login_required
def add_message(request):
    pub_date = datetime.datetime.now()
    # check user
    v_user = request.user.virtualuser
    if v_user is None:
        raise Http404('Invalid virtual user.')
    # check record
    iv_id = request.POST.get('iv_record')
    iv_record = IvRecord.objects.get(pk=iv_id)
    if iv_record is None:
        raise Http404('Invalid interview record.')
    # check add permission
    # check text
    text = request.POST.get('text')
    if not text:
        messages.warning(request, 'Message has not been added because of EMPTY content.')
    else:
        Message.objects.create(iv_record=iv_record, send_from=v_user, 
                                   text=text, pub_date=pub_date)
        messages.success(request, 'New message added.')
        # update comment
        if request.POST.get('iscomment'):
            iv_record.text = text
            iv_record.save()
    return HttpResponseRedirect('/interviews/%s/' % iv_id)
    
@csrf_protect
@login_required
def add_record(request):
    return HttpResponse('add record')

@csrf_protect
@login_required
def close_record(request, iv_id):
    return HttpResponse('close record')

@csrf_protect
@login_required
def reopen_record(request, iv_id):
    return HttpResponse('reopen record')

@csrf_protect
@login_required
def send_contact(request, iv_id):
    return HttpResponse('send_contact')

@csrf_protect
@login_required
def change_schedule(request, iv_id):
    return HttpResponse('change schedule')

@csrf_protect
@login_required
def cancel_schedule(request, iv_id):
    return HttpResponse('cancel schedule')

@csrf_protect
@login_required
def iv_checkin(request, iv_id):
    return HttpResponse('interview checkin')

