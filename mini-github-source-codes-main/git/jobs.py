from apscheduler.schedulers.background import BackgroundScheduler
from django.db.models import Q
import tzlocal
import time
from .models import gitUser, Repo, GitToken, TrendingRepo, Topic
from django.template.defaultfilters import slugify
import requests
from bs4 import BeautifulSoup
from .models import gitUser
from bs4 import BeautifulSoup
import json

def addTokens():
    if GitToken.objects.all().count() == 0:
        newToken = GitToken(token = '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', account = 'MS65553')
        newToken.save()
        newToken = GitToken(token = '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', account = 'Kashyap')
        newToken.save()
        newToken = GitToken(token = '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', account = 'Shakthi-2406')
        newToken.save()

addTokens()

tokens = []
for TokenItem in GitToken.objects.all():
    tokens.append(TokenItem.token)

def start():
    if GitToken.objects.all().count() == 0:
        addTokens()

    if Topic.objects.all().count() == 0:
        get_topic_details()
    
    if TrendingRepo.objects.all().count() == 0:
        abc = TrendingRepo(pop_topics_list='[{"topic": "react\n\n", "url": "https://github.com/topics/react"}, {"topic": "css\n\n", "url": "https://github.com/topics/css"}, {"topic": "kotlin\n\n", "url": "https://github.com/topics/kotlin"}, {"topic": "config\n\n", "url": "https://github.com/topics/config"}, {"topic": "python\n\n", "url": "https://github.com/topics/python"}, {"topic": "c\n\n", "url": "https://github.com/topics/c"}, {"topic": "html\n\n", "url": "https://github.com/topics/html"}, {"topic": "app\n\n", "url": "https://github.com/topics/app"}, {"topic": "python3\n\n", "url": "https://github.com/topics/python3"}, {"topic": "github-config\n\n", "url": "https://github.com/topics/github-config"}]')
        abc.save()
        Trending_repo_scrapping()
        popular_topics_details()

    global scheduler
    scheduler = BackgroundScheduler(timezone=str(tzlocal.get_localzone()))

    scheduler.add_job(Trending_repo_scrapping, 'interval', hours=5, id="trending-repo")
    scheduler.add_job(popular_topics_details, 'interval', hours=5, id="popular_topics")

    for i, access_token in enumerate(tokens):
        scheduler.add_job(getData, 'interval', [access_token, i], seconds=3*(i+1), id=access_token)


    scheduler.start()


try:
    variable = 1
    while gitUser.objects.all().filter(Q(g_id = variable) & Q(has_details = True)).count() != 0:
        variable += 1
    base = variable-1
    # base = gitUser.objects.all().filter(has_details = True).order_by('-g_id').first().g_id
except AttributeError:
    base = 0
if base == None:
    base = 0

print('*****************',base,'**************')

limit = 2
token_count = len(tokens)

def getData(access_token, i):

    # PAUSING SCHEDULED JOB
    scheduler.get_job(access_token).pause()
    print(i)
    lower_limit = base + (i*limit)
    upper_limit = base + ((i+1)*limit)
    print(lower_limit)
    print(upper_limit)
    User_and_Repo(access_token, lower_limit, upper_limit, i)


def User_and_Repo(access_token, lower_limit, upper_limit, i):

    headers = {'Authorization': "token " + access_token}
    number = lower_limit

    while number < upper_limit:

        url = f'https://api.github.com/users?since={ number }'
        sourceResponse = requests.get(url, headers=headers)
        source = requests.get(url, headers=headers).json()
        if sourceResponse.status_code != 200:
            print("*****AN ERROR HAS OCCURED")
            time.sleep(5)
            source = requests.get(url, headers=headers).json()

        # SCRAPED ALL DATA CONGRATS!! 😁
        if len(source) == 0:
            print("SCRAPPED EVERYTHING!!!!!")
            return

        for datum in source:

            rate_limit = int(requests.get(
                url, headers=headers).headers['X-RateLimit-Remaining'])
            print(f'***************{i}*{rate_limit}***********')

            # DATA FOR USER
            data = requests.get(datum.get('url'), headers=headers).json()

            # RATE LIMIT LL EXCEED IN BETWEEN REPO DATA (BETTER WAIT FOR RENEWAL)
            if rate_limit < int(7 * data['public_repos']):
                print("Sleep started")
                time.sleep(3610)  # WAITING FOR ONE HOUR
                print("Sleep ended")
                data = requests.get(datum.get('url'), headers=headers).json()

            # UPDATE LIMITS
            if data.get('id') > upper_limit:
                # UPDATE LIMITS WILL DO LATER
                print(f"**{i}**NEXT ITERATION**")
                User_and_Repo(access_token, lower_limit + (limit*token_count) , upper_limit + (limit*token_count) , i)
                return

            number = data.get('id')
            userName = data.get('login')

            # UPDATING USER
            if gitUser.objects.all().filter(slug=slugify(data['login'])).count() != 0:
                if gitUser.objects.all().filter(slug=slugify(data['login'])).first().has_details != True:

                    newUser = gitUser.objects.all().filter(login=data['login']).first()

                    newUser.login=data['login']
                    newUser.g_id=data.get('id')
                    newUser.node_id=data.get('node_id')
                    newUser.avatar_url=data.get('avatar_url')
                    newUser.html_url=data.get('html_url')
                    newUser.followers_url=data.get('followers_url')
                    newUser.following_url=data.get('following_url')
                    newUser.repos_url=data.get('repos_url')
                    newUser.type=data.get('type')
                    newUser.name=data.get('name')
                    newUser.company=data.get('company')
                    newUser.blog=data.get('blog')
                    newUser.location=data.get('location')
                    newUser.email=data.get('email')
                    newUser.hireable=data.get('hireable')
                    newUser.bio=data.get('bio')
                    newUser.twitter_username=data.get('twitter_username')
                    newUser.public_repos=data.get('public_repos')
                    newUser.followers=data.get('followers')
                    newUser.following=data.get('following')
                    newUser.created_at=data.get('created_at')
                    newUser.updated_at=data.get('updated_at')
                    newUser.has_details= True

                    # SAVING USER IN DB
                    newUser.save()
                else:
                    newUser = gitUser.objects.all().filter(slug=slugify(data['login'])).first()
            else:
                # CREATING USER
                newUser = gitUser(
                    login=data['login'],
                    g_id=data.get('id'),
                    node_id=data.get('node_id'),
                    avatar_url=data.get('avatar_url'),
                    html_url=data.get('html_url'),
                    followers_url=data.get('followers_url'),
                    following_url=data.get('following_url'),
                    repos_url=data.get('repos_url'),
                    type=data.get('type'),
                    name=data.get('name'),
                    company=data.get('company'),
                    blog=data.get('blog'),
                    location=data.get('location'),
                    email=data.get('email'),
                    hireable=data.get('hireable'),
                    bio=data.get('bio'),
                    twitter_username=data.get('twitter_username'),
                    public_repos=data.get('public_repos'),
                    followers=data.get('followers'),
                    following=data.get('following'),
                    created_at=data.get('created_at'),
                    updated_at=data.get('updated_at'),
                    has_details = True
                )
                # SAVING USER IN DB
                newUser.save()

            pagination = 0

            while(True):

                pagination += 1

                # DATA FOR REPOS
                reposData = requests.get(
                    f"{datum.get('repos_url')}?page={pagination}", headers=headers).json()
                print(datum.get('repos_url'))

                if len(reposData) == 0:
                    break

                for repoData in reposData:
                    # CREATING REPO
                    repoName = repoData.get('name')
                    soup = BeautifulSoup(requests.get(f'https://raw.githubusercontent.com/{userName}/{repoName}/master/README.md', headers=headers).content, 'lxml')
                    readMe = soup.text
                    if readMe == '404: Not Found':
                        readMe = None

                    newRepo = Repo(
                        g_id=repoData.get('id'),
                        name=repoData.get('name'),
                        owner=newUser,
                        html_url=repoData.get('html_url'),
                        description=repoData.get('description'),
                        languages_url=repoData.get('languages_url'),
                        created_at=repoData.get('created_at'),
                        updated_at=repoData.get('updated_at'),
                        size=repoData.get('size'),
                        stargazers_count=repoData.get('stargazers_count'),
                        watchers_count= len(requests.get(repoData.get('subscribers_url'), headers=headers).json()),
                        forks_count=repoData.get('forks_count'),
                        language=repoData.get('language'),
                        all_languages=requests.get(repoData.get(
                            'languages_url'), headers=headers).json(),
                        fork=repoData.get('fork'),
                        url=repoData.get('url'),
                        read_me = readMe
                    )

                    # SAVING REPO IN DB
                    if Repo.objects.all().filter(g_id = repoData.get('id')).count() == 0:
                        newRepo.save()
                        newRepo.read_me = readMe
                    else:
                        newRepo = Repo.objects.all().filter(g_id = repoData.get('id')).first()

                    # FORKED FROM
                    if repoData.get('fork') == True or repoData.get('fork') == "true":
                        ffdata = requests.get(repoData.get('url'), headers=headers).json()
                        data = ffdata.get('parent').get('owner').get('login')
                        ffdata_gid = ffdata.get('parent').get('owner').get('id')
                        ffdata_au = f'https://avatars.githubusercontent.com/u/{ffdata_gid}?v=4'
                        if gitUser.objects.all().filter(login=data).count() != 0:
                            user_obj = gitUser.objects.all().filter(login=data).first()
                            newRepo.forked_from.add(user_obj)
                        else:
                            user_obj = gitUser(login=data, g_id=ffdata_gid, avatar_url=ffdata_au)
                            user_obj.save()
                            newRepo.forked_from.add(user_obj)
                        newRepo.save()
                        #print("SAVED FORKED FROM")

                    # STARGAZERS
                    if int(repoData.get('stargazers_count')) > 0:

                        datum_star = requests.get(
                            f"{repoData.get('url')}/stargazers?per_page=100", headers=headers).json()
                        for b in datum_star:
                            try:
                                # print(b)
                                data = b.get('login')
                                strdata_gid = b.get('id')
                                strdata_au = f'https://avatars.githubusercontent.com/u/{strdata_gid}?v=4'
                                if gitUser.objects.all().filter(login=data).count() != 0:
                                    user_obj = gitUser.objects.all().filter(login=data).first()
                                    newRepo.stargazers.add(user_obj)
                                else:
                                    user_obj = gitUser(login=data, g_id=strdata_gid, avatar_url=strdata_au)
                                    user_obj.save()
                                    newRepo.stargazers.add(user_obj)
                                newRepo.save()
                            except AttributeError:
                                pass
                        #print("SAVED STARGAZERS")

                    # WATCHERS
                    if len(requests.get(repoData.get('subscribers_url'), headers=headers).json()) > 0:

                        datum_watchers = requests.get(
                            f"{repoData.get('url')}/subscribers?per_page=100", headers=headers).json()
                        for b in datum_watchers:
                            data = b.get('login')
                            wtdata_gid = b.get('id')
                            wtdata_au = f'https://avatars.githubusercontent.com/u/{wtdata_gid}?v=4'
                            if gitUser.objects.all().filter(login=data).count() != 0:
                                user_obj = gitUser.objects.all().filter(login=data).first()
                                newRepo.watchers.add(user_obj)
                            else:
                                user_obj = gitUser(login=data, g_id=wtdata_gid, avatar_url=wtdata_au)
                                user_obj = gitUser(login=data)
                                user_obj.save()
                                newRepo.watchers.add(user_obj)
                            newRepo.save()
                        #print("SAVED WATCHERS")
                        

                    # CONTRIBUTORS
                    try:
                        datxx = requests.get(f"{repoData.get('url')}/contributors?per_page=100", headers=headers).json()
                        if len(datxx) > 0:
                            for b in datxx:
                                user = b.get('login')
                                condata_gid = b.get('id')
                                condata_au = f'https://avatars.githubusercontent.com/u/{condata_gid}?v=4'
                                if gitUser.objects.all().filter(login=user).count() != 0:
                                    user_obj = gitUser.objects.all().filter(login=user).first()
                                    newRepo.contributors.add(user_obj)
                                else:
                                    user_obj = gitUser(login=user, g_id=condata_gid, avatar_url=condata_au)
                                    user_obj.save()
                                    newRepo.contributors.add(user_obj)
                                newRepo.save()
                    except:
                        pass


                    # FORKERS
                    if int(repoData.get('forks_count')) > 0:

                        datum_forkers = requests.get(
                            f"{repoData.get('url')}/forks?per_page=100", headers=headers).json()
                        for b in datum_forkers:
                            data = b.get('owner').get('login')
                            frkdata_gid = b.get('owner').get('id')
                            frkdata_au = f'https://avatars.githubusercontent.com/u/{frkdata_gid}?v=4'
                            if gitUser.objects.all().filter(login=data).count() != 0:
                                user_obj = gitUser.objects.all().filter(login=data).first()
                                newRepo.forkers.add(user_obj)
                            else:
                                user_obj = gitUser(login=data, g_id=frkdata_gid, avatar_url=frkdata_au)
                                user_obj.save()
                                newRepo.forkers.add(user_obj)
                            newRepo.save()

                    # TOPICS
                    topics = repoData.get('topics')
                    for topic in topics:
                        if Topic.objects.all().filter(topic=topic).count() != 0:
                            topic_obj = Topic.objects.all().filter(topic=topic).first()
                            newRepo.topics.add(topic_obj)
                        else:
                            new_topic = Topic(topic=topic)
                            new_topic.save()
                            newRepo.topics.add(new_topic)
                        newRepo.save()

                print(f"{i}-ONE REPO PAGE OVER")

            print(f"{i}-ONE USER WITH REPO OVER")
        print(f"{i}-ONE PAGE OVER")

def get_good_text(string):
    string = string.split(' ')
    string = [i for i in string if not i.isspace()]
    string = [i for i in string if i]
    return (' ').join(string)

def Trending_repo_scrapping():
    try:
        scheduler.get_job('trending-repo').pause()
    except:
        pass

    trending_repositories_details = []

    url_for_trending_repo = 'https://github.com/trending'
    response = requests.get(url_for_trending_repo, headers={
                            'User-Agent': "Mozilla/5.0"})
    response_status = response.status_code
    if response_status != 200:
        print("Error Occured")
    else:
        html_content = response.content
        dom = BeautifulSoup(html_content, 'lxml')
        all_trending_repos = dom.select("article.Box-row")

        for each_repo in all_trending_repos:
            href_link = each_repo.select("h1")[0].a.attrs['href']
            bottom_div = each_repo.select('div.color-fg-muted')[0]
            try:
                language = get_good_text(bottom_div.select('span')[
                                         0].select('span')[1].text)
            except IndexError:
                language = None
            stars_today = get_good_text(
                bottom_div.select("span.float-sm-right")[0].text)
            try:
                description = get_good_text(each_repo.select('p')[0].text)
            except IndexError:
                description = " "
            for x in bottom_div.select('span.d-inline-block'):
                y = x
            y.unwrap()
            for x in bottom_div.select('span.d-inline-block'):
                y = x

            builders_data = y
            builders = []
            for data in builders_data.select('a'):
                username = data.attrs['href'][1:]
                user_img_url = data.select('img')[0].attrs['src']

                dict = {
                    'username': username,
                    'user_img_url': user_img_url
                }
                builders.append(dict)
            total_star = get_good_text(bottom_div.select('a')[0].text)
            total_forks = get_good_text(bottom_div.select('a')[1].text)

            name = href_link[1:]

            trending_repo_dict = {
                'name': name,
                'stars_today': stars_today,
                'description': description,
                'language': language,
                'total_stars': total_star,
                'total_forks': total_forks,
                'builders': builders
            }

            trending_repositories_details.append(trending_repo_dict)

            # print(type(json.dumps(trending_repositories_details)))
            # print(type(json.decoder.JSONDecoder().decode(json.dumps(trending_repositories_details))))

        if TrendingRepo.objects.all().count() == 0:
            obj = TrendingRepo(list=json.dumps(trending_repositories_details))
        else:
            obj = TrendingRepo.objects.all().last()
            obj.list = json.dumps(trending_repositories_details)
        obj.save()
    try:
        scheduler.get_job('trending-repo').resume()
    except:
        pass

def get_topic_details():
    try:
        scheduler.get_job('topics').pause()
    except:
        pass

    start_page = 1    # 'start_page' - GitHub topics pages start from 1 & go till 6

    while start_page <= 6:

        # creating URL for the specific page
        url = f'https://github.com/topics?page={start_page}'
        r = requests.get(url)

        soup_doc = BeautifulSoup(r.text, 'lxml')

        all_divs = soup_doc.find_all(
            'div', {'class': 'py-4 border-bottom d-flex flex-justify-between'})

        for div in all_divs:
            topic_ptags = div.find(
                'p', {'class': 'f3 lh-condensed mb-0 mt-1 Link--primary'})
            topic = topic_ptags.text

            # extracting description
            descr_ptags = div.find(
                'p', {'class': 'f5 color-fg-muted mb-0 mt-1'})
            description = descr_ptags.text.strip()

            # extracting topic urls
            topic_url_tags = div.find(
                'a', {'class': 'no-underline flex-1 d-flex flex-column'})
            topic_url = 'https://github.com' + topic_url_tags['href']

            try:
                img_url_tags = div.find(
                    'a', {'class': 'no-underline flex-grow-0'}).find('img', {'class': 'rounded mr-3'})
                img_url = img_url_tags['src']
                newTopic = Topic(topic=topic,
                                 description=description,
                                 url=topic_url,
                                 img_url=img_url)

            except TypeError:
                newTopic = Topic(topic=topic,
                                 description=description,
                                 url=topic_url)
            newTopic.save()
            print("ONE TOPIC SAVED")

        start_page += 1
    try:
        scheduler.get_job('topics').resume()
    except:
        pass

def popular_topics_details():
    try:
        scheduler.get_job('popular_topics').pause()
    except:
        pass

    url = f'https://github.com/topics'  # creating URL for the specific page
    r = requests.get(url)
    final_list = []
    soup_doc = BeautifulSoup(r.text, 'lxml')
    div = soup_doc.find('div', {'class': 'col-lg-3'})
    for li in div.find_all('li', {'class': 'd-inline-block'}):

        topic = get_good_text(li.text)
        url = li.find('a')
        url = 'https://github.com' + url['href']

        dict = {'topic': topic, 'url': url}
        final_list.append(dict)
        print("ONE POPULAR TOPIC SAVED")

        if Topic.objects.all().filter(slug=slugify(topic)).count() == 0:
            obj = Topic(topic=topic)
            obj.save()

    if TrendingRepo.objects.all().count() == 0:
        obj = TrendingRepo(pop_topics_list=json.dumps(final_list))        
    else:
        obj = TrendingRepo.objects.all().last()
        obj.pop_topics_list = json.dumps(final_list)
    obj.save()

    try:
        scheduler.get_job('popular_topics').resume()
    except:
        pass
