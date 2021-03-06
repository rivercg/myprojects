from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404
from models import *
from interviews.models import IvRecord
from jobs.views import get_job_url
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib import messages

class TemplateDoesNotExist(Exception):
    pass

@login_required
def index(request):
    latest_candidate_list = Candidate.objects.all().order_by('-create_date')[:20]
    return render_to_response('candidates/index.html', {'user': request.user, 'title': 'candidates', 'latest_candidate_list': latest_candidate_list})

def candidiate_to_ivrecord(candidate):
    if isinstance(candidate, Candidate):
        return candidate.ivrecord
    else:
        return None

def candidiate_to_job(candidate):
    ivr = candidiate_to_ivrecord(candidate)
    if isinstance(ivr, IvRecord):
        return ivr.position
    else:
        return None

@login_required    
def detail(request, candidate_id):
    c = Candidate.objects.get(pk=candidate_id)
    p = candidiate_to_job(c)
    return render_to_response('candidates/detail.html', 
                              {'user': request.user, 
                               'title': c.name(), 
                               'candidate': c, 
                               'pos': p, 'has_filters': True,},
                               context_instance=RequestContext(request))

@login_required    
def change(request, candidate_id):
    c = Candidate.objects.get(pk=candidate_id)
    p = candidiate_to_job(c)
    return render_to_response('candidates/detail.html', 
                              {'user': request.user, 
                               'title': 'Change ' + c.name(), 
                               'candidate': c, 
                               'pos': p, 'has_filters': True,},
                               context_instance=RequestContext(request))

CF_TEMPLATE_FIELD_INDEX = 0 
CF_TEMPLATE_FIELD_INIT = 1 
CF_TEMPLATE_FIELD_ACKYES = 1 
CF_TEMPLATE_FIELD_ACKNO = 2
CF_TEMPLATE_FIELD_UPDATE = 3
CF_TEMPLATE_FIELD_RESET = 4
CF_TEMPLATE_FIELD_CLOSE = 6


CANDIDATE_FEATURE_TEMPLATES_NAMES = ('fea_index', 'temp_', 'temp_T', 'temp_U', 'temp_U', 'temp_W', 'temp_C');

CANDIDATE_FEATURE_TEMPLATES = (
    (CANDIDATE_FEATURE_ACC, 'ACC', 'ACC_YES', 'ACC_NO', '', '', ''),    
    (CANDIDATE_FEATURE_ASC, 'ASC', 'ASC_YES', 'ASC_NO', '', '', ''),    
    (CANDIDATE_FEATURE_UR, 'UR', '', '', 'UR_UPDATED', '', '', ''),
)

def _get_feature_templateset(feature_index):
    for t in CANDIDATE_FEATURE_TEMPLATES:
        if (t[CF_TEMPLATE_FIELD_INDEX] == feature_index):
            d = {}
            for i, key in enumerate(CANDIDATE_FEATURE_TEMPLATES_NAMES):
                d[key] = t[i]
            return d
    raise TemplateDoesNotExist

def get_feature_template(feature_index, ack=''):
    temp_set = _get_feature_templateset(feature_index)
    return 'candidates/%s.html' % temp_set['temp_' + ack];

def _make_relative_url(url):
    return '../../../' + url

def get_featurelink_vector(feature, digest, ack=''):
    # get feature definitions
    flink_vector = get_feature_defset(feature)
    # get the view template
    flink_vector['template'] = get_feature_template(flink_vector['fea_index'], ack)
    # query the link
    link_objs = flink_vector['fea_class'].objects.all()
    link_obj = link_objs.get(link_digest=digest)
    # check status of the link_obj
    if not link_obj.can_update_status(ack):
        raise FeatureLinkExpired
    # query and append other info
    c = link_obj.candidate        
    p = candidiate_to_job(c)
    flink_vector.update({'link_obj': link_obj, 'candidate': c, 'pos': p,})
    return flink_vector

def get_featurelink_url(feature, digest):
    return 'candidates/%s/%s/' % (feature, digest)

def _get_featurelink_ackurls(feature, digest):
    url = _make_relative_url(get_featurelink_url(feature, digest))
    return {'ack_true': url + 'T', 'ack_false': url + 'F', 'ack_update': url + 'U',
            'url_reset': url + 'W', 'url_close': url + 'C'}

def _do_featurelink(request, feature, digest):
    # query feature link vector
    flink_vector = get_featurelink_vector(feature, digest)
    # get relative url for yes and no
    ack_urls = _get_featurelink_ackurls(feature, digest) 
    flink_vector.update(ack_urls)
    flink_vector['user'] = request.user
    flink_vector.update({
                 'user': request.user,
                 'title': flink_vector['candidate'].name(),
                 'has_filters': True,
                })     
    #raise Exception
    return render_to_response(flink_vector['template'], flink_vector,
                              context_instance=RequestContext(request))

def featurelink(request, feature, digest):
    #try:
        return _do_featurelink(request, feature, digest)   
    #except:
    #    raise Http404
    
def _get_feature_wrap(flink_obj):  
    flink_vector = get_feature_defset_byindex(flink_obj.feature_index())
    feature_wrap = {'fea_key': flink_vector['fea_key'], 'fea_desc': flink_vector['fea_desc'],
                    'status_desc': flink_obj.get_status_display(), 'mod_date': flink_obj.mod_date,
                    'is_waiting': flink_obj.is_waiting(), 'is_closed': flink_obj.is_closed(),}
    feature_wrap.update(_get_featurelink_ackurls(flink_vector['fea_key'], flink_obj.link_digest))
    feature_wrap['url'] = '/' + get_featurelink_url(flink_vector['fea_key'], flink_obj.link_digest)
    return feature_wrap  
    
def get_candidate_feature_list(candidate):
    acc_wrap = _get_feature_wrap(candidate.candidateackcontactlink)
    asc_wrap = _get_feature_wrap(candidate.candidateackschdulelink)
    ur_wrap = _get_feature_wrap(candidate.candidateupdateresumelink)
    return [acc_wrap, asc_wrap, ur_wrap]

def _do_ack_featurelink(request, feature, digest, ack):
    # check value
    if not is_public_cfl_status(ack):
        raise FeatureStatusDoesNotExist
    # query feature link vector
    flink_vector = get_featurelink_vector(feature, digest, ack)
    # update the status
    flink_vector['link_obj'].update_status(ack)
    flink_vector.update({
                 'user': request.user,
                 'title': flink_vector['candidate'].name(),
                }) 
    return render_to_response(flink_vector['template'], flink_vector,
                               context_instance=RequestContext(request))

def ack_featurelink(request, feature, digest, ack):
    #try:
        return _do_ack_featurelink(request, feature, digest, ack)   
    #except:
    #    raise Http404

def _do_config_featurelink(request, feature, digest, ack):
    # get feature definitions
    flink_vector = get_feature_defset(feature)
    # query the link
    link_objs = flink_vector['fea_class'].objects.all()
    link_obj = link_objs.get(link_digest=digest)
    # check status of the link_obj
    if ack <> link_obj:
        if ack == 'C':
            link_obj.close_it()
        elif ack == 'W':
            digest = random_digest(flink_vector['fea_class'])
            link_obj.link_digest = digest
            link_obj.reset_it()
        else:
            raise FeatureLinkExpired
        messages.success(request, "Update '%s' status to '%s'" % (flink_vector['fea_desc'], link_obj.get_status_display()))
    else:
        messages.warning(request, "Cannot update '%s' status to '%s' because of the save status" % (flink_vector['fea_desc'], link_obj.get_status_display()))
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@csrf_protect
@login_required    
def reset_featurelink(request, feature, digest):
    #try:
        return _do_config_featurelink(request, feature, digest, 'W')
    #except:
    #    raise Http404

@csrf_protect
@login_required    
def close_featurelink(request, feature, digest):
    #try:
        return _do_config_featurelink(request, feature, digest, 'C')
    #except:
    #    raise Http404


    
    