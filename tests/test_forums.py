from dcard import Dcard


def test_forums(forums):
    all_forums = forums.get('all')
    no_school_forums = forums.get('no_school')
    assert len(all_forums) > len(no_school_forums)


def test_post_metas(forums):
    forum = forums.get('test')['alias']
    pop_metas = Dcard.forums(forum).get_metas(sort='popular')
    new_metas = Dcard.forums(forum).get_metas(sort='new')
    assert 0 <= len(pop_metas) <= 30
    assert 0 <= len(new_metas) <= 30
    assert len(pop_metas) <= len(new_metas) == 30


def test_multi_post_metas(forums):
    forum = forums.get('test')['alias']
    metas0 = Dcard.forums(forum).get_metas(pages=0)
    metas1 = Dcard.forums(forum).get_metas()
    metas = Dcard.forums(forum).get_metas(pages=3)

    assert len(metas0) == 0
    assert 0 <= len(metas1) <= 30
    assert 0 <= len(metas) <= 90


def test_multi_post_metas_with_callback(forums):

    def collect_ids(metas):
        return [meta['id'] for meta in metas]

    def with_no_return(metas):
        return None

    def simulate_store_into_db(metas):
        some_id = 987654
        return some_id

    forum = forums.get('test')['alias']

    ids = Dcard.forums(forum).get_metas(callback=collect_ids)
    none = Dcard.forums(forum).get_metas(callback=with_no_return)
    rids = Dcard.forums(forum).get_metas(callback=simulate_store_into_db)

    assert len(ids) != 0
    assert len(rids) != 0
    assert len(none) != 0
    assert none == [None] * len(none)
