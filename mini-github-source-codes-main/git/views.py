from django.shortcuts import render
from .models import Topic, gitUser,Repo,TrendingRepo
from django.db.models import Q
from django.shortcuts import redirect
import json



strrrr= '[{"topic": "react\n\n", "url": "https://github.com/topics/react"}, {"topic": "css\n\n", "url": "https://github.com/topics/css"}, {"topic": "kotlin\n\n", "url": "https://github.com/topics/kotlin"}, {"topic": "config\n\n", "url": "https://github.com/topics/config"}, {"topic": "python\n\n", "url": "https://github.com/topics/python"}, {"topic": "c\n\n", "url": "https://github.com/topics/c"}, {"topic": "html\n\n", "url": "https://github.com/topics/html"}, {"topic": "app\n\n", "url": "https://github.com/topics/app"}, {"topic": "python3\n\n", "url": "https://github.com/topics/python3"}, {"topic": "github-config\n\n", "url": "https://github.com/topics/github-config"}]'


def usersPage(request):
    users = gitUser.objects.all().filter(has_details = True).order_by('-id')[3:50]
    count = gitUser.objects.all().count()
    count1 = gitUser.objects.all().filter(has_details = True).count()
    top_topics = Topic.objects.all().order_by('?')[0:10]

    try:
        trending_topics = json.decoder.JSONDecoder().decode(TrendingRepo.objects.all().last().pop_topics_list)
    except:
        trending_topics = json.decoder.JSONDecoder().decode(strrrr)


    context = {
        'top_topics' : top_topics,
        'users': users,
        'count': count,
        'count1': count1,
        'trending_topics': trending_topics
    }
    return render(request, 'git/home.html', context)

def reposPage(request):
    repos = Repo.objects.all().order_by('-id')[3:40]
    try:
        trending_topics = json.decoder.JSONDecoder().decode(TrendingRepo.objects.all().last().pop_topics_list)
    except:
        trending_topics = json.decoder.JSONDecoder().decode(strrrr)
    top_topics = Topic.objects.all().order_by('?')[0:10]

    context = {
         'top_topics' : top_topics,
        'repos': repos,
        'trending_topics': trending_topics
    }
    return render(request, 'git/home_repos.html', context)

def topics(request):
    # most_searched_topics = Topic.objects.all().order_by('id')[0:180]
    most_searched_topics = Topic.objects.all().order_by('?')[0:30]
    try:
        trending_topics = json.decoder.JSONDecoder().decode(TrendingRepo.objects.all().last().pop_topics_list)
    except:
        trending_topics = json.decoder.JSONDecoder().decode(strrrr)
    top_topics = Topic.objects.all().order_by('?')[0:10]

    context = {
         'top_topics' : top_topics,
        'most_searched_topics': most_searched_topics,
        'trending_topics': trending_topics
    }
    return render(request, 'git/topics.html', context)

def repos_in_topic(request, slug, id):
    try:
        trending_topics = json.decoder.JSONDecoder().decode(TrendingRepo.objects.all().last().pop_topics_list)
    except:
        trending_topics = json.decoder.JSONDecoder().decode(strrrr)
    topic = Topic.objects.all().filter(id=id).first()
    repos_in_topic = topic.repos_in_topic.all()
    top_topics = Topic.objects.all().order_by('?')[0:10]

    context = {
         'top_topics' : top_topics,
        'repos_in_topic': repos_in_topic,
        'trending_topics': trending_topics,
        'topic': topic
    }
    return render(request, 'git/repos_in_topic.html', context)   

def searchTopic(request):

    try:
        trending_topics = json.decoder.JSONDecoder().decode(TrendingRepo.objects.all().last().pop_topics_list)
    except:
        trending_topics = json.decoder.JSONDecoder().decode(strrrr)
    top_topics = Topic.objects.all().order_by('?')[0:10]

    if request.method == "GET":
        searched_topic = request.GET['searched_topic']
        most_searched_topics = Topic.objects.all().filter(topic__contains = searched_topic)
        context = {
         'top_topics' : top_topics,
        'most_searched_topics': most_searched_topics,
        'trending_topics': trending_topics,
        'searched': searched_topic
        }
    else:
        most_searched_topics = Topic.objects.all()
        context = {
         'top_topics' : top_topics,
        'most_searched_topics': most_searched_topics,
        'trending_topics': trending_topics
    }
    return render(request, 'git/topics.html', context)


def searchRepo(request):

    if request.method == "GET":
        searched_repo = request.GET['searched_repo']
        repos = Repo.objects.all().filter(Q(name__contains = searched_repo) | Q(all_languages__contains = searched_repo))
        if searched_repo == None:
            print('something')
    else:
        repos = Repo.objects.all().order_by('-id')[0:20]
        pass
    try:
        trending_topics = json.decoder.JSONDecoder().decode(TrendingRepo.objects.all().last().pop_topics_list)
    except:
        trending_topics = json.decoder.JSONDecoder().decode(strrrr)
    top_topics = Topic.objects.all().order_by('?')[0:10]

    context = {
         'top_topics' : top_topics,
        'repos': repos,
        'searched': searched_repo,
        'trending_topics': trending_topics
    }
    return render(request, 'git/home_repos.html', context)



def searchUser(request):

    if request.method == "GET":
        searched_user = request.GET['searched_user']
        if searched_user == None:
            # return redirect(usersPage)
            print('something')
        users = gitUser.objects.all().filter(Q(login__contains = searched_user) | Q(name__contains = searched_user))
    else:
        print("something")
        users = gitUser.objects.all().order_by('-id')[0:40]
        pass
    try:
        trending_topics = json.decoder.JSONDecoder().decode(TrendingRepo.objects.all().last().pop_topics_list)
    except:
        trending_topics = json.decoder.JSONDecoder().decode(strrrr)
    top_topics = Topic.objects.all().order_by('?')[0:10]

    context = {
         'top_topics' : top_topics,
        'users': users,
        'searched': searched_user,
        'trending_topics': trending_topics
    }
    return render(request, 'git/home.html', context)

def trending_repos_in_topic(request, slug):
    topic = Topic.objects.all().filter(slug = slug).last()
    repos_in_topic = topic.repos_in_topic.all()
    top_topics = Topic.objects.all().order_by('?')[0:10]


    context = {
         'top_topics' : top_topics,
        'repos_in_topic': repos_in_topic,
        'topic': topic
    }
    return render(request, 'git/repos_in_topic.html', context) 

def trending_repo(request):
    trending_repos = TrendingRepo.objects.all().last()
    try:
        trending_topics = json.decoder.JSONDecoder().decode(TrendingRepo.objects.all().last().pop_topics_list)
    except:
        trending_topics = json.decoder.JSONDecoder().decode(strrrr)
    top_topics = Topic.objects.all().order_by('?')[0:10]

    print(type(trending_repos.list))
    print(type(json.decoder.JSONDecoder().decode(trending_repos.list)))
    context = {
         'top_topics' : top_topics,
        'trending_repos': json.decoder.JSONDecoder().decode(trending_repos.list),
        'trending_topics': trending_topics
    }
    # return render(request, 'git/trendingbackup.html', context)
    return render(request, 'git/trending.html', context)

def userDetail(request, slug):

    user = gitUser.objects.all().filter(slug=slug).first()
    repos = user.repositories.all()
    top_topics = Topic.objects.all().order_by('?')[0:10]
    
    context = {
         'top_topics' : top_topics,
        'user': user,
        'repos': repos
    }
    return render(request, 'git/user.html', context)

def searchRepoInUser(request, slug):
    user = gitUser.objects.all().filter(slug=slug).first()
    top_topics = Topic.objects.all().order_by('?')[0:10]

    if request.method == "GET":
        searched_repo = request.GET['searched_repo']
        repos = user.repositories.all().filter(Q(name__contains = searched_repo)| Q(all_languages__contains = searched_repo))
    else:
        repos = user.repositories.all()
        searched_repo = None
    context = {
         'top_topics' : top_topics,
        'user': user,
        'repos': repos,
        'searched_repo': searched_repo
    }
    return render(request, 'git/user.html', context)



def repoDetail(request, userSlug, rName, pk):
    top_topics = Topic.objects.all().order_by('?')[0:10]

    user = gitUser.objects.all().filter(slug= userSlug).first()
    repo = user.repositories.all().filter(pk = pk).first()
    total_count = 0
    try:
        for x in repo.all_languages:
            total_count += repo.all_languages[x]
    except TypeError:
        total_count = 100
    context = {
         'top_topics' : top_topics,
        'user': user,
        'repo': repo,
        'total_count': total_count
    }
    return render(request, 'git/repo.html', context)