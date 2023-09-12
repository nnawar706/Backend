from rest_framework import serializers
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.validators import UniqueTogetherValidator
from .models import ExamRoom, ExamRoomHasStudents
from quizzes.models import Quiz
from datetime import date
import secrets
import string

class ExamRoomCreateSerializer (serializers.ModelSerializer):

    class Meta:
        model = ExamRoom
        fields = ['title', 'detail']

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        self.request = context.get('request')
        super().__init__(*args, **kwargs)

    def validate (self, data):
        existing_room = ExamRoom.objects.filter(user=self.request.user, title=data['title']).first()

        if existing_room:
            raise serializers.ValidationError('A room with the same title already exists.')

        if len(data['title']) < 5:
            raise serializers.ValidationError('Title field must be at least 5 characters long.')

        return data

    def create (self, data):
        room = ExamRoom(
            user    = self.request.user,
            title   = data['title'],
            detail  = data['detail'],
            secret  = generate_code(8)
        )

        room.save()

        return room


class ExamRoomSerializer (serializers.ModelSerializer):

    class Meta:
        model = ExamRoom
        exclude = ['user','secret']


class ExamRoomUpdateSerializer (serializers.ModelSerializer):

    class Meta:
        model = ExamRoom
        exclude = ['user','secret','created_at']

    def validate (self, data):
        instance = self.instance
        if 'title' in data and len(data['title']) < 5:
            raise serializers.ValidationError('Title field must be at least 5 characters long.')

        if 'title' in data and data['title'] != instance.title:
            existing_room = ExamRoom.objects.filter(user=instance.user, title=data['title']).first()
            if existing_room:
                raise serializers.ValidationError('A room with the same title already exists.')

        return data

    def update (self, instance, data):
        instance.title = data.get('title', instance.title)
        instance.detail = data.get('detail', instance.detail)
        instance.save()
        return instance


class ExamRoomActiveStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamRoom
        fields = ['status']

    def validate(self, data):
        instance = self.instance
        is_active = data.get('status', instance.status)

        if not is_active:
            if Quiz.objects.filter(room=instance, occurring_date__gt=date.today()).exists():
                raise serializers.ValidationError('Cannot archive exam room that has upcoming quizzes.')
        
        return data

    def change_status (self, instance, data):
        instance.status = not instance.status
        instance.save()


class ExamRoomJoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamRoom
        fields = ['secret']

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        self.request = context.get('request')
        super().__init__(*args, **kwargs)

    def validate (self, data):
        room = ExamRoom.objects.filter(secret=data['secret'], status = 1).first()

        if not room:
            raise serializers.ValidationError('No active classroom is available with given secret.')

        if room.students.filter(id = self.request.user.id).exists():
            raise serializers.ValidationError('You have already joined the classroom that is associated with the given secret.')

        return data

    def join_room (self, data):
        room = ExamRoom.objects.filter(secret=data['secret']).first()
        room.students.add(self.request.user)
        return data


class ExamRoomInvitationSerializer(serializers.Serializer):
    emails = serializers.ListField(child = serializers.EmailField())

    def send_invitation (self, secret, data):
        mail_template = 'invitation.html'
        mail_message = render_to_string(mail_template, context = {'secret': secret})
        subject = 'Invitation From QUIZBOT'
        email_from = settings.EMAIL_FROM_USER
        recipient_list = data['emails']
        mail = EmailMessage(subject, mail_message, email_from, recipient_list)
        mail.content_subtype = 'html'
        mail.send()


def generate_code (length=8):
    characters = string.digits
    random_string = ''.join(secrets.choice(characters) for _ in range(length))

    return random_string