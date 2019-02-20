import enum


class UserTabStatus(enum.Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    DECLINED = 'declined'

    @classmethod
    def get_status_enum(cls, status_name):
        if status_name == 'APPROVED':
            return UserTabStatus.APPROVED
        elif status_name == 'DECLINED':
            return UserTabStatus.DECLINED
        else:
            return UserTabStatus.PENDING


class TabTransactionStatus(enum.Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    DECLINED = 'declined'
