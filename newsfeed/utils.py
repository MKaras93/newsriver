from .models import Article, Tag
from django.core.exceptions import ValidationError

def regular_refresh():
    max_tags_per_refresh = 1
    prior_tag_set = Tag.objects.filter(priority=True, active=True).order_by('-refreshedAt')[:max_tags_per_refresh]
    tag_slots_left = max_tags_per_refresh - prior_tag_set.count()

    for tag in prior_tag_set:
        tag.refresh_articles()

    if tag_slots_left > 0:
        reg_tag_set = Tag.objects.filter(active=True).order_by('-refreshedAt')[:tag_slots_left]
        for tag in reg_tag_set:
            tag.refresh_articles()
