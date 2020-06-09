from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions,IsAdminUser
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import *
#from rest_framework.mixins import *
from rest_framework.authentication import TokenAuthentication

from .permissions import IsAdminOrReadOnly

from agreement.models import Buyer
from agreement.api.serializers import *

#PDF
from reportlab.pdfgen import canvas
from reportlab.lib import colors

#EMAIL
from django.core.mail import EmailMessage
import os

@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated,))
def api_agreement_detail(request,slug):
     try:
         buyer_info= Buyer.objects.get(pk=slug)
     except expression as identifier:
         return Response(status=status.HTTP_404_NOT_FOUND)

     if request.method=='GET':
         serializer=AgreementSerializer(buyer_info)
         return Response(serializer.data)
     elif request.method=='PUT':
         serializer=AgreementSerializer(buyer_info,data=request.data)
         data={}
         if serializer.is_valid():
             serializer.save()
             data["success"]="update successful"
             data["status"]="success"
             return Response(data=data)
         else:
             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
     elif request.method=='DELETE':
         operation=buyer_info.delete()
         
         data={}
         if operation:
             data["success"]="delete successful"
             data["status"]="success"
         else:
             data["failure"]="delete failed"
             data["status"]="fail"
         return Response(data=data) 

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_agreement_detail(request):
    user= request.user;
    buyer_info=Buyer(created_user=user)

    if request.method=='POST':
        serializer=AgreementSerializer(buyer_info,data=request.data)
        
        if serializer.is_valid():
             serializer.save()
             data={}
             data['data']=serializer.data
             data["success"]="save successful"
             data["status"]="success"
             return Response(status=status.HTTP_201_CREATED,data=data)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

##>PDF
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def generateAgreementPDF(request,id):
    try:
        buyer= Buyer.objects.get(pk=id)
    except Exception as e:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        #print(buyer.items[0].make)
        fileName = 'Cars45_Kenya_agreements-'+str(id)+'.pdf'
        documentTitle = 'CAR SALES AGREEMENT'
        title = 'Cars45 Kenya Agreement'
        subTitle = 'The largest carnivorous marsupial'
        logo='media/logos/Webp.net-resizeimage.jpg'
        header='media/logos/header.jpg'
        footer='media/logos/footer.jpg'
        fontSize_common=12

        p = canvas.Canvas(fileName)
        # Courier
        # Courier-Bold
        # Courier-BoldOblique
        # Courier-Oblique
        # Helvetica
        # Helvetica-Bold
        # Helvetica-BoldOblique
        # Helvetica-Oblique
        # Symbol
        # Times-Bold
        # Times-BoldItalic
        # Times-Italic
        # Times-Roman
        # ZapfDingbats

        def drawMyRuler(pdf):
            pdf.drawString(100,810, 'x100')
            pdf.drawString(200,810, 'x200')
            pdf.drawString(300,810, 'x300')
            pdf.drawString(400,810, 'x400')
            pdf.drawString(500,810, 'x500')
            pdf.drawString(10,100, 'y100')
            pdf.drawString(10,200, 'y200')
            pdf.drawString(10,300, 'y300')
            pdf.drawString(10,400, 'y400')
            pdf.drawString(10,500, 'y500')
            pdf.drawString(10,600, 'y600')
            pdf.drawString(10,700, 'y700')
            pdf.drawString(10,800, 'y800')
        
        
        p.setTitle(documentTitle)
        #p.drawInlineImage()
        p.drawImage(header,10,740,width=550,height=100,preserveAspectRatio=True)
        p.drawImage(footer,20,20,width=550,height=100,preserveAspectRatio=True)
        p.setFont('Times-Bold',20)        
        p.drawCentredString(300, 730, documentTitle)
        p.setFont('Times-Bold',14) 
        p.drawAlignedString(50,700,"1. THE PARTIES TO THIS CAR SALES AGREEMENT ARE:")
        p.drawAlignedString(50,680,"1.1 THE SELLER:")

        #THE SELLER
        p.setFont('Times-Bold',13)
        p.drawString(60,660,"Gari Tech Limited T/A Cars45 Kenya")
        p.drawString(60,640,"P.O Box 52602 – 00100")
        p.drawString(60,620,"Valley Arcade, Nairobi")
        p.drawString(60,600,"Info@Cars45.co.ke")
        p.drawString(60,580,"Tel No: 0782454500")

        #THE BUYER
        p.drawAlignedString(50,540,"1.2 THE BUYER:")

        
        p.setFont('Times-Roman',13)
        p.drawString(60,520,"First Name(s):")
        p.drawString(60,500,"ID Number:")
        p.drawString(60,480,"Place of Work:")
        p.drawString(60,460,"Mobile Phone Number:")
        p.drawString(60,440,"Email Address:")
        p.drawString(60,420,"KRA Pin:")
        p.drawString(60,400,"Next of Kin:")
        p.drawString(300,400,"Tel of Next of Kin:")
        #p.line(30, 710, 550, 710)
        #DYNAMIC
        p.setFont('Times-Bold',12)
        p.drawString(150,520,buyer.first_name)
        p.drawString(150,500,str(buyer.id_number))
        p.drawString(150,480,buyer.occupation)
        p.drawString(190,460,str(buyer.phone_number))
        p.drawString(150,440,buyer.email)
        p.drawString(150,420,buyer.kra_pin)
        p.drawString(150,400,buyer.kin_name)
        p.drawString(420,400,str(buyer.kin_phone_number))

        #ITEM
        p.setFont('Times-Bold',13)
        p.drawString(60,370,"2 THE OBJECT OF SALE IS:")
        p.setFont('Times-Roman',13)
        p.drawString(60,350,"2.1 Make and Model:")
        p.drawString(60,330,"2.2 Colour:")
        p.drawString(60,310,"2.3 Year:")
        p.drawString(60,290,"2.4 Registration Number:")
        p.drawString(60,270,"2.5 Engine Number:")
        p.drawString(60,250,"2.6 Chassis Number:")
        p.drawString(60,230,"2.7 Odometer Reading:")
        p.drawString(60,210,"2.8 Registered Car Owner:")

        p.setFont('Times-Bold',12)
        p.drawString(180,350,buyer.items[0].make+' '+buyer.items[0].model)
        p.drawString(150,330,buyer.items[0].colour)
        p.drawString(150,310,str(buyer.items[0].year))
        p.drawString(200,290,buyer.items[0].reg_number)
        p.drawString(180,270,buyer.items[0].engine_number)
        p.drawString(180,250,buyer.items[0].chassis_number)
        p.drawString(185,230,buyer.items[0].odometer_reading)
        p.drawString(210,210,buyer.items[0].regitered_car_owner)
        p.showPage()
        #PAGE 2
        text3_1Lines = [
            'The Seller guarantees that they are the true and lawful owner of the above-described vehicle',
            'and that it is free of all encumbrances and any and all legal claims.',
            ]
        text4_1Lines = [
            'The Seller warrants that at the date of signature of this agreement there are no outstanding',
            'Government fees or taxes or other penalties outstanding against the registration of the vehicle',
            'sold in terms of this agreement.',
            ]
        text5_1Lines = [
            'The Seller or their agent gives no warranty or guarantee other than those specified in 3.1 and 4.1',
            'above.',
            ]
        text6_1Lines = [
            'The vehicle is sold “As –Is’’ and the seller shall not be liable for any defects, patent, latent or',
            'otherwise.',
            ]
        text6_2Lines = [
            'The Buyer admits having inspected the vehicle to his/her/its satisfaction and that no guarantees',
            'or warranties of any nature were expressed or implied by the Seller or his/her/its agent',
            'regarding its condition or quality.',
            ]
        text7_1Lines = [
            'The Buyer and Seller are legally competent to enter into this agreement.',
            ]
        text8_1Lines = [
            'The parties agree to sign all documents necessary to transfer ownership of the vehicle from the',
            'Seller onto the name of the Buyer within 1 (ONE) day of the seller receiving full payment.',
            ]
        text8_2Lines = [
            'The Buyer shall be liable for all costs relating to the registration of the vehicle into his/her name',
            'and all costs relating to the Transfer of Ownership Traffic Act (Cap 403, Section 9)',
            ]
        
        p.drawImage(header,10,740,width=550,height=100,preserveAspectRatio=True)
        p.drawImage(footer,20,20,width=550,height=100,preserveAspectRatio=True)
        p.setFont('Times-Bold',13)
        p.drawString(60,730,"3. OWNERSHIP:")
        p.setFont('Times-Roman',fontSize_common)
        p.drawString(60,700,"3.1")
        text3_1 = p.beginText(80, 700)
        text3_1.setFont("Times-Roman", fontSize_common)
        for line in text3_1Lines:
            text3_1.textLine(line)
        p.drawText(text3_1)

        p.setFont('Times-Bold',13)
        p.drawString(60,650,"4. WARRANTY:")
        p.setFont('Times-Roman',fontSize_common)
        p.drawString(60,620,"4.1")
        text4_1 = p.beginText(80, 620)
        text4_1.setFont("Times-Roman", fontSize_common)
        for line in text4_1Lines:
            text4_1.textLine(line)
        p.drawText(text4_1)

        p.setFont('Times-Bold',13)
        p.drawString(60,550,"5. NO WARRANTIES OR GUARANTEES:")
        p.setFont('Times-Roman',fontSize_common)
        p.drawString(60,520,"3.1")
        text5_1 = p.beginText(80, 520)
        text5_1.setFont("Times-Roman", fontSize_common)
        for line in text5_1Lines:
            text5_1.textLine(line)
        p.drawText(text5_1)

        p.setFont('Times-Bold',13)
        p.drawString(60,480,"6. DISCLAIMER:")
        p.setFont('Times-Roman',fontSize_common)
        p.drawString(60,450,"6.1")
        text6_1 = p.beginText(80, 450)
        text6_1.setFont("Times-Roman", fontSize_common)
        for line in text6_1Lines:
            text6_1.textLine(line)
        p.drawText(text6_1)
        p.drawString(60,400,"6.2")
        text6_2 = p.beginText(80, 400)
        text6_2.setFont("Times-Roman", fontSize_common)
        for line in text6_2Lines:
            text6_2.textLine(line)
        p.drawText(text6_2)

        p.setFont('Times-Bold',13)
        p.drawString(60,340,"7. LEGAL CAPACITY:")
        p.setFont('Times-Roman',fontSize_common)
        p.drawString(60,310,"7.1")
        text7_1 = p.beginText(80, 310)
        text7_1.setFont("Times-Roman", fontSize_common)
        for line in text7_1Lines:
            text7_1.textLine(line)
        p.drawText(text7_1)

        p.setFont('Times-Bold',13)
        p.drawString(60,280,"8. TRANSFER OF OWNERSHIP AND COSTS:")
        p.setFont('Times-Roman',fontSize_common)
        p.drawString(60,250,"8.1")
        text8_1 = p.beginText(80, 250)
        text8_1.setFont("Times-Roman", fontSize_common)
        for line in text8_1Lines:
            text8_1.textLine(line)
        p.drawText(text8_1)
        p.drawString(60,210,"8.2")
        text8_2 = p.beginText(80, 210)
        text8_2.setFont("Times-Roman", fontSize_common)
        for line in text8_2Lines:
            text8_2.textLine(line)
        p.drawText(text8_2)
        p.showPage()

        #PAGE 3
        text9_2Lines = [
            'The Purchase price is to be paid in full by bank guaranteed check or in a manner as agreed by',
            'both parties (specify)',
            ]
        text9_3Lines = [
            'Ownership of the vehicle will only pass onto the Buyer once the bank honours the cheque or',
            'other legal instrument of payment.',
            ]
        text9_4Lines = [
            'The vehicle will only be delivered to the Buyer once payment has been received in full as per 9.3',
            ]
        text9_5Lines = [
            'In the case of a down- payment: Down payment should not be less than 10% of the value of the',
            ]
        text10_1Lines = [
            'The Risk passes to the Buyer once the Buyer or his/her agent receives the keys to the car or takes',
            'possession of the vehicle.',
            ]
        text11_1Lines = [
            'The parties consent to the jurisdiction of the Kenyan Government (Kenyan Law)',
            ]
        #drawMyRuler(p)
        p.drawImage(header,10,740,width=550,height=100,preserveAspectRatio=True)
        p.drawImage(footer,20,20,width=550,height=100,preserveAspectRatio=True)
        p.setFont('Times-Bold',13)
        p.drawString(60,730,"9. PURCHASE PRICE:")
        p.setFont('Times-Roman',fontSize_common)
        p.drawString(60,700,"9.1")
        p.drawString(80,700,"The Purchase price is the sum of KSH")
        p.setFont('Times-Bold',13)
        p.drawString(300,700,str("{:,}".format(buyer.items[0].price)))
        p.setFont('Times-Roman',fontSize_common)
        p.drawString(400,700,"(Kenya Shillings)")
        p.setFont('Times-Roman',fontSize_common)
        p.drawString(60,670,"9.2")
        text9_2 = p.beginText(80, 670)
        text9_2.setFont("Times-Roman", fontSize_common)
        for line in text9_2Lines:
            text9_2.textLine(line)
        p.drawText(text9_2)        
        p.drawString(60,640,"9.3")
        text9_3 = p.beginText(80, 640)
        text9_3.setFont("Times-Roman", fontSize_common)
        for line in text9_3Lines:
            text9_3.textLine(line)
        p.drawText(text9_3)
        p.drawString(60,600,"9.4")
        text9_4 = p.beginText(80, 600)
        text9_4.setFont("Times-Roman", fontSize_common)
        for line in text9_4Lines:
            text9_4.textLine(line)
        p.drawText(text9_4)
        p.drawString(60,580,"9.5")
        text9_5 = p.beginText(80, 580)
        text9_5.setFont("Times-Roman", fontSize_common)
        for line in text9_5Lines:
            text9_5.textLine(line)
        p.drawText(text9_5)
        p.drawString(80,560,"vehicle,which in this case is Ksh")
        p.setFont('Times-Bold',13)
        p.drawString(250,560,str("{:,}".format(0.1*buyer.items[0].price)))
        p.setFont('Times-Roman',fontSize_common)
        p.drawString(350,560,"The buyer should there after complete")
        p.drawString(80,540,"the balance of Ksh")
        p.setFont('Times-Bold',13)
        p.drawString(180,540,str("{:,}".format(buyer.items[0].price-(0.1*buyer.items[0].price))))
        p.setFont('Times-Roman',fontSize_common)
        p.drawString(300,540,"by the")
        p.setFont('Times-Bold',13)
        p.drawString(350,540,"DATE")
        
        p.setFont('Times-Bold',13)
        p.drawString(60,510,"10. POSSESSION AND TRANSFER OF RISK:")
        p.setFont('Times-Roman',fontSize_common)
        p.drawString(60,480,"10.1")
        text10_1 = p.beginText(85, 480)
        text10_1.setFont("Times-Roman", fontSize_common)
        for line in text10_1Lines:
            text10_1.textLine(line)
        p.drawText(text10_1)

        p.setFont('Times-Bold',13)
        p.drawString(60,410,"11. JURISDICTION:")
        p.setFont('Times-Roman',fontSize_common)
        p.drawString(60,380,"11.1")
        text11_1 = p.beginText(85, 380)
        text11_1.setFont("Times-Roman", fontSize_common)
        for line in text11_1Lines:
            text11_1.textLine(line)
        p.drawText(text11_1)

        p.setLineWidth(0.1)
        p.setStrokeColor(colors.grey)
        p.drawString(60,350,"Signed at")
        p.line(110, 348, 350, 348)
        p.drawString(60,320,"On this")
        p.line(110, 318, 200, 318)
        p.drawString(230,320,"day of")
        p.line(270, 318, 320, 318)
        p.drawString(330,320,"20")
        p.line(350, 318, 400, 318)

        p.setFont('Times-Bold',13)
        p.drawString(60,270,"For Gari Tech Ltd T/A Cars45 Kenya")
        p.line(60, 240, 260, 240)
        p.setFont('Times-Roman',11)
        p.drawString(60,220,"STAMP")
        p.setFont('Times-Bold',13)
        p.drawString(300,270,"Buyer")
        p.line(300, 240, 500, 240)

        p.drawString(60,200,"Witness Name and Signature")
        p.setFont('Times-Roman',12)
        p.drawString(60,180,"Name:")
        p.line(130, 180, 260, 180)
        p.drawString(60,160,"Signature:")
        p.line(130, 160, 260, 160)
        p.drawString(60,140,"ID No:")
        p.line(130, 140, 260, 140)
        p.drawString(60,120,"Phone Number:")
        p.line(140, 120, 260, 120)
        p.drawString(60,100,"Email:")
        p.line(130, 100, 260, 100)

        p.setFont('Times-Bold',13)
        p.drawString(300,200,"Witness Name and Signature")
        p.setFont('Times-Roman',12)
        p.drawString(300,180,"Name:")
        p.line(370, 180, 500, 180)
        p.drawString(300,160,"Signature:")
        p.line(370, 160, 500, 160)
        p.drawString(300,140,"ID No:")
        p.line(370, 140, 500, 140)
        p.drawString(300,120,"Phone Number:")
        p.line(380, 120, 500, 120)
        p.drawString(300,100,"Email:")
        p.line(370, 100, 500, 100)
        

        p.save()
        
        data={}
        
        email = EmailMessage(
            subject='AGREEMENT',
            body=f'Hello {buyer.first_name}, Find Attached',
            from_email='info@cars45.co.ke',
            to=[buyer.email],
            cc=[request.user.email]
        )
        email.attach_file(fileName)
        try:
            email.send(fail_silently=False)
        except Exception as e:
            data["status"]="failed"
            data["message"]=str(e)
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE,data=data)
        if os.path.isfile(fileName):
           os.remove(fileName)

        
        data["success"]="pdf created successful"
        data["status"]="success"
        return Response(status=status.HTTP_200_OK,data=data)

##>>GET ONE
class AgreementRetrieveAPIView(RetrieveAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,DjangoModelPermissions)

##>>CREATE
class AgreementCreateApiView(CreateAPIView):
    
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,DjangoModelPermissions,)
    def perform_create(self, serializer):
        user=serializer.context['request'].user
        serializer.save(created_user=user)

##>>GET ALL
class AgreementListView(ListAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,DjangoModelPermissions,)
    pagination_class=PageNumberPagination

##>>UPDATE
class AgreementUpdateAPIView(UpdateAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,DjangoModelPermissions,)

##>>DELETE
class AgreementDestroyAPIView(DestroyAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,DjangoModelPermissions,)
    
 

