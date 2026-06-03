import json
import anthropic
from django.conf import settings
from django.utils import timezone

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
MODEL  = settings.AI_MODEL

def ai_chatbot_reply(user_message, student_context, conversation_history):
    system = f"""You are SchoolOS Assistant, a helpful AI for school management.
Help parents and students with attendance, fees, results, and school queries.
Student context: {json.dumps(student_context)}
Be warm, concise. Answer in the same language the parent writes in."""
    messages = conversation_history + [{'role':'user','content':user_message}]
    response = client.messages.create(model=MODEL, max_tokens=1000, system=system, messages=messages)
    return response.content[0].text

def generate_report_card_comment(student_data):
    prompt = f"""Write a personalised school report card for:
{json.dumps(student_data, indent=2)}
Respond ONLY with valid JSON (no markdown):
{{"class_teacher_comment":"...","principal_comment":"...","areas_to_improve":["..."],"strengths":["..."],"overall_grade":"..."}}"""
    response = client.messages.create(model=MODEL, max_tokens=1000, messages=[{'role':'user','content':prompt}])
    raw = response.content[0].text.strip().replace('```json','').replace('```','').strip()
    return json.loads(raw)

def generate_attendance_alert(student_data):
    prompt = f"""Write an attendance alert for a parent.
Student data: {json.dumps(student_data)}
Respond ONLY with valid JSON:
{{"sms_message":"under 160 chars","email_subject":"...","email_body":"3 paragraphs"}}"""
    response = client.messages.create(model=MODEL, max_tokens=800, messages=[{'role':'user','content':prompt}])
    raw = response.content[0].text.strip().replace('```json','').replace('```','').strip()
    return json.loads(raw)

def predict_fee_default_risk(student_id):
    from core.models import Student
    from fees.models import FeeInvoice
    student  = Student.objects.get(pk=student_id)
    invoices = FeeInvoice.objects.filter(student=student).order_by('-due_date')[:12]
    history  = [{'status':i.status,'amount_due':float(i.amount_due),'amount_paid':float(i.amount_paid),'due_date':str(i.due_date)} for i in invoices]
    prompt   = f"""Analyse fee payment history and predict default risk.
Student: {student.full_name}
History: {json.dumps(history)}
Respond ONLY with valid JSON:
{{"risk_score":0-100,"risk_label":"low|medium|high","reason":"...","recommendation":"..."}}"""
    response = client.messages.create(model=MODEL, max_tokens=400, messages=[{'role':'user','content':prompt}])
    raw = response.content[0].text.strip().replace('```json','').replace('```','').strip()
    result = json.loads(raw)
    if invoices.exists():
        inv = invoices.first()
        inv.ai_risk_score = result['risk_score']
        inv.ai_risk_label = result['risk_label']
        inv.save(update_fields=['ai_risk_score','ai_risk_label'])
    return result

def run_bulk_risk_scoring():
    from core.models import Student
    scored = 0
    for s in Student.objects.filter(is_active=True):
        try: predict_fee_default_risk(s.pk); scored += 1
        except: continue
    return scored

def send_bulk_attendance_alerts(threshold=75.0):
    from core.models import Student
    from django.core.mail import send_mail
    sent = 0
    for student in Student.objects.filter(is_active=True).select_related('parent'):
        if student.current_attendance_rate < threshold and student.parent and student.parent.email:
            data = {'student_name':student.full_name,'parent_name':student.parent.name,
                    'grade':str(student.grade),'attendance_rate':student.current_attendance_rate}
            try:
                alert = generate_attendance_alert(data)
                send_mail(alert['email_subject'], alert['email_body'], settings.DEFAULT_FROM_EMAIL, [student.parent.email], fail_silently=True)
                sent += 1
            except: continue
    return sent
