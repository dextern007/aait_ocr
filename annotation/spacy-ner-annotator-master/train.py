import spacy
import random
import time
import warnings
from spacy.util import minibatch, compounding, decaying
from spacy.gold import GoldParse
from spacy.scorer import Scorer


# Settings for google Collab
# spacy.require_gpu()
# gpu = spacy.prefer_gpu()
# print('GPU:', gpu)


# Downloading models
# spacy.cli.download("en_core_web_sm")
# spacy.cli.download("en_core_web_lg")


TRAIN_DATA = [("R ROSENDINLump SumP.O. Box 49070 DESIGN/BUILDSAN JOSE, CA 95161 COMMERCIAL408-286-2800 INDUSTRIALHIGHWAYBill To: Invoice No: 225022HITEC POWER PROTECTION, INC. Contractor's License: 142881-C1025707 SOUTHWEST FREEWAYROSENBERG, TX 77471Customer Number: 118273Description: May BillingCustomer PO Job No. Job Name Project Manager Division Invoice Date1284363 220224 365 MAIN HITEC Knap, Michael J. 2 05/26/2022REPLACEMENT PRODescriptionContract Amount $4,482,377.00Approved Extras ($449,571.00)Total Contract $4,032,806.00Electrical Installation Complete to Date $4,032,806.00Less: Previous Billings $3,920,413.00Subtotal $112,393.00Tax $0.00Less: Retention $0.00Total Amount Due $112,393.00Make all checks payable to: Rosendin Electric, Inc P.O. Box 49070, SAN JOSE, CA 95161If you have any questions concerning this invoice please call 408-286-2800CONDITIONAL WAIVER AND RELEASE ON FINAL PAYMENTNOTICE: THIS DOCUMENT WAIVES THE CLAIMANT'S LIEN, STOP PAYMENTNOTICE, AND PAYMENT BOND RIGHTS EFFECTIVE ON RECEIPT OF PAYMENT.A PERSON SHOULD NOT RELY ON THIS DOCUMENT UNLESS SATISFIED THATTHE CLAIMANT HAS RECEIVED PAYMENT.Identifying InformationName of Claimant: Rosendin Job#220224_Inv#225022Name of Customer: Hitec Power Protection, Inc.Job Location: Digital Realty SF, 365 Main St., San Francisco, CA. 94105Owner: DIGITAL 365 MAIN LLCConditional Waiver and ReleaseThis document waives and releases lien, stop payment notice, and payment bond rights the claimant hasfor labor and service provided, and equipment and material delivered, to the customer on this job. Rightsbased upon labor or service provided, or equipment or material delivered, pursuant to a written changeorder that has been fully executed by the parties prior to the date that this document is signed by theclaimant, are waived and released by this document, unless listed as an Exception below. This documentis effective only on the claimant's receipt of payment from the financial institution on which the followingcheck is drawn:Maker of Check: Swinerton BuildersAmount of Check: $ 112,393.00Check Payable to: RosendinExceptionsThis document does not affect any of the following: NoneDisputed claims for extras in the amount of: $ 0.00Signatureed by Ginger26 11:09:43 0700Claimant's Signature: ger Anlerasn cng anderson IoS|Claimant's Title: Billing SpecialistDate of Signature: 05/26/20227/1/12Bill To:Hitec Power Protection, Inc.25707 Southwest FreewayROSENDIN ELECTRIC2121 Oakdale AveSan Francisco, CA 94124Rosenberg, Texas 77471 PERIOD ENDING: 05/31/22us accountspayable@hitec-ups.comRusaskia provence@hitec-ups.com REQUEST NO: 25 - FINALGC Job # CUSTOMER NO: 12843631284363 REI JOB NO: 220224Job Name: PROJECT MANAGER: Ray Eudaly365 Main Hitec Replacement ProjectDESCRIPTION OF WORK VALUE WORKICOMRLETED Shonep TOTAL % COMP Ae Ee RETAINAGE 5%TOTAL BILLED] THIS PERIODPreconstruction / Engineering 316,187 316,187 316,187 100% $0SUBTOTAL $316,187 $316,187 $316,187 | 100% $0Material 323,254 320,021 320,021 99% $3,233Labor $1,931,166 $1,564,245 $1,564,245 81% $366,921Subcontracts:Rigging/Storage 304,665 304,665 304,665 | 100%BAS Controls $60,745 $60,745 $60,745 | 100%Sheet Metal Removal/Reinstall 168,854 168,854 168,854 | 100%Scaffold $46,903 $46,903 $46,903 | 100% $0Remove/Reinstall Doors $11,238 $11,238 $11,238 | 100%Permit & Fees $95,000 $66,500 $66,500 70% $28,500General Expenses 402,554 351,287 351,287 87% $51,267Equipment $73,980 $62,883 $62,883 85% $11,097SUBTOTAL $3,418,360 $2,957,341 $2,957,341 87% $461,019Overhead - 12% 410,203 $354,882 $354,882 87% $55,321Markup - 8% 306,285 $264,977 $264,977 87% $41,308SFGRT - .758% $31,342 $27,026 $27,026 86% $4,316SUBTOTAL $4,482,377 $3,920,413 $3,920,413 87% $561,964GMP SAVINGS5/25/2022Tof2Bill To:Hitec Power Protection, Inc.25707 Southwest FreewayROSENDIN ELECTRIC2121 Oakdale AveSan Francisco, CA 94124Rosenberg, Texas 77471 PERIOD ENDING: 05/31/22us accountspayable@hitec-ups.comRusaskia provence@hitec-ups.com REQUEST NO: 25 - FINALGC Job # CUSTOMER NO: 12843631284363 REI JOB NO: 220224Job Name: PROJECT MANAGER: Ray Eudaly365 Main Hitec Replacement ProjectDESCRIPTION OF WORK VALUE WORKICOMRLETED Shonep TOTAL % COMP Ae Ee RETAINAGE 5%TOTAL BILLED] THIS PERIODDeductive Savings - CO ($561,964) ($561,964) ($561,964) 100%Shared Savings - 20% REI - CO $112,393 $112,393 $112,393 | 100%SUBTOTAL ($449,571) $3,920,413 ($449,571)| ($449,571) 100%FINAL CONTRACT TOTALS & BILLING $4,032,806 $3,920,413 $112,393 $4,032,806 | 100% N/A5/25/202220f2", {'entities': [(677, 687, 'total'), (354, 347, 'inv_date'), (251, 257, 'cust_id'), (125, 131, 'invoice_number'), (10, 63, 'vendor_address'), (2, 10, 'vendor_name')]})]

TEST_DATA =  [("R ROSENDINLump SumP.O. Box 49070 DESIGN/BUILDSAN JOSE, CA 95161 COMMERCIAL408-286-2800 INDUSTRIALHIGHWAYBill To: Invoice No: 225022HITEC POWER PROTECTION, INC. Contractor's License: 142881-C1025707 SOUTHWEST FREEWAYROSENBERG, TX 77471Customer Number: 118273Description: May BillingCustomer PO Job No. Job Name Project Manager Division Invoice Date1284363 220224 365 MAIN HITEC Knap, Michael J. 2 05/26/2022REPLACEMENT PRODescriptionContract Amount $4,482,377.00Approved Extras ($449,571.00)Total Contract $4,032,806.00Electrical Installation Complete to Date $4,032,806.00Less: Previous Billings $3,920,413.00Subtotal $112,393.00Tax $0.00Less: Retention $0.00Total Amount Due $112,393.00Make all checks payable to: Rosendin Electric, Inc P.O. Box 49070, SAN JOSE, CA 95161If you have any questions concerning this invoice please call 408-286-2800CONDITIONAL WAIVER AND RELEASE ON FINAL PAYMENTNOTICE: THIS DOCUMENT WAIVES THE CLAIMANT'S LIEN, STOP PAYMENTNOTICE, AND PAYMENT BOND RIGHTS EFFECTIVE ON RECEIPT OF PAYMENT.A PERSON SHOULD NOT RELY ON THIS DOCUMENT UNLESS SATISFIED THATTHE CLAIMANT HAS RECEIVED PAYMENT.Identifying InformationName of Claimant: Rosendin Job#220224_Inv#225022Name of Customer: Hitec Power Protection, Inc.Job Location: Digital Realty SF, 365 Main St., San Francisco, CA. 94105Owner: DIGITAL 365 MAIN LLCConditional Waiver and ReleaseThis document waives and releases lien, stop payment notice, and payment bond rights the claimant hasfor labor and service provided, and equipment and material delivered, to the customer on this job. Rightsbased upon labor or service provided, or equipment or material delivered, pursuant to a written changeorder that has been fully executed by the parties prior to the date that this document is signed by theclaimant, are waived and released by this document, unless listed as an Exception below. This documentis effective only on the claimant's receipt of payment from the financial institution on which the followingcheck is drawn:Maker of Check: Swinerton BuildersAmount of Check: $ 112,393.00Check Payable to: RosendinExceptionsThis document does not affect any of the following: NoneDisputed claims for extras in the amount of: $ 0.00Signatureed by Ginger26 11:09:43 0700Claimant's Signature: ger Anlerasn cng anderson IoS|Claimant's Title: Billing SpecialistDate of Signature: 05/26/20227/1/12Bill To:Hitec Power Protection, Inc.25707 Southwest FreewayROSENDIN ELECTRIC2121 Oakdale AveSan Francisco, CA 94124Rosenberg, Texas 77471 PERIOD ENDING: 05/31/22us accountspayable@hitec-ups.comRusaskia provence@hitec-ups.com REQUEST NO: 25 - FINALGC Job # CUSTOMER NO: 12843631284363 REI JOB NO: 220224Job Name: PROJECT MANAGER: Ray Eudaly365 Main Hitec Replacement ProjectDESCRIPTION OF WORK VALUE WORKICOMRLETED Shonep TOTAL % COMP Ae Ee RETAINAGE 5%TOTAL BILLED] THIS PERIODPreconstruction / Engineering 316,187 316,187 316,187 100% $0SUBTOTAL $316,187 $316,187 $316,187 | 100% $0Material 323,254 320,021 320,021 99% $3,233Labor $1,931,166 $1,564,245 $1,564,245 81% $366,921Subcontracts:Rigging/Storage 304,665 304,665 304,665 | 100%BAS Controls $60,745 $60,745 $60,745 | 100%Sheet Metal Removal/Reinstall 168,854 168,854 168,854 | 100%Scaffold $46,903 $46,903 $46,903 | 100% $0Remove/Reinstall Doors $11,238 $11,238 $11,238 | 100%Permit & Fees $95,000 $66,500 $66,500 70% $28,500General Expenses 402,554 351,287 351,287 87% $51,267Equipment $73,980 $62,883 $62,883 85% $11,097SUBTOTAL $3,418,360 $2,957,341 $2,957,341 87% $461,019Overhead - 12% 410,203 $354,882 $354,882 87% $55,321Markup - 8% 306,285 $264,977 $264,977 87% $41,308SFGRT - .758% $31,342 $27,026 $27,026 86% $4,316SUBTOTAL $4,482,377 $3,920,413 $3,920,413 87% $561,964GMP SAVINGS5/25/2022Tof2Bill To:Hitec Power Protection, Inc.25707 Southwest FreewayROSENDIN ELECTRIC2121 Oakdale AveSan Francisco, CA 94124Rosenberg, Texas 77471 PERIOD ENDING: 05/31/22us accountspayable@hitec-ups.comRusaskia provence@hitec-ups.com REQUEST NO: 25 - FINALGC Job # CUSTOMER NO: 12843631284363 REI JOB NO: 220224Job Name: PROJECT MANAGER: Ray Eudaly365 Main Hitec Replacement ProjectDESCRIPTION OF WORK VALUE WORKICOMRLETED Shonep TOTAL % COMP Ae Ee RETAINAGE 5%TOTAL BILLED] THIS PERIODDeductive Savings - CO ($561,964) ($561,964) ($561,964) 100%Shared Savings - 20% REI - CO $112,393 $112,393 $112,393 | 100%SUBTOTAL ($449,571) $3,920,413 ($449,571)| ($449,571) 100%FINAL CONTRACT TOTALS & BILLING $4,032,806 $3,920,413 $112,393 $4,032,806 | 100% N/A5/25/202220f2", {'entities': [(677, 687, 'total'), (354, 347, 'inv_date'), (251, 257, 'cust_id'), (125, 131, 'invoice_number'), (10, 63, 'vendor_address'), (2, 10, 'vendor_name')]})]

random.seed(0)

# Log files for logging the train and testing scores for references
file = open('output_log.txt','w') 
file.write("iteration_no" + "," + "losses" +"\n")

file1 = open('test_output.txt','w')
file1.write("iteration_no"+ "," +"ents_p"+ "," +"ents_r"+ "," +"ents_f"+ "," +"ents_per_type"+ "\n")

file2 = open('train_output.txt','w')
file2.write("iteration_no"+ "," +"ents_p"+ "," +"ents_r"+ "," +"ents_f"+ "," +"ents_per_type"+ "\n")

model = None # ("en_core_web_sm")   # Replace with model you want to train
start_training_time = time.time()

def train_spacy(data,iterations):

    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("en")  # create blank Language class
        print("Created blank 'en' model")

    TRAIN_DATA = data

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
    
    else:
        ner = nlp.get_pipe("ner")

    # add labels
    for _, annotations in TRAIN_DATA:
         for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    if model is None:
        optimizer = nlp.begin_training()

        # For training with customized cfg 
        nlp.entity.cfg['conv_depth'] = 16
        nlp.entity.cfg['token_vector_width'] = 256
        # nlp.entity.cfg['bilstm_depth'] = 1
        # nlp.entity.cfg['beam_width'] = 2


    else:
        print ("resuming")
        optimizer = nlp.resume_training()
        print (optimizer.learn_rate)
    
    # get names of other pipes to disable them during training
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    
    dropout = decaying(0.8, 0.2, 1e-6) #minimum, max, decay rate
    sizes = compounding(1.0, 4.0, 1.001)

    with nlp.disable_pipes(*other_pipes):  # only train NER
        
        warnings.filterwarnings("once", category=UserWarning, module='spacy')

        for itn in range(iterations):
            
            file = open('outputlog.txt','a') # For logging losses of iterations 
            
            start = time.time() # Iteration Time
            
            if(itn%100 == 0):
                print("Itn  : "+str(itn), time.time()-start_training_time)
                print('Testing')
               
                results = evaluate(nlp, TEST_DATA)
                file1 = open('test_output.txt','a') 
                file1.write(str(itn)+','+ str(results['ents_p'])+','+str(results['ents_r'])+','+str(results['ents_f'])+','+str(results["ents_per_type"])+"\n")
                file1.close()

                results = evaluate(nlp, TRAIN_DATA)
                file2 = open('train_output.txt','a') 
                file2.write(str(itn)+','+ str(results['ents_p'])+','+str(results['ents_r'])+','+str(results['ents_f'])+','+str(results["ents_per_type"])+"\n")
                file2.close()

                modelfile = "training_model"+str(itn)
                nlp.to_disk(modelfile)
  
            # Reducing Learning rate after certain operations 
            if (itn == 300):
                optimizer.learn_rate = 0.0001 
    
            print("Statring iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}

            # use either batches or entire set at once

            ##### For training in Batches
            batches = minibatch(TRAIN_DATA, size=sizes)
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, drop=next(dropout), losses=losses)

            ###########################################

            ##### For training in as a single iteration
            
            # for text, annotations in TRAIN_DATA:
            #     nlp.update(
            #         [text],  # batch of texts
            #         [annotations],  # batch of annotations
            #         drop=0.2,  # dropout - make it harder to memorise data
            #         # drop=next(dropout),  Incase you are using decaying drop
            #         sgd=optimizer,  # callable to update weights
            #         losses=losses)


            print("Losses",losses)
            file.write(str(itn) + "," + str(losses['ner']) +"\n")
            print ("time for iteration:", time.time()-start)
            file.close()

    return nlp


 
def evaluate(ner_model, test_data):
    scorer = Scorer()
    for input_, annot in test_data:
        doc_gold_text = ner_model.make_doc(input_)
        gold = GoldParse(doc_gold_text, entities=annot['entities'])
        pred_value = ner_model(input_)
        scorer.score(pred_value, gold)
    return scorer.scores




prdnlp = train_spacy(TRAIN_DATA, 100)

# Save our trained Model

# uncomment if you want to put model name through command line
# modelfile = input("Enter your Model Name: ")
modelfile = "Final_model"
prdnlp.to_disk(modelfile)

#Test your text
test_text = """R ROSENDIN
Lump Sum
P.O. Box 49070 DESIGN/BUILD
SAN JOSE, CA 95161 COMMERCIAL
408-286-2800 INDUSTRIAL
HIGHWAY
Bill To: Invoice No: 225022
HITEC POWER PROTECTION, INC. Contractor's License: 142881-C10
25707 SOUTHWEST FREEWAY
ROSENBERG, TX 77471
Customer Number: 118273
Description: May Billing
Customer PO Job No. Job Name Project Manager Division Invoice Date
1284363 220224 365 MAIN HITEC Knap, Michael J. 2 05/26/2022
REPLACEMENT PRO
Description
Contract Amount $4,482,377.00
Approved Extras ($449,571.00)
Total Contract $4,032,806.00
Electrical Installation Complete to Date $4,032,806.00
Less: Previous Billings $3,920,413.00
Subtotal $112,393.00
Tax $0.00
Less: Retention $0.00
Total Amount Due $112,393.00
Make all checks payable to: Rosendin Electric, Inc P.O. Box 49070, SAN JOSE, CA 95161
If you have any questions concerning this invoice please call 408-286-2800
CONDITIONAL WAIVER AND RELEASE ON FINAL PAYMENT
NOTICE: THIS DOCUMENT WAIVES THE CLAIMANT'S LIEN, STOP PAYMENT
NOTICE, AND PAYMENT BOND RIGHTS EFFECTIVE ON RECEIPT OF PAYMENT.
A PERSON SHOULD NOT RELY ON THIS DOCUMENT UNLESS SATISFIED THAT
THE CLAIMANT HAS RECEIVED PAYMENT.
Identifying Information
Name of Claimant: Rosendin Job#220224_Inv#225022
Name of Customer: Hitec Power Protection, Inc.
Job Location: Digital Realty SF, 365 Main St., San Francisco, CA. 94105
Owner: DIGITAL 365 MAIN LLC
Conditional Waiver and Release
This document waives and releases lien, stop payment notice, and payment bond rights the claimant has
for labor and service provided, and equipment and material delivered, to the customer on this job. Rights
based upon labor or service provided, or equipment or material delivered, pursuant to a written change
order that has been fully executed by the parties prior to the date that this document is signed by the
claimant, are waived and released by this document, unless listed as an Exception below. This document
is effective only on the claimant's receipt of payment from the financial institution on which the following
check is drawn:
Maker of Check: Swinerton Builders
Amount of Check: $ 112,393.00
Check Payable to: Rosendin
Exceptions
This document does not affect any of the following: None
Disputed claims for extras in the amount of: $ 0.00
Signature
ed by Ginger
26 11:09:43 0700
Claimant's Signature: ger Anlerasn cng anderson Io
S|
Claimant's Title: Billing Specialist
Date of Signature: 05/26/2022
7/1/12
Bill To:
Hitec Power Protection, Inc.
25707 Southwest Freeway
ROSENDIN ELECTRIC
2121 Oakdale Ave
San Francisco, CA 94124
Rosenberg, Texas 77471 PERIOD ENDING: 05/31/22
us accountspayable@hitec-ups.com
Rusaskia provence@hitec-ups.com REQUEST NO: 25 - FINAL
GC Job # CUSTOMER NO: 1284363
1284363 REI JOB NO: 220224
Job Name: PROJECT MANAGER: Ray Eudaly
365 Main Hitec Replacement Project
DESCRIPTION OF WORK VALUE WORKICOMRLETED Shonep TOTAL % COMP Ae Ee RETAINAGE 5%
TOTAL BILLED] THIS PERIOD
Preconstruction / Engineering 316,187 316,187 316,187 100% $0
SUBTOTAL $316,187 $316,187 $316,187 | 100% $0
Material 323,254 320,021 320,021 99% $3,233
Labor $1,931,166 $1,564,245 $1,564,245 81% $366,921
Subcontracts:
Rigging/Storage 304,665 304,665 304,665 | 100%
BAS Controls $60,745 $60,745 $60,745 | 100%
Sheet Metal Removal/Reinstall 168,854 168,854 168,854 | 100%
Scaffold $46,903 $46,903 $46,903 | 100% $0
Remove/Reinstall Doors $11,238 $11,238 $11,238 | 100%
Permit & Fees $95,000 $66,500 $66,500 70% $28,500
General Expenses 402,554 351,287 351,287 87% $51,267
Equipment $73,980 $62,883 $62,883 85% $11,097
SUBTOTAL $3,418,360 $2,957,341 $2,957,341 87% $461,019
Overhead - 12% 410,203 $354,882 $354,882 87% $55,321
Markup - 8% 306,285 $264,977 $264,977 87% $41,308
SFGRT - .758% $31,342 $27,026 $27,026 86% $4,316
SUBTOTAL $4,482,377 $3,920,413 $3,920,413 87% $561,964
GMP SAVINGS
5/25/2022
Tof2
Bill To:
Hitec Power Protection, Inc.
25707 Southwest Freeway
ROSENDIN ELECTRIC
2121 Oakdale Ave
San Francisco, CA 94124
Rosenberg, Texas 77471 PERIOD ENDING: 05/31/22
us accountspayable@hitec-ups.com
Rusaskia provence@hitec-ups.com REQUEST NO: 25 - FINAL
GC Job # CUSTOMER NO: 1284363
1284363 REI JOB NO: 220224
Job Name: PROJECT MANAGER: Ray Eudaly
365 Main Hitec Replacement Project
DESCRIPTION OF WORK VALUE WORKICOMRLETED Shonep TOTAL % COMP Ae Ee RETAINAGE 5%
TOTAL BILLED] THIS PERIOD
Deductive Savings - CO ($561,964) ($561,964) ($561,964) 100%
Shared Savings - 20% REI - CO $112,393 $112,393 $112,393 | 100%
SUBTOTAL ($449,571) $3,920,413 ($449,571)| ($449,571) 100%
FINAL CONTRACT TOTALS & BILLING $4,032,806 $3,920,413 $112,393 $4,032,806 | 100% N/A
5/25/2022
20f2"""
# doc = prdnlp(test_text)
# for ent in doc.ents:
#     print(ent.text, ent.start_char, ent.end_char, ent.label_)

# Prints Final -- f1 score, precision and recall
results = evaluate(prdnlp, TEST_DATA)
import json
# print (json.dumps(results,indent=4))
