from rest_framework.permissions import BasePermission
from users.models import Publisher

class VerifySecretKey(BasePermission):
    
    def has_permission(self, request, view):
        key = request.data.get('key')
        user_id = request.data.get('id')

        try:
            # Fetch the Publisher instance based on user_id
            user = Publisher.objects.get(pk=int(user_id))
        except Publisher.DoesNotExist:
            return False
        
        # Assuming user.secret_key.key is the actual secret key to match against
        actual_key = user.secret_key.key if user.secret_key else None
        
        # Check if the provided key matches the actual key
        print(actual_key,key)
        return actual_key == key
    
class CommentorCreatorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.user.username )
        print(obj.created_by.username)
        return request.user.username == obj.created_by.username
    

class VotedUserOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            print(request.user.pk,obj.user.pk)
            return request.user.pk == obj.user.pk