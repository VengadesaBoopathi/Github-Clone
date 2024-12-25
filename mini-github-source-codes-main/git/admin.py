import imp
from django.contrib import admin
from .models import gitUser, Repo, GitToken, TrendingRepo, Topic

class RepoAdmin1(admin.TabularInline):
    model = Repo

class gitUserAdmin1(admin.ModelAdmin):
    inlines = [RepoAdmin1]

admin.site.register(gitUser, gitUserAdmin1)
admin.site.register(GitToken)
admin.site.register(TrendingRepo)
admin.site.register(Topic)

