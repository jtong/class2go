from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext
from datetime import datetime
from models import Course
from courses.actions import is_member_of_course
from courses.actions import auth_view_wrapper
from django.contrib import messages
from courses.common_page_data import get_common_page_data
from c2g.models import Course
from django.conf import settings
### C2G Core Views ###

@auth_view_wrapper
def home(request):
    #try:
    #    common_page_data = get_common_page_data(request, course_prefix, course_suffix)
    #except:
    raise Http404
    
    
    now = datetime.now()
    courses = Course.objects.filter(calendar_start__gt=now, mode="ready")
    available_course_list = []
    for course in courses:
        if is_member_of_course(course, request.user):
            course_student_member = 'True'
        else:
            course_student_member = 'False'
        
        viewable_handle = course.handle.replace('--', '/')
        available_course_list.append((course.title, course.handle, viewable_handle, course_student_member))
        
    return render_to_response('courses/signup.html', {'request': request, 'available_course_list': available_course_list}, context_instance=RequestContext(request))

def healthcheck(request):
    return HttpResponse("I'm alive!")

def throw500(request):
    raise Exception('Testing the exception--http500 mechanism')

def throw404(request):
    raise Http404

def hc(request):
    return render_to_response('honor_code.html',{},RequestContext(request))

def tos(request):
    return render_to_response('TOS.html',{},RequestContext(request))

def privacy(request):
    return render_to_response('privacy.html',{},RequestContext(request))
    
def faq(request):
    return render_to_response('faq.html',{'adminmail':settings.SERVER_EMAIL},context_instance=RequestContext(request))

def contactus(request):
    if request.GET.get('pre') and request.GET.get('post'):
        try:
            common_page_data = get_common_page_data(request, request.GET.get('pre'), request.GET.get('post'))
            course = common_page_data['course']
            staffmail=course.contact
        except Course.DoesNotExist:
            course=None
            staffmail=''
    else:
        course=None
        staffmail=''

    return render_to_response('contactus.html', 
                              {'request': request,
                               'course': course,
                               'staffmail' : staffmail,
                               'adminmail' : settings.SERVER_EMAIL,
                              },context_instance=RequestContext(request))

def test_messages(request):
    messages.add_message(request,messages.INFO, 'Hello World Info')
    messages.add_message(request,messages.SUCCESS, 'Hello World Success')
    messages.add_message(request,messages.WARNING, 'Hello World Warning')
    messages.add_message(request,messages.ERROR, 'Hello World Error')
            
    return HttpResponse("Messages Submitted, go back to regular page to view")
