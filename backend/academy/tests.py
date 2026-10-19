from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.core.management import call_command
from .models import ChildProfile
class MissionTests(TestCase):
 def setUp(self):
  call_command('seed_mission',verbosity=0)
  self.parent=User.objects.create_user(username='parent',password='StrongPass123!')
  self.other=User.objects.create_user(username='other',password='StrongPass123!')
  self.child=ChildProfile.objects.create(parent=self.parent,nickname='Explorer',age=9)
  self.client=APIClient();self.client.force_authenticate(user=self.parent)
 def test_mission_hides_correct_answers(self):
  data=self.client.get('/api/missions/meet-ai/').data
  self.assertNotIn('correct_index',str(data['questions']))
 def test_submission_and_badge(self):
  from .models import Mission
  qs=list(Mission.objects.get(slug='meet-ai').questions.all())
  answers={str(q.id):q.correct_index for q in qs}
  result=self.client.post(f'/api/children/{self.child.id}/missions/meet-ai/submit/',{'answers':answers},format='json')
  self.assertEqual(result.status_code,200);self.assertTrue(result.data['passed'])
  self.assertEqual(len(self.client.get(f'/api/children/{self.child.id}/progress/').data['badges']),1)
 def test_cannot_access_other_child(self):
  self.client.force_authenticate(user=self.other)
  self.assertEqual(self.client.get(f'/api/children/{self.child.id}/progress/').status_code,404)
 def test_age_gate(self):
  child=ChildProfile.objects.create(parent=self.parent,nickname='Older',age=13)
  result=self.client.post(f'/api/children/{child.id}/missions/meet-ai/submit/',{'answers':{}},format='json')
  self.assertEqual(result.status_code,403)
