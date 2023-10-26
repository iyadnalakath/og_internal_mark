from . import views
from django.db import router
from django.urls import path
from rest_framework_nested import routers




urlpatterns = [
    path('admin/list/internalmark/', views.StudentSubjectMarks.as_view(), name='admin_internalmark'),
    path('admin/semester_counts/', views.SemesterCountAPIView.as_view(), name='semester-counts'),

]

urlpatterns =  urlpatterns
router = routers.DefaultRouter()
router.register("subject", views.SubjectViews,basename="subject"),
router.register("semester", views.SemesterViews,basename="semester"),
router.register("teacher/registration", views.TeacherRegistrationView,basename="teacher"),
router.register("student/add", views.StudentRegistrationView,basename="student"),
router.register("theory/internalmark", views.TheoryInternalMarkViews,basename="theory_internalmark"),
router.register("lab/internalmark", views.LabInternalMarkViews,basename="lab_internalmark"),
# router.register("admin/list/internalmark", views.StudentSubjectMarksViewSet,basename="admin_internalmark"),
# router.register("assignment/internalmark", views.TheoryInternalMarkViews,basename="theory_internalmark"),
# router.register("event_management_users", views.EventManagementUsersView)
# router.register('eventteamlistsubcatagory',views.EventManagementSubcategoryViewSet,basename='MyModel')


urlpatterns = router.urls + urlpatterns
