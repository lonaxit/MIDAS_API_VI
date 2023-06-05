from celery import shared_task

from django.contrib.auth import get_user_model
from core.models import Loan,Product,Deduction,Saving,Profile,MasterLoanDeduction,SavingMaster
from django.db import transaction
from rest_framework.exceptions import ValidationError
import math
import io, csv, pandas as pd
import json
import datetime
from core.api.utilities import *
User = get_user_model()

@shared_task(bind=True)
def fun(self):
    # operations
    print("You are in Fun function")
    return "done"

@shared_task
def mul(x, y,z):
    print( x * y * z)
    
@shared_task
def create_loan_subscription(data):
    # data = json.loads(data)
    
    # convert the JSON data to a DataFrame
    data_frame = pd.read_json(data)
    
    try:
        for row in data_frame.itertuples():
            guarantor_id1 = 0
            guarantor_id2 = 0
            
            if pd.isnull(row.guarantor_id1):
                # Do something if the cell is empty
                pass
            else:
                guarantor_id1 = row.guarantor_id1
                
            if pd.isnull(row.guarantor_id2):
                # Do something if the cell is empty
                pass
            else:
                guarantor_id2 = row.guarantor_id2
                
            loan_date_stamp=row.disbursement_date
            loan_date_timestamp_ms = int(loan_date_stamp) / 1000
            loan_date = datetime.datetime.utcfromtimestamp(loan_date_timestamp_ms)
            
            start_date_stamp=row.loan_start_date
            start_date_timestamp_ms = int(start_date_stamp) / 1000
            start_date = datetime.datetime.utcfromtimestamp(start_date_timestamp_ms)
            
            end_date_stamp=row.loan_end_date
            end_date_timestamp_ms = int(end_date_stamp) / 1000
            end_date = datetime.datetime.utcfromtimestamp(end_date_timestamp_ms)
           
            Loan.objects.create(
                loan_date=loan_date,
                start_date=start_date,
                end_date=end_date,
               
                active=row.loan_status,
                transaction_code=row.ref.replace('-', ''), 
                sub_id=row.id,
                applied_amount=row.amount_applied,
                approved_amount=row.amount_approved,
                monthly_deduction=row.monthly_deduction,
                net_pay=0.0,
                tenor=row.custom_tenor,
                created_by=User.objects.get(pk=1),
                product=Product.objects.get(pk=row.product_id),
                owner=User.objects.get(pk=row.user_id),
                guarantor_one=guarantor_id1,
                guarantor_two=guarantor_id2,
            )
                  
    except ValueError as e:
        raise ValueError(f"Invalid value: {e}")
    except TypeError as e:
        raise TypeError(f"Type error: {e}")
    
    
@shared_task
def upload_loan_deduction(data):

    # convert the JSON data to a DataFrame
    data_frame = pd.read_json(data)
    
    try:
        for row in data_frame.itertuples():
            amount_deducted = None
            amount_debited = None
            
            if pd.isnull(row.amount_deducted):
                # Do something if the cell is empty
                pass
            else:
                amount_deducted = row.amount_deducted
                
            if pd.isnull(row.amount_debited):
                # Do something if the cell is empty
                pass
            else:
                amount_debited = row.amount_debited
                
            _date_stamp=row.entry_month
            _date_timestamp_ms = int(_date_stamp) / 1000
            _date = datetime.datetime.utcfromtimestamp(_date_timestamp_ms)
            
            Deduction.objects.create(
                loanee=User.objects.get(pk=row.user_id),
                loan=Loan.objects.get(pk=1),
                credit = amount_deducted,
                debit = amount_debited,
                narration = row.notes,
                transaction_code=row.deduct_reference.replace('-', ''), 
                transaction_date=_date,
                deduction_sub_id=row.lsubscription_id,
                created_by=User.objects.get(pk=1),
            )
                  
    except ValueError as e:
        raise ValueError(f"Invalid value: {e}")
    except TypeError as e:
        raise TypeError(f"Type error: {e}")
    

# update loan deduction swith correct loan ids
@shared_task
def update_loan_deduction_loanids():
    """
    Update the 'loan' field of all deductions based on the related loan subscription ID.

    This function loops through all loans, filters deductions based on their
    subscription ID, and updates their 'loan' field to match the corresponding
    loan's ID.
    """
    loans = Loan.objects.all()
    with transaction.atomic():
        
        for loan in loans:
            deductions = Deduction.objects.filter(deduction_sub_id=loan.sub_id)
            
            if deductions.exists():

                # Use a for...else loop instead of if...else to make the code more concise
                for deduction in deductions:
                    deduction.loan = loan
                    deduction.save()
            else:
                # The else block will execute only if the loop completes without a break
                pass
    # loans = Loan.objects.all()

    # with transaction.atomic():
    #     for item in loans:
    #         deductions = Deduction.objects.filter(deduction_sub_id=item.sub_id)

    #         if deductions.exists():
    #             deductions.update(loan=item.id)
    #         else:
    #             # If there are no deductions for this loan, do nothing
    #             pass

# upload user savings    
@shared_task
def upload_user_savings(userid,data):

    # convert the JSON data to a DataFrame
    data_frame = pd.read_json(data)
    
    with transaction.atomic():
        try:
            for row in data_frame.itertuples():
                credit_amt = None
                debit_amt = None
                
                if pd.isnull(row.amount_saved):
                    # Do something if the cell is empty
                    pass
                else:
                    credit_amt = row.amount_saved
                    
                if pd.isnull(row.amount_withdrawn):
                    # Do something if the cell is empty
                    pass
                else:
                    debit_amt = row.amount_withdrawn

                _date_stamp=row.entry_date
                _date_timestamp_ms = int(_date_stamp) / 1000
                _date = datetime.datetime.utcfromtimestamp(_date_timestamp_ms)
                
                Saving.objects.create(
                    user=User.objects.get(pk=row.user_id),
                    credit = credit_amt,
                    debit = debit_amt,
                    transaction_code=row.ref_string.replace('-', ''), 
                    transaction_date=_date,
                    narration = row.notes,
                    created_by=User.objects.get(pk=userid),
                )
                    
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except TypeError as e:
            raise TypeError(f"Type error: {e}")
        

# update profile 

@shared_task
def update_profile(data):
    """
    Update the 'profile' field of all users based on the related user ID.

    This function loops through all profiles, filters prodile based on their
    user ID, and updates relevant fields.
    """
    data_frame = pd.read_json(data)
    
    # profiles = Profile.objects.all()
    with transaction.atomic():
        for  row in data_frame.itertuples():
            
            try:
                # Attempt to get the order for the user
                profile= Profile.objects.get(user_id=row.id)
               
                #update profile
                profile.staff_id = row.staff_no
                profile.home_address = row.home_add
                profile.email = row.email
                profile.employment_type = row.employ_type
                profile.gender = row.sex
                profile.job_cadre = row.job_cadre
                profile.marital_status = row.marital_status
                profile.phone = row.phone
                profile.dept = row.dept
                profile.title = row.title
                profile.member_type = row.membership_type
                profile.save()
            except Profile.DoesNotExist:
                pass
             
@shared_task
def update_nok(data):
    """
    Update the 'profile'  next of kin details.

    
    """
    data_frame = pd.read_json(data)
    
    # profiles = Profile.objects.all()
    with transaction.atomic():
        for  row in data_frame.itertuples():
            surname = row.first_name
            firstname = row.last_name
            othername = row.other_name
            
            full_name = surname + ' ' + firstname
            
            if pd.isnull(row.other_name):
                    # Do something if the cell is empty
                pass
            else:
                full_name = surname + ' ' + firstname + ' ' + othername
            
            try:
                # Attempt to get the order for the user
                profile= Profile.objects.get(user_id=row.user_id)
                #update profile
                profile.nok_fullName = full_name
                profile.nok_relationship = row.relationship
                profile.nok_phone = row.phone
                profile.save()
            except Profile.DoesNotExist:
                pass
            
@shared_task
def update_bank(data):
    """
    Update the 'profile'  next of kin details.

    
    """
    data_frame = pd.read_json(data)
    
    # profiles = Profile.objects.all()
    with transaction.atomic():
        for  row in data_frame.itertuples():
          
            
            try:
                # Attempt to get the order for the user
                profile= Profile.objects.get(user_id=row.user_id)
                #update profile
                profile.bank = row.bank_name
                profile.bank_account = row.acct_number
                profile.save()
            except Profile.DoesNotExist:
                pass
            
# migrate master deductions

@shared_task
def upload_master_loan_deduction(userid,data):

    # convert the JSON data to a DataFrame
    data_frame = pd.read_json(data)
    with transaction.atomic():
        
        try:
            for row in data_frame.itertuples():
            
                _date_stamp=row.entry_date
                _date_timestamp_ms = int(_date_stamp) / 1000
                _date = datetime.datetime.utcfromtimestamp(_date_timestamp_ms)
                
                MasterLoanDeduction.objects.create(
                    name=row.name,
                    ippis_number=row.ippis_no,
                    cumulative_amount = row.cumulative_amount,
                    narration = row.description,
                    transaction_code=row.master_reference.replace('-', ''),
                    active = row.status, 
                    entry_date=_date,
                    created_by=User.objects.get(pk=userid),
                )
                    
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except TypeError as e:
            raise TypeError(f"Type error: {e}")
        

# migrate master savings deductions

@shared_task
def upload_master_saving(userid,data):

    # convert the JSON data to a DataFrame
    data_frame = pd.read_json(data)
    with transaction.atomic():
        
        try:
            for row in data_frame.itertuples():
            
                _date_stamp=row.entry_date
                _date_timestamp_ms = int(_date_stamp) / 1000
                _date = datetime.datetime.utcfromtimestamp(_date_timestamp_ms)
                
                SavingMaster.objects.create(
                    name=row.name,
                    ippis_number=row.ippis_no,
                    amount = row.saving_cumulative,
                    narration = row.notes,
                    transaction_code=row.ref_identification.replace('-', ''),
                    active = row.status, 
                    transaction_date=_date,
                    upload_by=User.objects.get(pk=userid),
                )
                    
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except TypeError as e:
            raise TypeError(f"Type error: {e}")
        
        

# Create bulk deduction from a master deduction table
def create_bulk_loan_deduction(userid,data):
    
      # convert the JSON data to a DataFrame
    data_frame = pd.read_json(data)
    
    
    # get all active master deduction records
    masterDeductions= MasterLoanDeduction.objects.filter(active=True)
        
    # get all active loans
    activeLoans = Loan.objects.filter(active=True)
        
    allDeductions = Deduction.objects.filter(loan__active=True)
        
    if masterDeductions.exists():
        
           
        for master in masterDeductions:
            
            try:
                # total cumulative deduction
                ippis_Deduction = master.cumulative_amount
                    
                profile = Profile.objects.get(ippis=master.ippis_number)
                    
                # get all active loans for a user
                myLoans = activeLoans.filter(owner=profile.user)
                    
                # total Monthly Deduction
                total_MonthlyDedcution = activeLoans.aggregate(totalMonthlyDeduction=Sum('monthly_deduction'))
                    
                monthlyDeduction = total_MonthlyDedcution['totalMonthlyDeduction']
                    
                    
                if ippis_Deduction > monthlyDeduction:
                    
                    continue
                    
                    
                userDeductions = allDeductions.filter(loanee=profile.user)
                    
                
                for singleLoan in myLoans:
                    
                    # get principal loan amount
                    loanPrincipal  = singleLoan.approved_amount
                           
                    totalcredit = userDeductions.filter(loan=singleLoan).aggregate(credit=Sum('credit'))
                        
                    totaldebit = userDeductions.filter(loan=singleLoan).aggregate(debit=Sum('debit'))
                        
                    credits = totalcredit['credit']
                    debits = totaldebit['debit']
                        
                    if not credits:
                        credits =0
                    if not debits:
                        debits =0
                            
                    payments = credits-debits
                        
                    # balance
                    bal = loanPrincipal-payments
                        
                    if(bal and bal <= singleLoan.monthly_deduction):
                        
                        ippis_Deduction = ippis_Deduction-bal
                            
                        Deduction.objects.create(  
                                    loanee=profile.user,
                                    loan= singleLoan,
                                    credit = bal,
                                    narration = master.narration,
                                    transaction_date = master.entry_date,
                                    transaction_code = master.transaction_code,
                                    created_by=User.objects.get(pk=userid),
                                    )
                        deactivateLoan(singleLoan)
                            
                           
                            
                    elif(bal and bal > ippis_Deduction):
                        ippis_Deduction = ippis_Deduction-singleLoan.monthly_deduction
                          
                        Deduction.objects.create(  
                                    loanee=profile.user,
                                    loan= singleLoan,
                                    credit = singleLoan.monthly_deduction,
                                    narration = master.narration,
                                    transaction_date = master.entry_date,
                                    transaction_code = master.transaction_code,
                                    created_by=User.objects.get(pk=userid),
                                    )
                        deactivateLoan(singleLoan)
                         
                    elif(ippis_Deduction > bal):
                           continue
                        
                        
                    # update the master record to inactive
                    master.active = False
                    master.save()
                            
                # except Profile.DoesNotExist:
                #     continue
            except Profile.DoesNotExist:
                continue
                
            return Response(
                {'msg':'Loan deductions created successfully'},
                status = status.HTTP_201_CREATED
                )
        else:
            raise ValidationError('No unprocessed deductions yet!')