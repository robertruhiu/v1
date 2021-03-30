from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import (
    SearchQuery, SearchRank, SearchVector, TrigramSimilarity,
)
from django.db import models

profile_vectors = (
    SearchVector('language', weight='A', config='english')
    + SearchVector('framework', weight='A', config='english')
    + SearchVector('skills', weight='A', config='english')
    + SearchVector('verified_skills', weight='B', config='english')
    + SearchVector(StringAgg('user__first_name', delimiter=' '), weight='A', config='english')
    + SearchVector(StringAgg('user__last_name', delimiter=' '), weight='A', config='english')
    + SearchVector(StringAgg('user__email', delimiter=' '), weight='B', config='english')

)

job_vectors = (SearchVector('company', 'title', 'job_role', 'tech_stack', 'city'))

class ProfileManager(models.Manager):

    def search(self, search_text):
        search_vectors = profile_vectors
        search_query = SearchQuery(
            search_text, config='english'
        )
        # search_rank = SearchRank(search_vectors, search_query)
        # trigram_similarity = TrigramSimilarity('skills', search_text)
        qs = ( self.get_queryset().annotate(search=search_vectors).filter(search=search_query)
            # self.get_queryset()
            #     .filter(search_vector=search_query)
            #     # .annotate(trigram_similarity)
            #     # .order_by('-rank')
            )
        return qs

class JobManager(models.Manager):
    use_for_related_fields = True

    def search(self, search_text):
        search_vectors = job_vectors
        search_query = SearchQuery(
            search_text, config='english'
        )
        # search_rank = SearchRank(search_vectors, search_query)
        # trigram_similarity = TrigramSimilarity('skills', search_text)
        qs = ( self.get_queryset().annotate(search=search_vectors).filter(search=search_query)
            # self.get_queryset()
            #     .filter(search_vector=search_query)
            #     # .annotate(trigram_similarity)
            #     # .order_by('-rank')
            )
        return qs