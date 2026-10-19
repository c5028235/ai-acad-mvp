from django.core.management.base import BaseCommand
from academy.models import LearningPath, Mission, Activity, QuizQuestion, Badge


class Command(BaseCommand):
    help = 'Create or update Mission 1 sample content'

    def handle(self, *args, **kwargs):
        path, _ = LearningPath.objects.update_or_create(
            slug='ai-explorers', defaults={'title': 'AI Explorers (8–10)', 'min_age': 8, 'max_age': 10})
        mission, _ = Mission.objects.update_or_create(slug='meet-ai', defaults={'path': path, 'title': 'Meet AI - The Mystery Machine', 'summary': 'Discover AI in everyday life and learn why we should check its answers.', 'objectives': [
                                                      'Explain AI simply', 'Spot everyday AI', 'Recognise AI mistakes', 'Think independently'], 'order': 1, 'duration_minutes': 18, 'is_published': True})
        activities = [
            ('Welcome to the Discovery Lab', 'story', {
             'narration': "Hey, Explorer! I'm Nova, your robot guide. AI helps computers recognise pictures, understand questions and make predictions. But AI isn't magic, and it can make mistakes!"}),
            ('Spot the AI', 'choice', {'prompt': 'Which of these uses AI?', 'options': ['An app recognising a cat in a photo', 'A basic calculator adding 2 + 3',
             'A torch with a simple switch'], 'correct_index': 0, 'explanation': 'Image recognition can use AI; basic arithmetic and switches do not require it.'}),
            ('Nova Makes a Mistake', 'choice', {'prompt': 'Nova says every bird can fly. What should you do?', 'options': [
             'Believe Nova', 'Check the claim: penguins cannot fly', 'Repeat the answer without checking'], 'correct_index': 1, 'explanation': 'AI can sound confident while being wrong. Check facts with trusted sources.'}),
            ('Think First', 'reflection', {'prompt': 'Name one thing you can do to check an AI answer. Think of your own answer before continuing.',
             'guidance': 'Compare with a trusted book, teacher or parent. No response is sent to an AI service.'}),
        ]
        for n, (title, kind, content) in enumerate(activities, 1):
            Activity.objects.update_or_create(mission=mission, order=n, defaults={
                                              'title': title, 'kind': kind, 'content': content})
        questions = [
            ('What does AI stand for?', ['Automatic Internet', 'Artificial Intelligence',
             'Amazing Information'], 1, 'AI means Artificial Intelligence.'),
            ('Which of these can use AI?', ['An app identifying animals in pictures',
                                            'A normal pencil', 'A paper notebook'], 0, 'AI can help identify objects in images.'),
            ('Can AI sometimes give incorrect answers?', [
                'Yes', 'No', 'Only when the internet is off'], 0, 'AI can be wrong even when it sounds confident.'),
            ('What should you do if an AI answer sounds strange?', [
                'Believe it immediately', 'Copy it without checking', 'Check with a trusted source or adult'], 2, 'Verify important information.'),
            ('Which is a good way to learn with AI?', ['Let AI do all your thinking', 'Try yourself, then use AI to help understand',
                                                       'Copy everything AI says'], 1, 'AI should support your thinking, not replace it.'),
        ]
        for n, (prompt, options, correct_index, explanation) in enumerate(questions, 1):
            QuizQuestion.objects.update_or_create(mission=mission, order=n, defaults={
                                                  'prompt': prompt, 'options': options, 'correct_index': correct_index, 'explanation': explanation})
        Badge.objects.update_or_create(slug='ai-discovery', defaults={
                                       'title': 'AI Discovery Badge', 'description': 'Completed Mission 1 with at least 80% accuracy', 'mission': mission})
        self.stdout.write(self.style.SUCCESS('Mission 1 seeded successfully.'))
