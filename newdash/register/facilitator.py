# from django.views import View
# from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse
# from django.contrib.auth.mixins import LoginRequiredMixin
# from newdash.models import Course, FacilitatorRegistration

# class FacilitatorRequestView(LoginRequiredMixin, View):
#     def get(self, request):
#         # Get all courses to render in the form
#         courses = Course.objects.all()
#         return render(request, 'dashboard/unbord_facilitaor.html', {'courses': courses})

#     def post(self, request):
#         course_id = request.POST.get('course')

#         if not course_id:
#             return JsonResponse({'error': 'Course ID not provided'}, status=400)

#         course = get_object_or_404(Course, id=course_id)

#         if course.facilitators:
#             return JsonResponse({'error': 'This course already has a facilitator.'}, status=400)

#         if FacilitatorRegistration.objects.filter(user=request.user, course=course).exists():
#             return JsonResponse({'error': 'You have already applied for this course.'}, status=400)

#         FacilitatorRegistration.objects.create(
#             user=request.user,
#             course=course,
#             approved=False
#         )

#         return JsonResponse({'success': f'Your request to become a facilitator for {course.name} has been submitted.'})
