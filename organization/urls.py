from django.urls import path
from .views import OrganisationListCreateView, OrganisationDetailView,  AddUserToOrganisationView
from members.views import UserDetailView
urlpatterns = [
    path('organisations/', OrganisationListCreateView.as_view(), name='organisation_list'),
    path('organisations/<str:orgId>/', OrganisationDetailView.as_view(), name='organisation_detail'),
    path('organisations/<str:orgId>/users/', AddUserToOrganisationView.as_view(), name='add_user_to_organisation'),
    path('users/<str:id>/', UserDetailView.as_view(), name='user_detail'),
]
