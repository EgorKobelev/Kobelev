import pretty_table_generator
import pdf_generator

option = input("Напишите 1, если хотите сгенерировать таблицу. Напишите 2, если хотите сформировать pdf ")
if (option == "1"):
    pretty_table_generator.get_pretty_table()
elif (option == "2"):
    pdf_generator.get_pdf_statistic()