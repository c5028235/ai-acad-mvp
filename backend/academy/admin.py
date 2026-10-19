from django.contrib import admin
from .models import ChildProfile,LearningPath,Mission,Activity,QuizQuestion,Badge,MissionProgress,QuizAttempt,ChildBadge
for model in [ChildProfile,LearningPath,Mission,Activity,QuizQuestion,Badge,MissionProgress,QuizAttempt,ChildBadge]:admin.site.register(model)
