from django.urls import path
from .views import CreateSubmission
from .views
from .views
from .views

urlpatterns = [
    path('contracts/<int:contract_id>/create-submission/', CreateSubmission.as_view()),
    path('contracts/<int:contract_id>/submissions/', ListSubmissions.as_view()),
    path('submission/<int:id>/approve/', ApproveSubmission.as_view()),
    path('submission/<int:id>/request-revision/', RequestRevisionSubmission.as_view()),
]