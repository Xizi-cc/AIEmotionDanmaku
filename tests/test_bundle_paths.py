from app.bundle_paths import is_frozen, project_root, resource_path


def test_project_root_is_repo_in_dev():
    assert not is_frozen()
    root = project_root()
    assert (root / "main.py").is_file()
    assert (root / "web" / "static" / "index.html").is_file()


def test_resource_path_data_pool():
    pool = resource_path("data", "danmu_pool_zh.json")
    assert pool.is_file()
    assert pool.parent == project_root() / "data"


def test_feedback_page_in_index_html():
    html = (project_root() / "web" / "static" / "index.html").read_text(encoding="utf-8")
    assert 'data-page="feedback"' in html
    assert 'id="page-feedback"' in html
    assert 'id="feedbackForm"' in html
    assert 'id="feedbackContent"' in html
    assert "qrcode_" not in html
    assert "reward_qrcode" not in html


def test_announcements_page_in_index_html():
    html = (project_root() / "web" / "static" / "index.html").read_text(encoding="utf-8")
    assert 'data-page="announcements"' in html
    assert 'id="page-announcements"' in html
    assert 'id="announcementsList"' in html
    assert 'id="announcementsNavBadge"' in html
    assert 'id="overviewAnnouncementBanner"' in html
    assert 'id="btnOverviewAnnouncementDismiss"' in html
    assert "/static/supabase-client.js" in html


def test_overview_announcement_banner_in_app_js():
    js = (project_root() / "web" / "static" / "app.js").read_text(encoding="utf-8")
    assert "danmu_announcements_overview_banner_dismissed_id" in js
    assert "function buildAnnouncementSnippet" in js
    assert "function updateOverviewAnnouncementBanner" in js


def test_api_settings_visible_in_simplified_mode():
    """记忆与温度控件不得带 settings-full-only，否则简化模式下会被 CSS 隐藏。"""
    html = (project_root() / "web" / "static" / "index.html").read_text(encoding="utf-8")
    for field_id in ("memory_mode", "memory_window", "temperature"):
        idx = html.index(f'id="{field_id}"')
        chunk = html[max(0, idx - 120) : idx]
        assert "settings-full-only" not in chunk, field_id
