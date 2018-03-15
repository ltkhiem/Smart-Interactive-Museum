from rest_framework import serializers

from repo.models import Repo, Class


class RepoSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Repo
        fields = ('id', 'name', 'owner', 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')


class ClassSerializer(serializers.ModelSerializer):

    repo = serializers.ReadOnlyField(source='repo.name')

    class Meta:
        model = Class
        fields = ('id', 'name', 'repo', 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')
