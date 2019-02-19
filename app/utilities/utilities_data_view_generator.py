from app.models.Tabs.UserTabStatus import TabUserStatus, UserTabStatus


def create_tab_view_dictionary(tab_model, user_tab_status):
    return {
        'tab_id': tab_model.id,
        'user_tab_status_id': user_tab_status.id,
        'tab_name': tab_model.name,
        'tab_status': tab_model.status.name,
        'tab_balance': user_tab_status.balance,
    }


def has_all_users_approved(tab_status):
    all_approved = True
    user_tab_statuses = TabUserStatus.get_all_tab_status(tab_status.tab_id)
    for user_tab_status in user_tab_statuses:
        if not (user_tab_status.status == UserTabStatus.APPROVED):
            all_approved = False
            break
    return all_approved
