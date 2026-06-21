from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.ai_views import ChatbotView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/profile/', RedirectView.as_view(url='/admin/')),
    path('api/auth/token/', TokenObtainPairView.as_view()),
    path('api/auth/token/refresh/', TokenRefreshView.as_view()),
    path('api/ai/chat/', ChatbotView.as_view()),
    path('', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from api.student_views import StudentListView
urlpatterns += [path('api/students/', StudentListView.as_view())]

from api.signup_views import SchoolSignupView, PricingPlansView
urlpatterns += [
    path('api/signup/', SchoolSignupView.as_view()),
    path('api/pricing/', PricingPlansView.as_view()),
]
