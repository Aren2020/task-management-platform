import uuid
from django.db import models

class Project(models.Model):
    """Project model to manage projects and their details."""
    
    PROJECT_STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
        ('Cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    project_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    owner_id = models.UUIDField()
    name = models.CharField(max_length = 250)
    description = models.TextField(blank = True, null = True)
    
    project_status = models.CharField(max_length = 20, 
                                      choices = PROJECT_STATUS_CHOICES,
                                      default = 'Not Started')
    priority = models.CharField(max_length = 10,
                                choices = PRIORITY_CHOICES,
                                default = 'Medium')

    start_date = models.DateTimeField(null = True, blank = True)
    end_date = models.DateTimeField(null = True, blank = True)
    deadline = models.DateTimeField(null = True, blank = True)  # Final deadline for project completion

    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ('owner_id', 'name') 

class ProjectMember(models.Model):
    """Mapping between users and projects to manage members and their roles."""

    project = models.ForeignKey(Project, related_name = 'members', on_delete = models.CASCADE)
    user_id = models.UUIDField()
    
    role = models.CharField(max_length = 50)  # Role within the project (e.g., Developer, Designer, etc.)
    date_added = models.DateTimeField(auto_now_add = True)
 
    def __str__(self):
        return f'{self.user.username} - {self.role}'

    class Meta:
        unique_together = ('project', 'user_id')  # Ensure a user can't be added to the same project more than once