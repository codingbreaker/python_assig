import graphene

# Define GraphQL types
class Todo(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    time = graphene.String()
   

# Define queries
class Query(graphene.ObjectType):
    todos = graphene.List(Todo)

    def resolve_todos(self, info):
        # Replace this with actual database query to fetch todos
        todos_data = [
            {'id': 1, 'title': 'Task 1', 'description': 'Description for Task 1', 'time': '10:00 AM'},
            {'id': 2, 'title': 'Task 2', 'description': 'Description for Task 2', 'time': '11:00 AM'}
        ]
        return [Todo(**todo) for todo in todos_data]

# Define mutations
class CreateTodo(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String()
        time = graphene.String()
        

    todo = graphene.Field(Todo)

    def mutate(self, info, title, description, time):
        # Replace this with actual database creation logic
        global todos_data
        new_todo = {'id': len(todos_data) + 1, 'title': title, 'description': description, 'time': time}
        todos_data.append(new_todo)
        return CreateTodo(todo=Todo(**new_todo))

# Define the GraphQL schema
class Mutation(graphene.ObjectType):
    create_todo = CreateTodo.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

# Initialize an empty list for todos
todos_data = []

# Example usage:
# query_string = '{ todos { id title description time images } }'
# result = schema.execute(query_string)
# print(result.data)
