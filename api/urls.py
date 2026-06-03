from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import ai_views

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('ai/chat/', ai_views.chat, name='ai_chat'),
    path('ai/report-card/', ai_views.report_card, name='report_card'),
    path('ai/fee-risk/bulk/', ai_views.fee_risk, name='fee_risk'),
    path('ai/attendance-alerts/', ai_views.attendance_alerts, name='attendance_alerts'),
]
