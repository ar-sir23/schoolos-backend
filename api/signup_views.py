"""
api/signup_views.py
Self-service school signup -- any school can register and get instant access.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from tenants.services import onboard_new_school


class SchoolSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        required = ['school_name', 'admin_email', 'admin_password', 'admin_name', 'phone']
        missing = [f for f in required if not data.get(f)]
        if missing:
            return Response(
                {'error': 'Missing required fields: ' + ', '.join(missing)},
                status=status.HTTP_400_BAD_REQUEST
            )

        plan = data.get('plan', 'free')
        if plan not in ['free', 'starter', 'growth', 'scale']:
            plan = 'free'

        try:
            result = onboard_new_school(
                school_name=data['school_name'],
                admin_email=data['admin_email'],
                admin_password=data['admin_password'],
                plan=plan,
            )
            result['message'] = 'School created successfully! You can now log in.'
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PricingPlansView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        plans = [
            {
                'id': 'free', 'name': 'Free Trial', 'price': 0, 'period': '14 days',
                'max_students': 100,
                'features': ['Student management', 'Basic attendance', 'Fee tracking', 'Admin panel'],
            },
            {
                'id': 'starter', 'name': 'Starter', 'price': 2500, 'period': 'month',
                'max_students': 500,
                'features': ['Everything in Free', 'Parent portal', 'SMS alerts', 'Email support'],
            },
            {
                'id': 'growth', 'name': 'Growth', 'price': 6000, 'period': 'month',
                'max_students': 2000,
                'features': ['Everything in Starter', 'AI chatbot', 'AI report cards', 'Fee risk prediction'],
                'popular': True,
            },
            {
                'id': 'scale', 'name': 'Scale', 'price': 12000, 'period': 'month',
                'max_students': 999999,
                'features': ['Everything in Growth', 'Multi-branch', 'Custom domain', 'Dedicated support'],
            },
        ]
        return Response({'plans': plans})
