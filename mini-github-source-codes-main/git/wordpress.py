# import
import os
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import media
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo


def upload_image(in_image_file_name, out_image_file_name):
    if os.path.exists(in_image_file_name):
        with open(in_image_file_name, 'rb') as f:
            binary = f.read()

        data = {
            "name": out_image_file_name,
            "type": 'image/png',
            "overwrite": True,
            "bits": binary
        }

        media_id = wp.call(media.UploadFile(data))['id']
        print(in_image_file_name.split('/')
              [-1], 'Upload Success : id=%s' % media_id)
        return media_id
    else:
        print(in_image_file_name.split('/')[-1], 'NO IMAGE!!')


# Set URL, ID, Password
WORDPRESS_ID = "YourID"
WORDPRESS_PW = "YourPassword"
WORDPRESS_URL = "YourURL/xmlrpc.php"
wp = Client(WORDPRESS_URL, WORDPRESS_ID, WORDPRESS_PW)

# Picture file name & Upload
imgPath = "picture.png "
media_id = upload_image(imgPath, imgPath)

# Blog Title
title = "Article title"

# Blog Content (html)
body = """

<p>Body Body Body Body Body Body Body Body Body Body Body Body Body Body Body Body</p>

<h2>Heading</h2>

<figure class="wp-block-image alignwide size-large">
<img src="YourURL/wp-content/uploads/year/month/%s" alt="" class="wp-image-%s"/>
</figure>

""" %(imgPath, media_id)

# publish or draft
status = "draft"

#Category keyword
cat1 = 'category1'
cat2 = 'category2'
cat3 = 'category3'

#Tag keyword
tag1 = 'tag1'
tag2 = 'tag2'
tag3 = 'tag3'

slug = "slug"

# Post
post = WordPressPost()
post.title = title
post.content = body
post.post_status = status
post.terms_names = {
    "category": [cat1, cat2, cat3],
    "post_tag": [tag1, tag2, tag3],
}
post.slug = slug

# Set eye-catch image
post.thumbnail = media_id

# Post Time
post.date = datetime.datetime.now() - datetime.timedelta(hours=9)

wp.call(NewPost(post))