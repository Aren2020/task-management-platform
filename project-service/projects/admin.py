from django.contrib import admin
from .models import Project, ProjectMember

class ProjectMemberInline(admin.TabularInline):
    """Inline for displaying project members directly in the project form."""

    model = ProjectMember
    extra = 1 
    fields = ['user_id', 'role', 'date_added']
    readonly_fields = ['date_added']

class ProjectAdmin(admin.ModelAdmin):

    list_display = ('pk', 'name', 'project_status',  'priority', 'start_date', 'end_date')
    list_filter = ('project_status', 'priority')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'owner_id')
        }),
        ('Project Dates', {
            'fields': ('start_date', 'end_date', 'deadline')
        }),
        ('Project Settings', {
            'fields': ('project_status', 'priority')
        })
    )
    inlines = [ProjectMemberInline]

class ProjectMemberAdmin(admin.ModelAdmin):
    """Admin configuration for the ProjectMember model."""
    list_display = ('project', 'user_id', 'role', 'date_added')
    list_filter = ('role', 'project')
    search_fields = ('user_id', 'role')
    ordering = ('-date_added',)

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectMember, ProjectMemberAdmin)
