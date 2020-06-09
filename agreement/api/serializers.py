from rest_framework import serializers
from agreement.models import Buyer,Item,Agreement

class AgreementSerializer(serializers.ModelSerializer):
    id =serializers.IntegerField(required=False)
    class Meta:
        model = Agreement
        fields=['id','item','buyer','date_created','buyer_signature','witness_one_name','witness_one_signature','witness_one_id_number','witness_one_phone_number','witness_one_email','witness_two_name','witness_two_signature','witness_two_id_number','witness_two_phone_number','witness_two_email']
        read_only_fields=('item','buyer','buyer_signature','witness_one_signature','witness_two_signature','date_created')

class ItemSerializer(serializers.ModelSerializer):
    id =serializers.IntegerField(required=False)
    agreement=AgreementSerializer(many=False)
    class Meta:
        model = Item
        fields=['id','make','model','colour','year','reg_number','engine_number','chassis_number','odometer_reading','regitered_car_owner','price','agreement']
    
    

class BuyerSerializer(serializers.ModelSerializer):
    items=ItemSerializer(many=True)
    created_user=serializers.CharField(required=False)
    class Meta:
        model = Buyer
        fields = ['id', 'first_name', 'id_number', 'occupation', 'phone_number', 'email','kra_pin','profile','items','kin_name','kin_phone_number','created_date','created_user']
    
    def create(self,validated_data):        
        items=validated_data.pop('items')
        agreement=items[0].pop('agreement')
        
        
        if(len(items)<1):
            raise serializers.ValidationError({
                'items': 'This field is required. with fields'
            })
        # if(len(agreement)<1):
        #     raise serializers.ValidationError({
        #         'agreement': 'This field is required. with fields'
        #     })
        buyer=Buyer.objects.create(**validated_data)
        item=Item.objects.create(**items[0],buyer=buyer)
        agreement=Agreement.objects.create(**agreement,item=item,buyer=buyer)
        
        return buyer
    

