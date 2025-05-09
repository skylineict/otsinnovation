from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST
from .models import Course, LiveClass, Attendance
from .forms import LiveClassForm, JoinClassForm

class FacilitatorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        course_id = self.kwargs.get('course_id')
        if course_id:
            return Course.objects.filter(id=course_id, facilitators=self.request.user).exists()
        live_class_id = self.kwargs.get('pk')
        if live_class_id:
            return LiveClass.objects.filter(id=live_class_id, facilitator=self.request.user).exists()
        return False

# Facilitator Views
@login_required
def facilitator_dashboard(request):
    teaching_courses = Course.objects.filter(facilitators=request.user)
    upcoming_classes = LiveClass.objects.filter(
        facilitator=request.user,
        status='scheduled',
        scheduled_start__gt=timezone.now()
    ).order_by('scheduled_start')
    active_classes = LiveClass.objects.filter(
        facilitator=request.user, 
        status='active'
    )
    
    context = {
        'teaching_courses': teaching_courses,
        'upcoming_classes': upcoming_classes,
        'active_classes': active_classes,
    }
    return render(request, 'elearning/facilitator_dashboard.html', context)

class LiveClassCreateView(LoginRequiredMixin, FacilitatorRequiredMixin, CreateView):
    model = LiveClass
    form_class = LiveClassForm
    template_name = 'elearning/live_class_form.html'
    
    def form_valid(self, form):
        form.instance.facilitator = self.request.user
        form.instance.course_id = self.kwargs.get('course_id')
        response = super().form_valid(form)
        
        # Create attendance records for all enrolled students
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        for enrollment in course.courseenrollment_set.all():
            Attendance.objects.create(
                live_class=self.object,
                student=enrollment.student
            )
        
        messages.success(self.request, f"Live class '{form.instance.title}' created successfully!")
        return response
    
    def get_success_url(self):
        return reverse('course_detail', kwargs={'pk': self.kwargs.get('course_id')})

class LiveClassDetailView(LoginRequiredMixin, DetailView):
    model = LiveClass
    template_name = 'elearning/live_class_detail.html'
    context_object_name = 'live_class'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        live_class = self.get_object()
        attendances = live_class.attendances.all()
        
        is_facilitator = (live_class.facilitator == self.request.user)
        can_join = False
        has_marked_attendance = False
        
        if not is_facilitator:
            # Check if the user is enrolled in the course and has an attendance record
            student_attendance = attendances.filter(student=self.request.user).first()
            can_join = student_attendance is not None and live_class.is_active()
            has_marked_attendance = student_attendance is not None and student_attendance.status == 'present'
        
        context.update({
            'is_facilitator': is_facilitator,
            'can_join': can_join,
            'has_marked_attendance': has_marked_attendance,
            'attendances': attendances,
        })
        return context

@login_required
@require_POST
def activate_live_class(request, pk):
    live_class = get_object_or_404(LiveClass, pk=pk)
    
    if live_class.facilitator != request.user:
        return JsonResponse({"success": False, "message": "You don't have permission to activate this class"}, status=403)
    
    success = live_class.activate()
    if success:
        return JsonResponse({
            "success": True,
            "message": f"Live class '{live_class.title}' is now active!"
        })
    else:
        return JsonResponse({
            "success": False, 
            "message": "Could not activate this class. It may already be active or completed."
        })

@login_required
@require_POST
def end_live_class(request, pk):
    live_class = get_object_or_404(LiveClass, pk=pk)
    
    if live_class.facilitator != request.user:
        return JsonResponse({"success": False, "message": "You don't have permission to end this class"}, status=403)
    
    success = live_class.end_class()
    if success:
        return JsonResponse({
            "success": True,
            "message": f"Live class '{live_class.title}' has been completed!"
        })
    else:
        return JsonResponse({
            "success": False,
            "message": "Could not end this class. It may not be active."
        })

@login_required
@require_POST
def mark_attendance(request, class_id):
    live_class = get_object_or_404(LiveClass, id=class_id)
    
    if live_class.facilitator != request.user:
        return JsonResponse({"success": False, "message": "You don't have permission to mark attendance"}, status=403)
    
    student_id = request.POST.get('student_id')
    status = request.POST.get('status')
    
    attendance = get_object_or_404(Attendance, live_class=live_class, student_id=student_id)
    attendance.status = status
    if status == 'present' and not attendance.join_time:
        attendance.join_time = timezone.now()
    attendance.save()
    
    return JsonResponse({
        'success': True,
        'message': f"Attendance marked as {status} successfully"
    })

@login_required
@require_POST
def toggle_attendance_button(request, class_id):
    live_class = get_object_or_404(LiveClass, id=class_id)
    
    if live_class.facilitator != request.user:
        return JsonResponse({"success": False, "message": "You don't have permission to toggle attendance button"}, status=403)
    
    is_active = request.POST.get('is_active') == 'true'
    live_class.attendance_button_active = is_active
    live_class.save()
    
    message = "Attendance button activated!" if is_active else "Attendance button deactivated!"
    return JsonResponse({
        'success': True,
        'message': message
    })

# Student Views
@login_required
def student_dashboard(request):
    enrolled_courses = Course.objects.filter(students=request.user)
    upcoming_classes = LiveClass.objects.filter(
        course__in=enrolled_courses,
        status='scheduled',
        scheduled_start__gt=timezone.now()
    ).order_by('scheduled_start')
    active_classes = LiveClass.objects.filter(
        course__in=enrolled_courses,
        status='active'
    )
    
    # Get attendance states for active classes
    attendance_states = {}
    for live_class in active_classes:
        attendance = Attendance.objects.filter(
            live_class=live_class,
            student=request.user
        ).first()
        
        if attendance:
            attendance_states[live_class.id] = {
                'status': attendance.status,
                'can_mark': live_class.attendance_button_active and attendance.status != 'present'
            }
    
    context = {
        'enrolled_courses': enrolled_courses,
        'upcoming_classes': upcoming_classes,
        'active_classes': active_classes,
        'attendance_states': attendance_states,
    }
    return render(request, 'elearning/student_dashboard.html', context)

@login_required
def join_live_class(request):
    if request.method == 'POST':
        form = JoinClassForm(request.POST)
        if form.is_valid():
            join_code = form.cleaned_data['join_code']
            try:
                live_class = LiveClass.objects.get(join_code=join_code, status='active')
                
                # Check if student is enrolled in the course
                if not live_class.course.students.filter(id=request.user.id).exists():
                    return JsonResponse({
                        "success": False,
                        "message": "You are not enrolled in this course."
                    })
                
                # Mark attendance
                attendance, created = Attendance.objects.get_or_create(
                    live_class=live_class,
                    student=request.user,
                    defaults={'status': 'absent'}
                )
                attendance.mark_present()
                
                return JsonResponse({
                    "success": True,
                    "message": f"You've joined the live class: {live_class.title}",
                    "redirect_url": reverse('live_class_detail', kwargs={'pk': live_class.id})
                })
                
            except LiveClass.DoesNotExist:
                return JsonResponse({
                    "success": False,
                    "message": "Invalid join code or the class is not currently active."
                })
    else:
        form = JoinClassForm()
    
    return render(request, 'elearning/join_class.html', {'form': form})

@login_required
@require_POST
def mark_student_attendance(request, pk):
    live_class = get_object_or_404(LiveClass, pk=pk)
    
    # Verify the class is active and has attendance button enabled
    if not live_class.status == 'active' or not live_class.attendance_button_active:
        return JsonResponse({
            "success": False,
            "message": "Attendance marking is not currently available for this class."
        })
    
    # Verify the student is enrolled in this course
    if not live_class.course.students.filter(id=request.user.id).exists():
        return JsonResponse({
            "success": False,
            "message": "You are not enrolled in this course."
        }, status=403)
    
    attendance = get_object_or_404(Attendance, live_class=live_class, student=request.user)
    
    # Only allow marking if not already present
    if attendance.status == 'present':
        return JsonResponse({
            "success": False,
            "message": "Your attendance is already marked for this class."
        })
    
    attendance.status = 'present'
    attendance.join_time = timezone.now()
    attendance.save()
    
    return JsonResponse({
        "success": True,
        "message": "Your attendance has been marked successfully!"
    })

@login_required
@require_POST
def leave_live_class(request, pk):
    live_class = get_object_or_404(LiveClass, pk=pk)
    
    # Verify the student is enrolled in this course
    if not live_class.course.students.filter(id=request.user.id).exists():
        return JsonResponse({
            "success": False,
            "message": "You are not enrolled in this course."
        }, status=403)
    
    attendance = get_object_or_404(Attendance, live_class=live_class, student=request.user)
    attendance.mark_leave()
    
    return JsonResponse({
        "success": True,
        "message": "You have left the live class. Your attendance has been recorded."
    })

@login_required
def get_active_classes_status(request):
    """API endpoint to check for active classes with attendance button status"""
    enrolled_courses = Course.objects.filter(students=request.user)
    active_classes = LiveClass.objects.filter(
        course__in=enrolled_courses,
        status='active'
    )
    
    classes_data = []
    for live_class in active_classes:
        attendance = Attendance.objects.filter(
            live_class=live_class,
            student=request.user
        ).first()
        
        classes_data.append({
            'id': live_class.id,
            'title': live_class.title,
            'course': live_class.course.title,
            'attendance_button_active': live_class.attendance_button_active,
            'attendance_status': attendance.status if attendance else 'unknown',
            'can_mark_attendance': live_class.attendance_button_active and 
                                  attendance and 
                                  attendance.status != 'present'
        })
    
    return JsonResponse({'classes': classes_data})
