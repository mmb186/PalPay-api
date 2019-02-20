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