from django.contrib import admin
from django.urls import path
import git.views as git_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', git_views.usersPage, name='home'),
    path('repos/', git_views.reposPage, name='repo_page'),
    path('trending/repos/', git_views.trending_repo, name='trending_repo'),
    path('topics/', git_views.topics, name='topics'),
    path('topic/<str:slug>/<int:id>', git_views.repos_in_topic, name='repos_in_topic'),
    path('topic/<str:slug>/', git_views.trending_repos_in_topic, name='trending_repos_in_topic'),
    path('user/<str:slug>/', git_views.userDetail, name='user_detail'),
    path('search/user/<str:slug>/repo/', git_views.searchRepoInUser, name='search_repo_in_user'),
    path('search/topic/', git_views.searchTopic, name='search_topic'),
    path('search/user/', git_views.searchUser, name='search_user'),
    path('search/repo/', git_views.searchRepo, name='search_repo'),
    path('repo/<str:userSlug>/<str:rName>/<int:pk>/', git_views.repoDetail, name='repo_detail')
]
