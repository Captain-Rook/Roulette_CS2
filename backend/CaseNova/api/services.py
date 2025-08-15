from random import choices
from rest_framework.exceptions import ValidationError
from cases.models import SkinTransaction

from core import constants

# def upgrade_skin():
    

class CaseService:
    @staticmethod
    def open_case(case, user):
        CaseService._validate_balance(user, case)
        CaseService._change_balance(case, user)
        skins = case.skins.all()
        # sum_of_skin_prices = sum([skin.price for skin in skins])
        weights = [1 / skin.price for skin in skins]
        sum_weights = sum(weights)
        normalized_weights = [w / sum_weights for w in weights]
        random_skin = choices(skins, normalized_weights)[0]
        CaseService._add_open_case_transaction(random_skin, case, user)
        print(normalized_weights)
        return random_skin

    @staticmethod
    def _validate_balance(user, case):
        if user.balance < case.price:
            raise ValidationError('Недостаточно средств.')

    @staticmethod
    def _change_balance(case, user):
        user.balance -= case.price
        user.save()
    
    @staticmethod
    def _add_open_case_transaction(skin, case, user):
        try:
            SkinTransaction.objects.create(
                user=user,
                skin=skin,
                details={
                    'from_case': case.id,
                }
            )
        except:
            raise ValueError(skin)


class TransactionService:
    @staticmethod
    def sell_item(user, transaction):
        TransactionService._check_status(transaction)
        TransactionService._change_balance(user, transaction)
        transaction.status = constants.STATUS_SALED
        transaction.action = constants.ACTION_SALED
        transaction.save()
        return transaction

    @staticmethod
    def _change_balance(user, transaction):
        user.balance += transaction.skin.price
        user.save()
    
    @staticmethod
    def _check_status(transaction):
        if transaction.status != constants.STATUS_IN_INVENTORY:
            raise ValidationError('Невозможно продать предмет.')