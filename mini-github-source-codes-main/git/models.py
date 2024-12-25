from operator import mod
from django.db.models.deletion import CASCADE
from django.db import models
from django.forms import SlugField
from jsonfield import JSONField
from django.template.defaultfilters import slugify

class gitUser(models.Model):
    login = models.CharField(max_length=5000, null=True)
    slug = models.SlugField(unique=True)
    g_id = models.PositiveIntegerField(null=True, blank=True)
    node_id = models.CharField(max_length=5000, null=True)
    avatar_url = models.URLField(null=True, blank=True)
    html_url = models.URLField(null=True, blank=True)
    followers_url = models.URLField(null=True, blank=True)
    following_url = models.URLField(null=True, blank=True)
    repos_url = models.URLField(null=True, blank=True)
    type = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=2000, null=True, blank=True)
    company = models.CharField(max_length=2000, null=True, blank=True)
    blog = models.URLField(null=True, blank=True)
    location = models.CharField(max_length=2000, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    hireable = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(max_length= 20000, null=True, blank=True)
    twitter_username = models.CharField(max_length=2000, null=True, blank=True)
    public_repos = models.PositiveIntegerField(null=True, blank=True)
    followers = models.PositiveIntegerField(null=True, blank=True)
    following = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    has_details = models.BooleanField(null=True, default=False)

    def __str__(self):
        return f'{self.login}-{self.g_id}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.login)
        super(gitUser, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']

    @property
    def git_stats_url(self):
        return f'https://github-readme-stats.vercel.app/api?username={self.login}&show_icons=true'
        
    @property
    def most_used_languages_url(self):
        return f'https://github-readme-stats.vercel.app/api/top-langs/?username={self.login}&layout=compact'

class Topic(models.Model):
    topic = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=1000, null=True)
    url = models.URLField(null=True)
    img_url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.topic

    def save(self, *args, **kwargs):
        self.slug = slugify(self.topic)
        super(Topic, self).save(*args, **kwargs)


class Repo(models.Model):
    g_id = models.PositiveIntegerField(null=True)
    name = models.CharField(max_length=5000, null=True)
    # slug = models.SlugField(max_length=1000, null = True)
    owner = models.ForeignKey(gitUser ,related_name='repositories',on_delete= CASCADE)
    html_url = models.URLField(null=True)
    description = models.TextField(null=True,blank=True)
    languages_url = models.URLField(null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    size = models.PositiveIntegerField(null=True)
    stargazers_count = models.PositiveIntegerField(null=True)
    watchers_count = models.PositiveIntegerField(null=True)
    forks_count = models.PositiveIntegerField(null=True)
    language = models.CharField(max_length=5000, null=True)
    all_languages = JSONField(null = True)
    read_me = models.TextField(blank=True, null=True, default=None)

    topics = models.ManyToManyField(Topic, related_name='repos_in_topic')

    fork = models.BooleanField(default=False, null=True)
    url = models.URLField(max_length=1000)
    forked_from = models.ManyToManyField(gitUser, related_name='forked_repos')
    contributors = models.ManyToManyField(gitUser, related_name='contributed_repos')
    stargazers = models.ManyToManyField(gitUser, related_name='stargazed_repos')
    watchers = models.ManyToManyField(gitUser, related_name='repos_watched')
    forkers = models.ManyToManyField(gitUser, related_name='repos_forked')

    def __str__(self):
        return self.name

    @property
    def slug(self):
        return slugify(self.name)

class GitToken(models.Model):
    token = models.CharField(max_length=1000, help_text="Paste token here")
    account = models.CharField(max_length=1000, help_text="Just for identification if needed", null= True, blank=True)

    def __str__(self):
        if self.account:
            return f"{self.account}'s Token"
        return self.token

class TrendingRepo(models.Model):
    list = models.TextField(null=True)
    pop_topics_list = models.TextField(null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Repos-id{self.id}"



    # login = models.CharField(max_length=5000)
    # g_id = models.PositiveIntegerField()
    # node_id = models.CharField(max_length=5000)
    # avatar_url = models.URLField()
    # gravatar_id = models.CharField(null=True, blank=True)
    # url = models.URLField()
    # html_url = models.URLField()
    # followers_url = models.URLField()
    # following_url = models.URLField()
    # gists_url = models.URLField()
    # starred_url = models.URLField()
    # subscriptions_url = models.URLField()
    # organizations_url = models.URLField()
    # repos_url = models.URLField()
    # events_url = models.URLField()
    # received_events_url = models.URLField()
    # type = models.CharField(max_length=30)
    # site_admin = models.BooleanField(default=False)
    # name = models.CharField(max_length=2000)
    # company = models.CharField(max_length=2000, null=True, blank=True)
    # blog = models.URLField(null=True, blank=True)
    # location = models.CharField(max_length=2000, null=True, blank=True)
    # email = models.EmailField()
    # hireable = models.CharField(max_length=200, null=True, blank=True)
    # bio = models.TextField(max_length= 20000, null=True, blank=True)
    # twitter_username = models.CharField(max_length=2000, null=True, blank=True)
    # public_repos = models.PositiveIntegerField()
    # public_gists = models.PositiveIntegerField()
    # followers = models.PositiveIntegerField()
    # following = models.PositiveIntegerField()
    # created_at = models.DateTimeField()
    # updated_at = models.DateTimeField()