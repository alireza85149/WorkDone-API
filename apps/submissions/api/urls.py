from django.urls import path

urlpatterns = [
    path('contracts/<int:id>/create-submission/', CreateSubmission.as_view()),
    path('contracts/<int:id>/submissions/', ListSubmissions.as_view()),
    path('submission/<int:id>/approve/', ApproveSubmission.as_view()),
    path('submission/<int:id>/request-revision/', RequestRevisionSubmission.as_view()),
]