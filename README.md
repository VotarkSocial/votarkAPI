# votarkAPI
django rest API for votark social network for voting!

HELLO EVERYONE IN THE README YOU WILL FIND TWO THINGS:
#### 1.How to run?
#### 2.Documentation

## 1.How to Run:

1. Clone this repository
2. Create a virtual enviroment for python
3. Initialize the virtual enviroment
4. Install requirements.txt through pip method
5. Create a Database named votark in postgres with this credentials:

    'NAME': 'votark',
    'USER': 'admin',
    'PASSWORD': 'admin',
    'HOST': 'localhost',
    'PORT': '5432',

or change the lines 99-108 in the file votarkAPI/settings.py 

6.  run python3 manage.py makemigrations
7.  run python3 manage.py migrate
8.  run  python3 manage.py run server


## 2. Documentation:

Following the valid api routes are listed:

chat: 

    picture = models.ImageField(null=False, blank=False)
    name = models.CharField(max_length=200)
    date = models.DateField(default=now)

    api/v1/chat                      'post'
    api/v1/chat/id                   'delete','patch','get'
    api/v1/chat/id/add_admin         'post'                             username is required
    api/v1/chat/id/add               'post'                             username is required
    api/v1/chat/id/messages          'get'

comment


    content = models.CharField(max_length=1000)
    date = models.DateField(default=now)
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    post = models.ForeignKey(
        'post.Post',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    versus = models.ForeignKey(
        'versus.Versus',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )

    api/v1/comment                  'get','post'
    api/v1/comment/id               'delete','patch','get'

Devices:

    ALL URL FROM PUSH NOTIFICATIONS FCM

Follow: 

    date = models.DateField(default=now)
    onVersus = models.ForeignKey(
        'versus.Versus',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        related_name='userfollows',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    follower = models.ForeignKey(
        'votarkUser.VotarkUser',
        related_name='follower',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )

    api/v1/follow                       'get','post'
    api/v1/follow/id                    'delete','get' 


Hashtag:

    content = models.CharField(max_length=100,null=False, blank=False)
    topic = models.ForeignKey(
        'topic.Topic',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )

    api/v1/hashtag                       'get','post'
    api/v1/hashtag/id                    'delete','get'

Like:

    reaction = models.IntegerField()
    date = models.DateField(default=now)
    versus = models.ForeignKey(
        'versus.Versus',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )

    api/v1/like                          'get','post'
    api/v1/like/id                       'delete','get'

message:

    content = models.CharField(max_length=1000,null=False, blank=False)
    date = models.DateField(default=now)
    chat = models.ForeignKey(
        'chat.Chat',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )

    api/v1/message                          'post'
    api/v1/message/id                       'patch','delete','get'

post:

    image = models.ImageField(null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, verbose_name="")
    description = models.CharField(max_length=500)
    victories = models.IntegerField()
    date = models.DateField(default=now)
    order = models.IntegerField()
    topic = models.ForeignKey(
        'topic.Topic',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )

    api/v1/post                          'post','get'
    api/v1/post/id                       'patch','delete','get'

report: 

    content = models.ImageField(max_length=1000,null=False, blank=False)
    date = models.DateField(default=now)
    type = models.CharField(max_length=1000)
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )

    api/v1/report                          'post','get'
    api/v1/report/id                       'delete','get'

Share:

    date = models.DateField(default=now)
    versus = models.ForeignKey(
        'versus.Versus',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    post = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )

    api/v1/share                          'get','post'
    api/v1/share/id                       'get'

story: 

    image = models.ImageField(null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, verbose_name="")
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    date = models.DateField(default=now)

    api/v1/story                          'get','post'
    api/v1/story/id                       'get','delete'
    api/v1/story/id/views                 'get'

Topic:

    name = models.CharField(max_length=100,null=False, blank=False)
    privacity = models.BooleanField(default=False)
    creator = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )

    api/v1/topic                          'get','post'
    api/v1/topic/id                       'get','delete','patch'
    api/v1/topic/id/trending              'get'
    api/v1/topic/id/order                 'get'
    api/v1/topic/id/hashtags              'get'

Versus:

    unique_together = (('post1', 'post2'))
    date = models.DateField(default=now)
    post1 = models.ForeignKey(
        'post.Post',
        related_name='post1',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    post2 = models.ForeignKey(
        'post.Post',
        related_name='post2',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )

    api/v1/versus                          'get'
    api/v1/versus/id                       'get'
    api/v1/versus/id/comments              'get'
    api/v1/versus/id/likes                 'get'
    api/v1/versus/id/shares                'get'
    api/v1/versus/pick                     'post'           postid required


ViewedStory:

    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    story = models.ForeignKey(
        'story.Story',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )

    api/v1/viewed_story                          'post'

User: 

    'first_name',
    'last_name',
    'username',
    'password',
    'email',
    'bio',
    'birth_date',
    'location',
    'picture' 

    api/v1/user                             'get','post'
    api/v1/user/id                          'get','delete','patch'
    api/v1/user/id/followers                'get'
    api/v1/user/id/following                'get'
    api/v1/user/id/chats                    'get'
    api/v1/user/id/search_history_hashtag   'get'
    api/v1/user/id/search_history_user      'get'
    api/v1/user/id/stories                  'get'
    api/v1/user/id/mystories                'get'
    api/v1/user/id/posts                    'get'
    api/v1/user/id/pick                     'get'
    api/v1/user/id/search_user              'post'                        query is required
    api/v1/user/id/search_hashtag           'post'                        query is required
    api/v1/user/restore                     'post'                        email required


vote:

    unique_together = (('user', 'versus'))
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    versus = models.ForeignKey(
        'versus.Versus',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    date = models.DateField(default=now)
    winner = models.BooleanField(null=False,blank=False)    #True for Post1 - False for Post2


    api/v1/user                             'get','post'
    api/v1/user/id                          'get'
