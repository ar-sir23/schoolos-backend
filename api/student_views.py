from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication
from core.models import Student, Grade, Section, AcademicYear, Parent
import datetime

class StudentListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        try:
            students = Student.objects.filter(is_active=True).select_related('grade','section','parent')
            data = [{
                'id': s.id,
                'student_id': s.student_id,
                'full_name': s.full_name,
                'gender': s.gender,
                'cls': f"{s.grade.name if s.grade else ''}-{s.section.name if s.section else ''}",
                'att': 95,
                'fee': 'Paid',
                'risk': 'Low',
                'parent': s.parent.name if s.parent else '',
                'phone': s.parent.phone if s.parent else '',
            } for s in students]
            return Response({'results': data, 'count': len(data)})
        except Exception as e:
            return Response({'results': [], 'count': 0})

    def post(self, request):
        try:
            data = request.data
            year, _ = AcademicYear.objects.get_or_create(
                is_current=True,
                defaults={'name':'2025-2026','start_date':'2025-01-01','end_date':'2026-12-31'}
            )
            grade = None
            if data.get('grade'):
                grade, _ = Grade.objects.get_or_create(name=data['grade'], defaults={'order':1})
            section = None
            if grade and data.get('section'):
                section, _ = Section.objects.get_or_create(grade=grade, name=data['section'])
            parent = None
            if data.get('parent_name'):
                parent = Parent.objects.create(
                    name=data['parent_name'],
                    phone=data.get('parent_phone',''),
                    email=data.get('parent_email',''),
                )
            dob = data.get('date_of_birth') or '2010-01-01'
            student = Student.objects.create(
                student_id=data['student_id'],
                full_name=data['full_name'],
                gender=data.get('gender','M'),
                date_of_birth=dob,
                grade=grade,
                section=section,
                academic_year=year,
                roll_number=data.get('roll_number',''),
                parent=parent,
                is_active=True,
            )
            return Response({'success': True, 'id': student.id, 'name': student.full_name})
        except Exception as e:
            return Response({'error': str(e)}, status=400)
