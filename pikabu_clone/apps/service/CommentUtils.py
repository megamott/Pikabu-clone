def find_ids_of_comments(ids, qs):
    """ Find all comment ids (include nested) is QuerySet """
    for comment in qs:
        if comment.comment_children:
            ids.append(comment.id)
            find_ids_of_comments(ids, comment.comment_children.all())

    return ids
