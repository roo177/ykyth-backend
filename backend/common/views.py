from rest_framework.permissions import DjangoModelPermissions

class NoQuerysetDjangoModelPermissions(DjangoModelPermissions):
    """
    Custom permission class that allows DjangoModelPermissions
    without requiring a `.queryset` attribute or `.get_queryset()` method.
    """
    def get_queryset(self, view):
        return None
    
