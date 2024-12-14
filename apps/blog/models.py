from apps.common.models.base import *

# Blog model
class Blog(BaseModel):

    blog_title = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    blog_description = models.TextField(**COMMON_NULLABLE_FIELD_CONFIG)

    def __str__(self) -> str:
        return self.blog_title
    