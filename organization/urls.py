from django.urls import path
from .views import OrganisationListView, OrganisationDetailView, OrganisationCreateView, AddUserToOrganisationView

urlpatterns = [
    path('api/organisations/', OrganisationListView.as_view(), name='organisation_list'),
    path('api/organisations/<str:orgId>/', OrganisationDetailView.as_view(), name='organisation_detail'),
    path('api/organisations/', OrganisationCreateView.as_view(), name='organisation_create'),
    path('api/organisations/<str:orgId>/users/', AddUserToOrganisationView.as_view(), name='add_user_to_organisation'),
]
