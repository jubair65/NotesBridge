def update_tier(profile):
    k = profile.karma
    if k >= 1000:
        profile.tier = 'Legend'
    elif k >= 500:
        profile.tier = 'Expert'
    elif k >= 200:
        profile.tier = 'Regular'
    elif k >= 50:
        profile.tier = 'Contributor'
    else:
        profile.tier = 'Newcomer'

    profile.save()

def update_karma(profile):
    profile.karma = (
            profile.total_upvotes * 1 +
            profile.total_uploads * 5 -
            profile.total_downvotes * 0.5 -
            profile.moderation_penalty
    )
    update_tier(profile)
    profile.save()
