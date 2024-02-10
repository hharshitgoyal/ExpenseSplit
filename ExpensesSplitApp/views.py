from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User, Expense
from .serializers import UserSerializer, ExpenseSerializer

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        expense_type = serializer.validated_data['expense_type']
        if expense_type == Expense.EXACT:
            amount = serializer.validated_data['amount']
            split_values = serializer.validated_data['split_values']
            total_split_amount = sum(split_values.values())
            if total_split_amount != amount:
                return Response({"error": "Total split amount does not match expense amount"}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        
        self.update_balances(serializer.instance)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update_balances(self, expense):
        payer = expense.payer
        participants = expense.participants.all()
        amount = expense.amount
        expense_type = expense.expense_type
        split_values = expense.split_values
        
        if expense_type == Expense.EQUAL:
            split_amount = amount / len(participants)
            for participant in participants:
                if participant != payer:
                    participant.balance += split_amount
                    participant.save()
                else:
                    participant.balance -= amount
                    participant.save()
        elif expense_type == Expense.EXACT:
            for participant, share in split_values.items():
                participant_obj = User.objects.get(id=participant)
                participant_obj.balance += share
                participant_obj.save()
        elif expense_type == Expense.PERCENT:
            total_percent = sum(split_values.values())
            for participant, percent in split_values.items():
                participant_obj = User.objects.get(id=participant)
                share = (amount * percent) / total_percent
                participant_obj.balance += share
                participant_obj.save()
