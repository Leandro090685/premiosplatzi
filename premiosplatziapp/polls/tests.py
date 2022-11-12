import datetime

from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls.base import reverse

class QuestionModelTest(TestCase):
    
    def test_was_publish_recently_with_future_questions(self):
        """was_publish_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿Quien es el mejor CD de Platzi?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_publish_recently_with_past_questions(self):
        """was_publish_recently returns False for questions whose pub_date is in the past"""
        time = timezone.now() - datetime.timedelta(days=2)
        past_question = Question(question_text="¿Quien es el mejor CD de Platzi?", pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)
    
    def test_was_publish_recently_with_present_questions(self):
        """was_publish_recently returns False for questions whose pub_date is in the present"""
        time = timezone.now()
        present_question= Question(question_text="¿Quien es el mejor CD de Platzi?", pub_date=time)
        self.assertIs(present_question.was_published_recently(), True)

def create_question(question_text,days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """If no question exist, an apropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_future_question_no_displayed(self):
        """If created the question with pub_date in in the future, this question no displayed"""
        create_question("future question",days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")

        
    def test_past_question_no_displayed(self):
        """If created the question with pub_date in in the past, this question displayed"""
        question = create_question("past question",days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[question] )
    
    def two_question_future(self):
        question1 = create_question("question1",days=10)
        question2 = create_question("question2",days=20)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[] )


        