"""View module for handling requests about customers"""
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ItsAlive.models import Customer


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Customers

    Arguments:
        serializers
    """
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id'
        )
        fields = ('id', 'url', 'phone_number', 'address', 'user', 'user_id')
        depth = 1


class Customers(ViewSet):
    """
    Customers for Its Alive API
    """

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Attraction instance
        """
        new_customer = Customer()
        new_customer.phone_number = request.data["phone_number"]
        new_customer.address = request.data["address"]
        new_customer.user_id = request.data["user_id"]

        new_customer.save()

        serializer = CustomerSerializer(new_customer, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a customer
        Returns:
            Response -- JSON serialized customer instance
        """
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to customers resource

        Returns:
            Response -- JSON serialized list of customers
        """
        customers = Customer.objects.all()

        # Support filtering Products by user id
        user_id = self.request.query_params.get('customer', None)
        if user_id is not None:
            customers = customers.filter(user__id=user_id)

        serializer = CustomerSerializer(
            customers, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def currentCustomer(self, request):

        try:
            customer = Customer.objects.get(user=request.auth.user)
        except Customer.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer, context={'request': request})
        return Response(serializer.data)