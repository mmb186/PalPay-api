from app.models.User import User
from app.models.Tabs.Tab import Tab
from app.models.Tabs.UserTabTransactionStatus import UserTabTransactionStatus
from app.models.Tabs.TabTransaction import TransactionType
from app.models.Tabs.UserTabStatus import TabUserStatus
from app.models.Tabs.enums import UserTabStatus, TabTransactionStatus


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
    user_tab_statuses = TabUserStatus.get_all_users_tab_status(tab_status.tab_id)
    for user_tab_status in user_tab_statuses:
        if not (user_tab_status.status == UserTabStatus.APPROVED):
            all_approved = False
            break
    return all_approved


def get_transaction_type_enum(transaction_type):

    if transaction_type == 'WITHDRAW':
        return TransactionType.WITHDRAW
    elif transaction_type == 'DEPOSIT':
        return TransactionType.DEPOSIT
    else:
        return None


def has_all_approved_transaction(tab_transaction):
    all_approved = True
    users_tab_transaction_statuses = UserTabTransactionStatus.\
        get_transaction_by_tab_transaction_id(tab_transaction.id)
    for user_tab_transaction_status in users_tab_transaction_statuses:
        if not (user_tab_transaction_status.status == TabTransactionStatus.APPROVED):
            all_approved = False
            break
    return all_approved


def updated_user_tab_status(tab_transaction):
    transaction_amount = tab_transaction.amount
    if not tab_transaction.transaction_type == TransactionType.WITHDRAW:
        transaction_amount = transaction_amount * (-1)
    users_tab_status = TabUserStatus.get_all_users_tab_status(tab_transaction.tab_id)
    for user_tab_status in users_tab_status:
        if user_tab_status.user_id == tab_transaction.created_by_id:
            user_tab_status.balance = user_tab_status.balance - transaction_amount
        else:
            user_tab_status.balance = user_tab_status.balance + transaction_amount
        user_tab_status.save()
    return True


def get_user_tab_summaries(current_user_id):
    tabs_query_results = TabUserStatus.get_all_user_tabs(current_user_id)

    tab_summary = dict()
    tab_summary['balance'] = 0
    tab_summary['tabs'] = []
    for tabs_query_result in tabs_query_results:
        tab, user_tab = tabs_query_result
        tab_info = {
            'name': tab.name,
            'tab_status': tab.status.name,
            'tab_id': tab.id,
            'user_tab_status': user_tab.status.name,
            'balance': user_tab.balance
        }
        tab_summary['balance'] = tab_summary['balance'] + tab_info['balance']
        tab_summary['tabs'].append(tab_info)
    return tab_summary


def generate_tab_details(current_user, tab_id):
    tab_transactions = UserTabTransactionStatus.get_user_transaction_data(current_user.id, tab_id)
    tab = Tab.get_by_id(tab_id)
    transaction_summary = dict()
    transaction_summary['tab_name'] = tab.name
    transaction_summary['balance'] = TabUserStatus.get_user_tab_status(tab_id, current_user.id).balance
    transaction_summary['transactions'] = []
    for t in tab_transactions:
        tab_transaction, user_transaction_status = t
        transaction_data = {
            'amount': tab_transaction.amount,
            'username': User.get_by_id(tab_transaction.created_by_id).username,
            'transaction_type': tab_transaction.transaction_type.name,
            'transaction_status': tab_transaction.status.name,
            'creation_time': tab_transaction.creation_time.strftime("%d-%m-%Y"),
            'tab_transaction_id': user_transaction_status.id,
            'user_transaction_status': user_transaction_status.status.name
        }
        transaction_summary['transactions'].append(transaction_data)
    return transaction_summary


