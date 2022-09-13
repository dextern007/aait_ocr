from mindee import Client


# Note that the latest version of the API will be called

my_client = Client().config_invoice("03a6d29f915972aa366a34eb0d07325e")


receipt_doc = my_client.doc_from_path("9.pdf")


parsed_receipt = receipt_doc.parse("invoice")

print(parsed_receipt.http_response)