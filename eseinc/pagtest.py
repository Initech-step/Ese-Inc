
from eseweb.models import Posts

posts  = Posts.query.paginate(per_page=3, page=3)
for post in posts.items:
    print(post)

print('total', posts.total)
# for post in posts:
#     print(post)