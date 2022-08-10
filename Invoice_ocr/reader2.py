
# import typing
# # from borb.pdf.document import Document
# from borb.pdf.pdf import PDF

# # New import
# from borb.toolkit.text.simple_text_extraction import SimpleTextExtraction
# from borb.toolkit.location.location_filter import LocationFilter
# from borb.pdf.canvas.geometry.rectangle import Rectangle
# from decimal import Decimal

# def main():

#     # d: typing.Optional[Document] = None
#     r: Rectangle = Rectangle(Decimal(280),
#                              Decimal(510),
#                              Decimal(200),
#                              Decimal(130))

#     # Set up EventListener(s)
#     l0: LocationFilter = LocationFilter(r)
#     l: SimpleTextExtraction = SimpleTextExtraction()
#     with open("1.pdf", "rb") as pdf_in_handle:
#         d = PDF.loads(pdf_in_handle, [l])

#     assert d is not None
#     print(l.get_text_for_page(1))


# if __name__ == "__main__":
#     main()


# {

# }