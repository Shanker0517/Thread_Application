import graphene
import post_application.schema

class Query(post_application.schema.Query, graphene.ObjectType):
    pass

class Mutation(post_application.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)