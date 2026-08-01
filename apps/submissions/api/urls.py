from django.urls import path
from .views import CreateSubmission
from .views import RetrieveSubmission
from .views import ListSubmissions
from .views import ApproveSubmission
from .views import RequestRevisionSubmission

urlpatterns = [
    path('contracts/<int:contract_id>/create-submission/', CreateSubmission.as_view()),
    path('contracts/<int:contract_id>/submissions/', ListSubmissions.as_view()),
    path('submission/<int:pk>/retrieve/', RetrieveSubmission.as_view()),
    path('submission/<int:pk>/approve/', ApproveSubmission.as_view()),
    path('submission/<int:pk>/request-revision/', RequestRevisionSubmission.as_view()),
]