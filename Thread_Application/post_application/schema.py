import graphene
from graphene_django import DjangoObjectType
from .models import Thread

class ThreadType(DjangoObjectType):
    class Meta:
        model=Thread

class Query(graphene.ObjectType):
    all_threads = graphene.List(ThreadType)
    thread_by_id = graphene.Field(ThreadType, id=graphene.Int(required=True))

    def resolve_all_threads(self, info):
        return Thread.objects.all()

    def resolve_thread_by_id(self, info, id):
        try:
            return Thread.objects.get(id=id)
        except Thread.DoesNotExist:
            return None

class CreateThread(graphene.Mutation):
    class Arguments:
        title=graphene.String(required=True)
        description=graphene.String(required=True)

    thread=graphene.Field(ThreadType)

    def mutate(self,info,title,description):
        thread=Thread(title=title,description=description)
        thread.save()
        return CreateThread(thread=thread)    
class UpdateThread(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()

    thread = graphene.Field(ThreadType)

    def mutate(self, info, id, title=None, description=None):
        thread = Thread.objects.get(id=id)
        if title:
            thread.title = title
        if description:
            thread.description = description
        thread.save()
        return UpdateThread(thread=thread)

class DeleteThread(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        try:
            thread = Thread.objects.get(id=id)
            thread.delete()
            return DeleteThread(ok=True)
        except Thread.DoesNotExist:
            return DeleteThread(ok=False)

class Mutation(graphene.ObjectType):
    create_thread = CreateThread.Field()
    update_thread = UpdateThread.Field()
    delete_thread = DeleteThread.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)