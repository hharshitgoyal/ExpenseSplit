from rest_framework import serializers
from .models import User, Expense


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'mobile_number']

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'payer', 'description', 'amount', 'expense_type', 'participants', 'split_values', 'created_at']
