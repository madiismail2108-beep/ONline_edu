from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Course, Module, Lesson

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

        Lesson.objects.create(
            module=module,
            title=title,
            content=content
        )

        return redirect("module_detail", pk=module_id)

    return render(request, "courses/add/create_lesson.html", {"module": module})
# Create your views here.
