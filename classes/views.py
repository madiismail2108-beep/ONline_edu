from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Course, Module, Lesson, Topic
from django.contrib.auth import logout
from .forms import TopicForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from .models import User
from django.http import HttpResponse
from django.contrib import messages

def topic_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    topics = Topic.objects.filter(lesson__module__course=course).order_by('order')

    return render(request, 'courses/classes/topic_list.html', {
        'course': course,
        'topics': topics
    })

def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    
    return render(request, 'courses/classes/topic_detail.html', {
        'topic': topic
    })

def topic_create(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = TopicForm()

    return render(request, 'courses/classes/topic_form.html', {
        'form': form
    })

def topic_update(request, pk):
    topic = get_object_or_404(Topic, pk=pk)

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('topic_detail', pk=topic.pk)
    else:
        form = TopicForm(instance=topic)

    return render(request, 'courses/classes/topic_form.html', {
        'form': form,
        'topic': topic
    })

def topic_delete(request, pk):
    topic = get_object_or_404(Topic, pk=pk)

    if request.method == 'POST':
        topic.delete()
        return redirect('course_list')

    return render(request, 'courses/classes/topic_confirm_delete.html', {
        'topic': topic
    })

def logout_view(request):
    logout(request)
    return redirect('login')

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})

def module_detail(request, pk):
    module = get_object_or_404(Module, pk=pk)
    return render(request, 'courses/module_detail.html', {'module': module})

def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    return render(request, 'courses/lesson_detail.html', {'lesson': lesson})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/lists/course_list.html', {'courses': courses})

def module_list(request):
    modules = Module.objects.all()
    return render(request, 'courses/lists/module_list.html', {'modules': modules})

def lesson_list(request):
    lessons = Lesson.objects.all()
    return render(request, 'courses/lists/lesson_list.html', {'lessons': lessons})

def home(request):
    return render(request, 'home.html')

def admin_only(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to perform this action.")

def create_course(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Only admin can create courses!")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        Course.objects.create(
            title=title,
            description=description,
            image=image
        )

        return redirect("course_list")

    return render(request, "courses/add/create_course.html")

def create_module(request, course_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Only admin can create modules!")

    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        Module.objects.create(
            course=course,
            title=title,
            description=description
        )

        return redirect("course_detail", pk=course_id)

    return render(request, "courses/add/create_module.html", {"course": course})

def create_lesson(request, module_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Only admin can create lessons!")

    module = get_object_or_404(Module, id=module_id)

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        video_url = request.POST.get("video_url")



        Lesson.objects.create(
            module=module,
            title=title,
            content=content,
            video_url=video_url
        )

        return redirect("module_detail", pk=module_id)

    return render(request, "courses/add/create_lesson.html", {"module": module})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        mail_subject = 'Activate your account'
        message = render_to_string('accounts/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        email = EmailMessage(
            mail_subject,
            message,
            to=[email]
        )
        email.send()

        return render(request, 'accounts/check_email.html')

    return render(request, 'accounts/register.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Account activated successfully')
    else:
        return HttpResponse('Activation link is invalid!')


# Create your views here.
